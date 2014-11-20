describe('dms.stats', function () {
    beforeEach(function () {
        module('dms.stats');
    });
    describe('StatService', function () {
        var httpMock,
            statsService,
            apiUrl,
            aggregateStats = {
                busia: {
                    messages: {
                        count: 0,
                        percentage: 0
                    }
                }
            };
        beforeEach(function () {
            inject(function (StatsService, Config, $httpBackend) {
                httpMock = $httpBackend;
                statsService = StatsService;
                apiUrl = Config.apiUrl;
                httpMock.when('GET', apiUrl + 'location-stats/').respond(aggregateStats);
            });
        });
        describe('METHOD: getAggregates', function () {
            it('should fetch aggregate stats', function () {
                var obtainedStats = statsService.getAggregates();
                httpMock.expectGET(apiUrl + 'location-stats/');
                httpMock.flush();
                expect(obtainedStats).toBeDefined();
            });
            it('should filter aggregate stats by date', function () {
                var options = {from: '2014-12-23', to: '2014-12-30'};
                var obtainedStats = statsService.getAggregates(options);
                httpMock.expectGET(apiUrl + 'location-stats/?from=2014-12-23&to=2014-12-30').respond({});
                httpMock.flush();
                expect(obtainedStats).toBeDefined();
            });
            it('should filter aggregate stats of a particular location', function () {
                var obtainedStats = statsService.getAggregates({district: 'gulu'});
                httpMock.expectGET(apiUrl + 'location-stats/gulu/').respond({});
                httpMock.flush();
                expect(obtainedStats).toBeDefined();
            });
        });
    });

    describe('StatsSummaryService', function () {
        var httpMock,
            statsSummaryService,
            apiUrl,
            statSummary = {
                disasters: {
                    count: 0,
                    affected: 0,
                    types: {Flood: 0}
                }
            };

        beforeEach(function () {
            inject(function (StatsSummaryService, Config, $httpBackend) {
                httpMock = $httpBackend;
                statsSummaryService = StatsSummaryService;
                apiUrl = Config.apiUrl;
                httpMock.when('GET', apiUrl + 'stats-summary/').respond(statSummary);
            });
        });

        describe('METHOD: getSummary', function () {
            it('should fetch aggregate summary stats', function () {
                var obtainedStats = statsSummaryService.getSummary();
                httpMock.expectGET(apiUrl + 'stats-summary/');
                httpMock.flush();
                expect(obtainedStats).toBeDefined();
            });

            it('should filter aggregate summary stats by date', function () {
                var options = {from: '2014-12-23', to: '2014-12-30'};
                var obtainedStats = statsSummaryService.getSummary(options);
                httpMock.expectGET(apiUrl + 'stats-summary/?from=2014-12-23&to=2014-12-30').respond({});
                httpMock.flush();
                expect(obtainedStats).toBeDefined();
            });
            it('should filter aggregate summary stats by disaster_type', function () {
                var options = {disaster_type: 'Flood'};
                var obtainedStats = statsSummaryService.getSummary(options);
                httpMock.expectGET(apiUrl + 'stats-summary/?disaster_type=Flood').respond({});
                httpMock.flush();
                expect(obtainedStats).toBeDefined();
            });
            it('should filter aggregate summary stats by location', function () {
                var options = {location: 'kampala'};
                var obtainedStats = statsSummaryService.getSummary(options);
                httpMock.expectGET(apiUrl + 'stats-summary/?location=kampala').respond({});
                httpMock.flush();
                expect(obtainedStats).toBeDefined();
            });
            it('should filter aggregate summary stats by subcounty and district', function () {
                var options = {district: 'kampala', subcounty: 'bukoto'};
                var obtainedStats = statsSummaryService.getSummary(options);
                httpMock.expectGET(apiUrl + 'stats-summary/?district=kampala&subcounty=bukoto').respond({});
                httpMock.flush();
                expect(obtainedStats).toBeDefined();
            });
        });
    });
});