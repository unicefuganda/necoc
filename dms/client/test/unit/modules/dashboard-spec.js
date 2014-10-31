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
                    text: "Where are you?",
                    event: "43",
                    disaster: {
                        locations: [
                            {
                                name: "LIRA PALWO",
                                parent: {
                                    name: "AGAGO"
                                }
                            }
                        ]
                    }
                },
                {
                    phone: "023020301",
                    text: "Fire??",
                    event: "44",
                    disaster: {
                        locations: [
                            {
                                name: "AWACH",
                                parent: {
                                    name: "GULU"
                                }
                            }
                        ]
                    }
                },
                {
                    phone: "023020303",
                    text: "Fire??",
                    event: "45",
                    disaster: {
                        locations: [
                            {
                                name: "PALARO",
                                parent: {
                                    name: "GULU"
                                }
                            }
                        ]
                    }
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

        it('should set district to an empty string by default', function () {
            scope.params = {location: {district: undefined, subcounty: undefined}};
            scope.$apply();
            expect(scope.district).toEqual('');
        });

        it('should set subcounty to an empty string by default', function () {
            scope.params = {location: {district: undefined, subcounty: undefined}};
            scope.$apply();
            expect(scope.subcounty).toEqual('');
        });

        it('should update district on location changes', function () {
            scope.params = {location: {district: 'gulu', subcounty: undefined}};
            scope.$apply();
            expect(scope.district).toEqual('gulu');
            expect(scope.subcounty).toEqual('');
        });

        it('should update subcounty on location changes', function () {
            scope.params = {location: {district: 'gulu', subcounty: 'awach'}};
            scope.$apply();
            expect(scope.district).toEqual('gulu');
            expect(scope.subcounty).toEqual('awach');
        });
    });
});
