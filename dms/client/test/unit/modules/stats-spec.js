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
                httpMock.when('GET', apiUrl + 'location-stats').respond(aggregateStats);
            });
        });

        describe('.getAggregates()', function () {
            it('should fetch aggregate stats', function () {
                var obtainedStats = statsService.getAggregates();
                httpMock.expectGET(apiUrl + 'location-stats');
                httpMock.flush();
                expect(obtainedStats).toBeDefined();
            });
        });
    });
});