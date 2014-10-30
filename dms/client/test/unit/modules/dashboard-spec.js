describe('dms.dashboard', function () {

    describe('DashboardMessagesController', function () {
        var scope,
            apiUrl,
            httpMock,
            messagesStub;

        beforeEach(function () {
            module('dms.dashboard');
            messagesStub = [
                {
                    phone: "023020302",
                    time: "2014-02-13T02:00:00",
                    relayer: 2,
                    sms: 1,
                    text: "Where are you?",
                    relayer_phone: "2939829949",
                    status: "2",
                    direction: "43",
                    event: "43"
                }
            ];

            inject(function ($controller, $rootScope, $httpBackend, Config) {
                httpMock = $httpBackend;
                apiUrl = Config.apiUrl;
                scope = $rootScope.$new();

                httpMock.when('GET', apiUrl + 'rapid-pro/').respond(messagesStub);
                $controller('DashboardMessagesController', { $scope: scope});
            });
        });

        it('should add a list of messages to the scope', function () {
            httpMock.expectGET(apiUrl + 'rapid-pro/');
            httpMock.flush();
            expect(scope.messages).toEqual(messagesStub);
        });

        it('should tell the scope not to show checkboxes', function () {
            expect(scope.showMessageCheckboxes).toBeFalsy();
        });
    });
});
