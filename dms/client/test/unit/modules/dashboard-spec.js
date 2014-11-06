describe('dms.dashboard', function () {

    beforeEach(function () {
        module('dms.dashboard');
    });

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
                $controller('DashboardMessagesController', { $rootScope: scope, $scope: scope});
            });
        });

        it('should add a list of messages to the scope', function () {
            httpMock.expectGET(apiUrl + 'rapid-pro/?from=2014-11-06&to=2014-11-08').respond(messagesStub);
            scope.filter = {from: '2014-11-06', to: '2014-11-07'};
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

    describe('slidingPanel', function () {
        var compile,
            scope,
            element,
            ngElement,
            html = "<div sliding-panel='back-arrow'>" +
                "<span class='back-arrow icon icon-chevron-right-1'></span>" +
                "</div>";

        beforeEach(module('dms.dashboard'));

        beforeEach(inject(function ($compile, $rootScope) {
            scope = $rootScope;
            ngElement = angular.element(html);
            element = $compile(ngElement)(scope);
            scope.$digest();
        }));

        it('should default to left chevron', function () {
            expect(element.html()).toContain("icon-chevron-left");
        });

        it('should change to right chevron on click', function () {
            expect(element.html()).toContain("icon-chevron-left");
            element.find('.back-arrow').trigger('click');
            expect(element.html()).toContain("icon-chevron-right-1");
        });

        it('should animate opening on click', function () {
            spyOn($.fn, 'animate').andCallThrough();
            element.find('.back-arrow').trigger('click');
            expect($.fn.animate).toHaveBeenCalledWith({left: '26%'});
        });

        it('should animate closing on click', function () {
            element.find('.back-arrow').trigger('click');
            spyOn($.fn, 'animate').andCallThrough();
            element.find('.back-arrow').trigger('click');
            expect($.fn.animate).toHaveBeenCalledWith({left: '97%'});
        });
    });


    describe('DashboardController', function () {
        var scope;
        var yesterday = "2014-11-03";

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

        beforeEach(function () {
            inject(function ($rootScope, $controller) {
                scope = $rootScope.$new();
                $controller('DashboardController', {$rootScope: scope, $moment: mockMoment });
            });
        });

        it('should have a time filter on the scope with from date as yesterday', function () {
            expect(scope.filter).toEqual({from: yesterday })
        });
    });
});
