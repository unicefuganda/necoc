describe('dms.location', function () {
    var httpMock,
        locationService,
        districtsStub,
        countiesStub,
        subCountiesStub,
        parishStub,
        apiUrl,
        scope;

    beforeEach(function () {
        module('dms.location');

        districtsStub = [
            {
                "id": "542470d1d6f45f5e141b2272",
                "name": "kampala",
                "type": "district",
                "parent": null
            }
        ];

        subCountiesStub = [
            {
                "id": "542470d1d6f45f5e141b2272",
                "name": "some-sub-county",
                "type": 'subcounty',
                "parent": 'county-id'
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
                    var districts = response.data;
                    expect(districts.length).toEqual(1);
                    expect(districts).toEqual(districtsStub)
                });

                scope.$apply();
            });
        });

        describe('METHOD: subCounties', function () {
            it('should load subCounty locations', function () {
                var subCountiesPromise = locationService.subcounties('district-id');
                httpMock.expectGET(apiUrl + 'locations/?district=district-id&type=subcounty').respond(subCountiesStub);
                httpMock.flush();

                subCountiesPromise.then(function (response) {
                    var subCounties = response.data;
                    expect(subCounties.length).toEqual(1);
                });

                scope.$apply();
            });
        });

    });
});
