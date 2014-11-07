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
                var obtainedStats = statsService.getAggregates({location: 'gulu'});
                httpMock.expectGET(apiUrl + 'location-stats/gulu/').respond({});
                httpMock.flush();
                expect(obtainedStats).toBeDefined();
            });
        });
    });
});