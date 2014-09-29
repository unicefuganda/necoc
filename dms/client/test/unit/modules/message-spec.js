describe('dms.message', function () {
    var $scope;
    var httpMock;
    var messagesStub;
    var baseUrl;
    var initController;

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

        inject(function ($controller, $rootScope, $httpBackend, Config) {
            httpMock = $httpBackend;
            baseUrl = Config.baseUrl;
            httpMock.when('GET', baseUrl + '/api/v1/rapid-pro/').respond(messagesStub);

            initController = function () {
                $scope = $rootScope.$new();
                $controller('MessageController', {$scope: $scope});
            }
        });

    });

    it('should retrieve messages from the \'/api/v1/rapid-pro/\' endpoint and add them to the scope.', function () {
        initController();

        httpMock.expectGET(baseUrl + '/api/v1/rapid-pro/');
        httpMock.flush();
        expect($scope.messages).toEqual(messagesStub);
    });

    it('should filter message by location given location id', function () {
        initController();
        $scope.location = "location-id";
        var messageStub = { text:"Some text", phone: "45678909876543"};
        httpMock.expectGET(baseUrl + '/api/v1/rapid-pro/?location='+$scope.location).respond(messageStub);
        httpMock.flush();
        expect($scope.messages).toEqual(messageStub);
    });

    it('should retrieve all messages when location not supplied', function () {
        initController();
        $scope.location = "location-id";

        var messageStub = [{ text:"Some text", phone: "45678909876543"}];
        httpMock.expectGET(baseUrl + '/api/v1/rapid-pro/?location='+$scope.location).respond(messageStub);
        httpMock.flush();
        expect($scope.messages).toEqual(messageStub);

        $scope.location = "";
        messageStub = [{ text:"Some text", phone: "45678909876543"}, { text:"Other text", phone: "45678909876543"}];
        httpMock.expectGET(baseUrl + '/api/v1/rapid-pro/').respond(messageStub);
        httpMock.flush();
        expect($scope.messages).toEqual(messageStub);
    });

});