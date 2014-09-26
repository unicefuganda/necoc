describe('dms.location', function () {
    var httpMock;
    var locationService;
    var apiUrl;
    var districtsStub;
    var scope;

    beforeEach(function () {
        module('dms.location');

        districtsStub = [
            {
                "id": "542470d1d6f45f5e141b2272",
                "name": "dadad",
                "type": "district",
                "parent": null
            },
            {
                "id": "5424a8a7d6f45f6642e43a5b",
                "name": "Mokono",
                "type": "district",
                "parent": null
            }
        ];

        inject(function (LocationService, $httpBackend, Config, $rootScope) {
            httpMock = $httpBackend;
            scope = $rootScope.$new();
            apiUrl = Config.apiUrl;
            httpMock.when('GET', apiUrl + 'locations/?type=district').respond(districtsStub);

            locationService = LocationService;
        });
    });

    describe('LocationService', function () {
        describe('METHOD: districts', function () {
            it('should load district locations', function () {
                var districtsPromise = locationService.districts();
                httpMock.expectGET(apiUrl + 'locations/?type=district');
                httpMock.flush();

                districtsPromise.then(function (response) {
                    var districts =  response.data;
                    expect(districts.length).toEqual(2);
                    expect(districts).toEqual(districtsStub)
                });

                scope.$apply();
            });
        });
    });
});
