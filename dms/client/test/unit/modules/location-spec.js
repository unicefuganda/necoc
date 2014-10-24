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
                "name": "kampala",
                "type": "district",
                "parent": null
            }
        ];

        countiesStub = [
            {
                "id": "542470d1d6f45f5e141b2272",
                "name": "basie",
                "type": 'county',
                "parent": '5424a8a7d6f45f6642e43a5b'
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

        parishStub = [
            {
                "id": "542470d1d6f45f5e141b2272",
                "name": "some-parish",
                "type": 'parish',
                "parent": 'subcounty-id'
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

        describe('METHOD: counties', function () {
            it('should load county locations', function () {
                var countiesPromise = locationService.counties('district-id');
                httpMock.expectGET(apiUrl + 'locations/?district=district-id&type=county').respond(countiesStub);
                httpMock.flush();

                countiesPromise.then(function (response) {
                    var counties = response.data;
                    expect(counties.length).toEqual(1);
                });

                scope.$apply();
            });
        });

        describe('METHOD: subCounties', function () {
            it('should load subCounty locations', function () {
                var subCountiesPromise = locationService.subcounties('county-id');
                httpMock.expectGET(apiUrl + 'locations/?county=county-id&type=subcounty').respond(subCountiesStub);
                httpMock.flush();

                subCountiesPromise.then(function (response) {
                    var subCounties = response.data;
                    expect(subCounties.length).toEqual(1);
                });

                scope.$apply();
            });
        });

        describe('METHOD: parishes', function () {
            it('should load parish locations', function () {
                var parishPromise = locationService.parishes('sub-county-id');
                httpMock.expectGET(apiUrl + 'locations/?subcounty=sub-county-id&type=parish').respond(parishStub);
                httpMock.flush();

                parishPromise.then(function (response) {
                    var parishes = response.data;
                    expect(parishes.length).toEqual(1);
                });

                scope.$apply();
            });
        });

        describe('METHOD: villages', function () {
            it('should load village locations', function () {
                var villagePromise = locationService.villages('parish-id');
                httpMock.expectGET(apiUrl + 'locations/?parish=parish-id&type=village').respond(parishStub);
                httpMock.flush();

                villagePromise.then(function (response) {
                    var villages = response.data;
                    expect(villages.length).toEqual(1);
                });

                scope.$apply();
            });
        });

    });
});
