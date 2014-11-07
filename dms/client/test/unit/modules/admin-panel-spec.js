describe('dms.admin-panel', function () {
    var $scope,
        httpMock,
        messagesStub,
        apiUrl,
        initController,
        uncategorizedMessagesStub,
        mockMessageService;

    beforeEach(function () {
        module('dms.admin-panel');
        module('dms.message');

        messagesStub = [
            {
                phone: "023020302",
                time: "2014-02-13T02:00:00",
                relayer: 2,
                sms: 1,
                text: "Where are you",
                relayer_phone: "2939829949",
                status: "2",
                direction: "43",
                event: "43"
            }
        ];
        uncategorizedMessagesStub = [
            {
                phone: "0230350302",
                time: "2014-02-13T02:00:00",
                relayer: 3,
                sms: 1,
                text: "Why are you there",
                relayer_phone: "2033827749",
                status: "2",
                direction: "44",
                event: "44"
            }
        ];

        inject(function ($controller, $rootScope, $httpBackend, Config) {
            httpMock = $httpBackend;
            apiUrl = Config.apiUrl;
            mockMessageService = createPromiseSpy('mockMessageService', ['filter', 'all']);
            mockMessageService.when('filter').returnPromiseOf({ data:uncategorizedMessagesStub });
            mockMessageService.when('all').returnPromiseOf({ data:messagesStub });

            initController = function () {
                $scope = $rootScope.$new();
                $controller('AdminPanelController', {$scope: $scope, MessageService: mockMessageService });
            }
        });

    });

    it('should retrieve messages from the \'/api/v1/rapid-pro/\' endpoint and add them to the scope.', function () {
        initController();

        $scope.$apply();
        expect(mockMessageService.all).toHaveBeenCalled();
        expect($scope.messages).toEqual(messagesStub);
    });

    it('should retrieve uncategorized messages and add them to the scope.', function () {
        initController();

        $scope.$apply();
        expect(mockMessageService.filter).toHaveBeenCalledWith({disaster: ''});
        expect($scope.uncategorizedMessagesCount).toEqual(1);
    });

});
