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

        it('should remove disaster_type from filter when cleared', function () {
            httpMock.expectGET(apiUrl + 'rapid-pro/?from=2014-11-06').respond(messagesStub);
            scope.filter = {from: '2014-11-06', disaster_type: undefined};
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
            initElement,
            ngElement,
            html = "<div data-for='message' sliding-panel='back-arrow'>" +
                "<span class='back-arrow icon icon-chevron-right-1'></span>" +
                "</div>";

        beforeEach(module('dms.dashboard'));

        beforeEach(inject(function ($compile, $rootScope) {
            scope = $rootScope;
            initElement = function (aHtml) {
                ngElement = angular.element(aHtml);
                element = $compile(ngElement)(scope);
                scope.$digest();
            };
            initElement(html);
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

        it('should animate opening on click much to the left for stats overlay', function () {
            var stats_html = "<div data-for='stats' sliding-panel='back-arrow'>" +
                "<span class='back-arrow icon icon-chevron-right-1'></span>" +
                "</div>";

            initElement(stats_html);

            spyOn($.fn, 'animate').andCallThrough();
            element.find('.back-arrow').trigger('click');
            expect($.fn.animate).toHaveBeenCalledWith({left: '70%'});
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

    describe('DashboardStatsController', function () {
        var scope,
            apiUrl,
            httpMock,
            stateSummaryStub,
            disasterData,
            disasterStatsChartsData;

        beforeEach(function () {
            module('dms.dashboard');
            module('dms.stats');
            stateSummaryStub = {
                disasters: {
                    count: 0,
                    affected: 0,
                    types: {Flood: 0}
                }
            };
            disasterData = [
                ['Flood', 0]
            ];

            inject(function ($controller, $rootScope, $httpBackend, Config, ChartConfig) {
                httpMock = $httpBackend;
                apiUrl = Config.apiUrl;
                scope = $rootScope.$new();
                disasterStatsChartsData = {
                    options: ChartConfig,
                    title: {text: ''}
                    };

                httpMock.when('GET', apiUrl + 'stats-summary/').respond(stateSummaryStub);
                $controller('DashboardStatsController', { $rootScope: scope, $scope: scope});
            });
        });

        it('should add stats summary to the scope', function () {
            httpMock.expectGET(apiUrl + 'stats-summary/?from=2014-11-06&to=2014-11-08').respond(stateSummaryStub);
            scope.filter = {from: '2014-11-06', to: '2014-11-07'};
            httpMock.flush();

            expect(scope.stats).toEqual(stateSummaryStub);
            expect(scope.disasterTypeDistribution).toEqual(disasterData);
            expect(scope.series).toEqual([{data: disasterData}]);

            disasterStatsChartsData.series = [{data: disasterData}];
            expect(scope.disasterStatsCharts).toEqual(disasterStatsChartsData);
        });

        it('should remove disaster_type from filter when cleared', function () {
            httpMock.expectGET(apiUrl + 'stats-summary/?from=2014-11-06').respond(stateSummaryStub);
            scope.filter = {from: '2014-11-06', disaster_type: undefined};
            httpMock.flush();

            expect(scope.stats).toEqual(stateSummaryStub);
            expect(scope.disasterTypeDistribution).toEqual(disasterData);
            expect(scope.series).toEqual([{data: disasterData}]);

            disasterStatsChartsData.series = [{data: disasterData}];
            expect(scope.disasterStatsCharts).toEqual(disasterStatsChartsData);
        });

        it('should set Uganda and Districts as locationTitles by default', function () {
            scope.params = {};
            scope.$apply();

            expect(scope.locationTitles).toEqual({name: 'Uganda', subLocation: 'Districts'});
        });

        it('should set disctict name and subcounties as locationTitles, when location is district', function () {
            scope.params = {location: {district: 'kampala'}};
            scope.$apply();

            expect(scope.locationTitles).toEqual({name: 'KAMPALA District', subLocation: 'Subcounties'});
        });

//        it('should set subcounty name and subcounties as locationTitles, when location is subcounty, and make the corresponding api call', function () {
//            scope.params = {location: {district: 'kampala', subcounty: 'bukoto'}};
////            scope.$apply()
//
//            httpMock.expectGET(apiUrl + 'stats-summary/?subcounty=bukoto').respond(stateSummaryStub);
//            httpMock.flush();
//
//            expect(scope.locationTitles).toEqual({name: 'BUKOTO District', subLocation: 'Subcounties'});
//            expect(scope.stats).toEqual(stateSummaryStub);
//            expect(scope.disasterTypeDistribution).toEqual(disasterData);
//            expect(scope.series).toEqual([{data: disasterData}]);
//        });

    });

});
