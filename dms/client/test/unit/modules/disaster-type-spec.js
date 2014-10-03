describe('dms.disaster-type', function () {
    var disasterTypeService;
    var httpMock;
    var scope;
    var apiUrl;
    var disasterTypes = [
        {
            id: "542e6c4fd6f45f19f97d9407",
            name: "Flood"
        }
    ];

    beforeEach(function () {
        module('dms.disaster-type');
        inject(function ($rootScope, DisasterTypeService, $httpBackend, Config) {
            scope = $rootScope.$new();
            apiUrl = Config.apiUrl;
            disasterTypeService = DisasterTypeService;
            httpMock = $httpBackend;
            httpMock.when('GET', apiUrl + 'disaster-types/').respond(disasterTypes);
        });
    });

    describe('DisasterTypeService', function () {

        it('should get all disasters from the api', function () {
            var disastersPromise = disasterTypeService.all()
            httpMock.expectGET(apiUrl + 'disaster-types/');
            httpMock.flush();

            disastersPromise.then(function (response) {
                var retrievedDisasterTypes = response.data;
                expect(retrievedDisasterTypes).toEqual(disasterTypes)
            });

            scope.$apply();
        });
    });
});