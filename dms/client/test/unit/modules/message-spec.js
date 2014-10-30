describe('dms.message', function () {
    var $scope;
    var httpMock;
    var messagesStub;
    var apiUrl;
    var initController;
    var interval;

    beforeEach(function () {
        module('dms.message');
        module('dms.config');

        messagesStub = [
            {
                phone: "023020302",
                time: "2014-02-13T02:00:00",
                relayer: 2,
                sms: 1,
                text: "Where are yout",
                relayer_phone: "2939829949",
                status: "2",
                direction: "43",
                event: "43"
            }
        ];

        inject(function ($controller, $rootScope, $httpBackend, $interval, Config) {
            httpMock = $httpBackend;
            interval = $interval;
            apiUrl = Config.apiUrl;
            httpMock.when('GET', apiUrl + 'rapid-pro/').respond(messagesStub);
            httpMock.when('GET', apiUrl + 'rapid-pro/?disaster=').respond(messagesStub);
            $scope = $rootScope.$new();

            initController = function () {
                $controller('MessageController', {$scope: $scope });
            };
        });

    });

    it('should retrieve messages from the \'/api/v1/rapid-pro/\' endpoint and add them to the scope.', function () {
        initController();

        httpMock.expectGET(apiUrl + 'rapid-pro/');
        httpMock.flush();
        expect($scope.messages).toEqual(messagesStub);
    });

    it('should poll messages from the \'/api/v1/rapid-pro/\' endpoint at an interval of 15 seconds', function () {
        initController();

        interval.flush(15000);
        httpMock.flush();
        expect($scope.polled).toBeTruthy();
    });

    it('should retrieve filtered uncategorized messages', function () {
        initController();

        httpMock.expectGET(apiUrl + 'rapid-pro/?disaster=');
        httpMock.flush();
        expect($scope.uncategorizedMessages).toEqual(messagesStub);
    });

    it('should filter message by location given location id', function () {
        initController();
        $scope.location = "location-id";
        var messageStub = { text: "Some text", phone: "45678909876543"};
        httpMock.expectGET(apiUrl + 'rapid-pro/?location=' + $scope.location).respond(messageStub);
        httpMock.flush();
        expect($scope.messages).toEqual(messageStub);
    });

    it('should retrieve all messages when location not supplied', function () {
        initController();
        $scope.location = "location-id";

        var messageStub = [
            { text: "Some text", phone: "45678909876543"}
        ];
        httpMock.expectGET(apiUrl + 'rapid-pro/?location=' + $scope.location).respond(messageStub);
        httpMock.flush();
        expect($scope.messages).toEqual(messageStub);

        $scope.location = "";
        messageStub = [
            { text: "Some text", phone: "45678909876543"},
            { text: "Other text", phone: "45678909876543"}
        ];
        httpMock.expectGET(apiUrl + 'rapid-pro/').respond(messageStub);
        httpMock.flush();
        expect($scope.messages).toEqual(messageStub);
    });

    it('should tell the scope to show messages', function () {
        initController();
        expect($scope.showMessageCheckboxes).toBeTruthy();
    });

    describe('SmsModalController', function () {
        var initController;
        var scope;
        var mockGrowl;

        beforeEach(function () {

            mockGrowl = jasmine.createSpyObj('growl', ['success']);

            inject(function ($controller, $rootScope) {
                initController = function (isFormValid) {
                    scope = $rootScope.$new();
                    scope.send_sms_form = { $valid: isFormValid};
                    $controller('SmsModalController', {$scope: scope, growl: mockGrowl});
                }
            });
        });

        it('should post the sms to the api endpoint given the sms form has no errors', function () {
            initController(true);
            scope.sms = { phone_numbers: "232,4334", text: "message" };
            scope.sendBulkSms();

            httpMock.expectPOST(apiUrl + 'sent-messages/', {"phone_numbers": ["232", "4334"], "text": "message"}).respond({});
            expect(scope.saveStatus).toBeTruthy();
            expect(scope.successful).toBeFalsy();

            httpMock.flush();
            expect(scope.hasErrors).toBeFalsy();
            expect(scope.saveStatus).toBeFalsy();
            expect(scope.successful).toBeTruthy();
            expect(scope.sms).toBeNull();
            expect(mockGrowl.success).toHaveBeenCalledWith('Message successfully sent', { ttl: 3000 });
        });
    });

    describe('AddToDisasterController', function () {
        var initController;
        var scope;

        beforeEach(function () {

            inject(function ($controller, $rootScope) {
                initController = function (isFormValid) {
                    scope = jasmine.createSpyObj('scope', ['setMessages']);
                    scope.add_to_disaster_form = { $valid: isFormValid};
                    $controller('AddToDisasterController', {$scope: scope});
                }
            });
        });

        describe('scope.addToDisaster', function () {
            it('should put a disaster to messages api given form is valid', function () {
                initController(true);
                scope.selected = {messages: ['message-id-1', 'message-id-2']};
                scope.disaster = 'disaster-id';
                scope.addToDisaster();

                httpMock.expectPOST(apiUrl + 'rapid-pro/message-id-1/', { disaster: 'disaster-id'}).respond({});
                httpMock.expectPOST(apiUrl + 'rapid-pro/message-id-2/', { disaster: 'disaster-id'}).respond({});
                httpMock.expectGET(apiUrl + 'rapid-pro/').respond(messagesStub);
                expect(scope.saveStatus).toBeTruthy();
                expect(scope.successful).toBeFalsy();

                httpMock.flush();
                expect(scope.saveStatus).toBeFalsy();
                expect(scope.hasErrors).toBeFalsy();
                expect(scope.successful).toBeTruthy();
                expect(scope.disaster).toBeNull();
                expect(scope.setMessages).toHaveBeenCalledWith(messagesStub);
            });
        })
    });
});