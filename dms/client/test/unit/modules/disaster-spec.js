describe('dms.disaster', function () {
    var httpMock;
    var apiUrl;
    var disastersStub = [
        {
            status: "Assessment",
            name: {
                name: "Flood",
                description: ""
            },
            location: {
                name: "ADJUMANI"
            },
            description: "Some location"
        }
    ];

    beforeEach(function () {
        module('dms.disaster');

        inject(function ($httpBackend, Config) {
            httpMock = $httpBackend;
            apiUrl = Config.apiUrl;
        });
    });

    describe('DisastersModalController', function () {
        var initController;
        var scope;

        beforeEach(function () {
            inject(function ($controller, $rootScope) {
                scope = $rootScope.$new();
                httpMock.when('POST', apiUrl + 'disasters/').respond(disastersStub);
                initController = function (isValid) {
                    scope.disasters_form = { $valid: isValid};
                    $controller('DisastersModalController', {$scope: scope});
                };
            });
        });

        it('should post disaster given the form is valid', function () {
            initController(true);
            scope.disaster = { name: "Flood", date: "2014/10/02 19:13"};
            scope.disasters = [];

            scope.saveDisaster();
            httpMock.expectPOST(apiUrl + 'disasters/', {name:"Flood", date:"2014-10-02T19:13"});
            expect(scope.saveStatus).toBeTruthy();
            httpMock.flush();

            expect(scope.saveStatus).toBeFalsy();
            expect(scope.disaster).toBeNull();
            expect(scope.disasters).toEqual([disastersStub]);
        });

        it('should not post disaster given the form has errors', function () {
            initController(false);
            scope.saveDisaster();
            expect(scope.hasErrors).toBeTruthy();
        });
    });


    describe('DisastersController', function () {
        var initController;
        var scope;
        beforeEach(function () {
            inject(function ($controller, $rootScope) {
                scope = $rootScope.$new();

                httpMock.when('GET', apiUrl + 'disasters/').respond(disastersStub);
                initController = function () {
                    $controller('DisastersController', { $scope: scope });
                };
            });
        });

        it('should add a list of existing disasters to the scope', function () {
            initController();
            httpMock.expectGET(apiUrl + 'disasters/');
            httpMock.flush();

            expect(scope.disasters).toEqual(disastersStub);
        });
    });
});