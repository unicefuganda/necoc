describe('dms.message', function () {
    var $scope;
    var httpMock;
    var messagesStub;
    var initController;
    var interval;
    var yesterday = '2014-11-03';

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

        var mockMoment = function () {
            return {
                format: function () {
                    return yesterday;
                },
                subtract: function () {
                    return this;
                }
            };
        };

        module(function ($provide) {
            $provide.value('$moment', mockMoment)
        });

    });

    describe('MessageController', function () {
        var mockMessageService;
        beforeEach(function () {
            mockMessageService = createPromiseSpy('mockMessageService', ['filter', 'all']);
            mockMessageService.when('all').returnPromiseOf({ data: messagesStub });
            mockMessageService.when('filter').returnPromiseOf({ data: messagesStub });

            inject(function ($controller, $rootScope, $httpBackend, $interval, Config) {
                httpMock = $httpBackend;
                interval = $interval;
                $scope = $rootScope.$new();
                initController = function () {
                    $controller('MessageController', {$scope: $scope, MessageService: mockMessageService });
                };
            });
        });

        it('should retrieve messages from the \'/api/v1/rapid-pro/\' endpoint and add them to the scope.', function () {
            initController();
            expect(mockMessageService.all).toHaveBeenCalled();
            $scope.$apply();
            expect($scope.messages).toEqual(messagesStub);
        });

        it('should retrieve filtered uncategorized message count', function () {
            initController();
            $scope.$apply();
            expect($scope.uncategorizedMessagesCount).toEqual(1);
        });

        it('should filter message by location given location id', function () {
            initController();
            $scope.location = "location-id";
            var messageStub = { text: "Some text", phone: "45678909876543"};
            mockMessageService.when('filter').returnPromiseOf({ data: messageStub });

            $scope.$apply();
            expect(mockMessageService.filter.mostRecentCall.args).toEqual([{ location : 'location-id' }]);
            expect($scope.messages).toEqual(messageStub);
        });

        it('should retrieve all messages when location not supplied', function () {
            initController();
            $scope.location = "location-id";

            var messageStub = [
                { text: "Some text", phone: "45678909876543"}
            ];

            mockMessageService.when('filter').returnPromiseOf({ data: messageStub });

            $scope.$apply();
            expect(mockMessageService.filter.mostRecentCall.args).toEqual([{ location : 'location-id' }]);
            expect($scope.messages).toEqual(messageStub);

            $scope.location = "";
            messageStub = [
                { text: "Some text", phone: "45678909876543"},
                { text: "Other text", phone: "45678909876543"}
            ];
            mockMessageService.when('all').returnPromiseOf({ data: messageStub });

            $scope.$apply();
            expect(mockMessageService.all).toHaveBeenCalled();
            expect($scope.messages).toEqual(messageStub);
        });

        it('should tell the scope to show messages', function () {
            initController();
            expect($scope.showMessageCheckboxes).toBeTruthy();
        });

        describe('$scope.refresh()', function () {
            it('should refresh all messages', function () {
                initController();
                $scope.refresh();
                expect($scope.saveStatus).toBeTruthy();
                $scope.$apply();
                expect($scope.saveStatus).toBeFalsy();
                expect(mockMessageService.all).toHaveBeenCalled();
            });
        });
    });

    describe('MessageService', function () {
        var httpMock,
            apiUrl,
            $scope,
            messageService;

        beforeEach(function () {

            inject(function ($rootScope, $httpBackend, Config, MessageService) {
                httpMock = $httpBackend;
                apiUrl = Config.apiUrl;
                $scope = $rootScope.$new();
                messageService = MessageService;
            });
        });

        describe('METHOD: filter', function () {
            it('should get filter messages filtered by date given the date filter is passed', function () {
                var filter = {disaster: 'disaster-id', from: '2011-02-02'};
                messageService.filter(filter);
                httpMock.expectGET(apiUrl + 'rapid-pro/?disaster=disaster-id&from=2011-02-02').respond(messagesStub);
                httpMock.flush()
            });
        });

        describe('METHOD: all', function () {
            it('should retrieve all messages from api', function () {
                messageService.all();
                httpMock.expectGET(apiUrl + 'rapid-pro/').respond(messagesStub);
                httpMock.flush();
            });
        });

        describe('METHOD: sendBulkSms', function () {
            it('should post the sms to the api endpoint', function () {
                var sms = { phone_numbers: ["232", "4334"], text: "message" };
                messageService.sendBulkSms(sms);
                httpMock.expectPOST(apiUrl + 'sent-messages/', {"phone_numbers": ["232", "4334"], "text": "message"}).respond({});
                httpMock.flush();
            });
        });

        describe('METHOD: mapToDisaster', function () {
            it('should put a disaster to messages api given form is valid', function () {
                var selected = {messages: ['message-id-1', 'message-id-2']};
                var disaster = 'disaster-id';
                messageService.mapToDisaster(disaster, selected.messages);

                httpMock.expectPOST(apiUrl + 'rapid-pro/message-id-1/', { disaster: 'disaster-id'}).respond({});
                httpMock.expectPOST(apiUrl + 'rapid-pro/message-id-2/', { disaster: 'disaster-id'}).respond({});
                httpMock.flush();
            });
        });

    });

    describe('SmsModalController', function () {
        var initController;
        var scope;
        var mockGrowl;
        var mockMessageService;

        beforeEach(function () {
            mockMessageService = createPromiseSpy('mockMessageService', ['sendBulkSms', 'all']);
            mockMessageService.when('sendBulkSms').returnPromiseOf({ data: {} });
            mockGrowl = jasmine.createSpyObj('growl', ['success']);

            inject(function ($controller, $rootScope) {
                initController = function (isFormValid) {
                    scope = $rootScope.$new();
                    scope.send_sms_form = { $valid: isFormValid};
                    $controller('SmsModalController', {$scope: scope, growl: mockGrowl, MessageService: mockMessageService });
                }
            });
        });

        it('should post the sms to the api endpoint given the sms form has no errors', function () {
            initController(true);
            scope.sms = { phone_numbers: "232,4334", text: "message" };
            scope.sendBulkSms();

            expect(scope.saveStatus).toBeTruthy();
            expect(scope.successful).toBeFalsy();
            expect(mockMessageService.sendBulkSms).toHaveBeenCalledWith({ phone_numbers: [ '232', '4334' ], text: 'message' });

            scope.$apply();
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
        var $scope;
        var mockMessageService;

        beforeEach(function () {
            mockMessageService = createPromiseSpy('mockMessageService', ['mapToDisaster', 'all']);
            mockMessageService.when('mapToDisaster').returnPromiseOf({ data: {} });
            mockMessageService.when('all').returnPromiseOf({ data: messagesStub });

            inject(function ($controller, $rootScope) {
                $scope = $rootScope.$new();
                initController = function (isFormValid) {
                    scope = jasmine.createSpyObj('scope', ['setMessages']);
                    scope.add_to_disaster_form = { $valid: isFormValid};
                    $controller('AddToDisasterController', {$scope: scope, MessageService: mockMessageService });
                }
            });
        });

        describe('scope.addToDisaster', function () {
            it('should put a disaster to messages api given form is valid', function () {
                initController(true);
                scope.selected = { messages: ['message-id-1', 'message-id-2'] };
                scope.disaster = 'disaster-id';
                scope.addToDisaster();

                expect(scope.saveStatus).toBeTruthy();
                expect(scope.successful).toBeFalsy();
                expect(mockMessageService.mapToDisaster).toHaveBeenCalledWith('disaster-id', [ 'message-id-1', 'message-id-2' ]);

                $scope.$apply();
                expect(scope.saveStatus).toBeFalsy();
                expect(scope.hasErrors).toBeFalsy();
                expect(scope.successful).toBeTruthy();
                expect(scope.disaster).toBeNull();
                expect(scope.setMessages).toHaveBeenCalledWith(messagesStub);
            });
        })
    });
});
