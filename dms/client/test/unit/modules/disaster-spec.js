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
            scope.disaster = { name: "Flood", date: "2014/10/02 19:13", subcounties: 'subcounty_id'};
            scope.disasters = [];
            scope.hasErrors = true;

            scope.saveDisaster();
            httpMock.expectPOST(apiUrl + 'disasters/', {name: "Flood", date: "2014-10-02T19:13", locations: ['subcounty_id'] });
            expect(scope.saveStatus).toBeTruthy();
            httpMock.flush();

            expect(scope.saveStatus).toBeFalsy();
            expect(scope.disaster).toBeNull();
            expect(scope.hasErrors).toBeFalsy();
            expect(scope.disasters).toEqual([disastersStub]);
        });

        it('should not post disaster given the form has errors', function () {
            initController(false);
            scope.saveDisaster();
            expect(scope.hasErrors).toBeTruthy();
        });

        it('should post disaster with location as subcounty if it is given', function () {
            initController(true);
            scope.disaster = { name: "Flood", date: "2014/10/02 19:13",
                district: {name: 'district-name'}, subcounties: 'sub-county-id1,sub-county-id2' };
            scope.disasters = [];

            scope.saveDisaster();
            httpMock.expectPOST(apiUrl + 'disasters/', { name: "Flood", date: "2014-10-02T19:13",
                locations: ['sub-county-id1', 'sub-county-id2'] });
            httpMock.flush();
        });

        it('should post disaster with location as district if no subcounty is given', function () {
            initController(true);
            scope.disaster = { name: "Flood", date: "2014/10/02 19:13", district: 'district-id' };
            scope.disasters = [];

            scope.saveDisaster();
            httpMock.expectPOST(apiUrl + 'disasters/', {name: "Flood", date: "2014-10-02T19:13",
                locations: ['district-id'] });
            httpMock.flush();
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
                    scope.associatedMessages = [];
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

        describe('showAssociatedMessages()', function () {
            it('should add messages associated to a disaster to the scope', function () {
                initController();
                var mockAssociatedMessages = [
                        {name: "mockMessages"}
                    ],
                    disasterStub = {id: "disaster_id"};

                scope.showAssociatedMessages(disasterStub);
                httpMock.expectGET(apiUrl + 'rapid-pro/?disaster=disaster_id').respond(mockAssociatedMessages);

                httpMock.flush();
                expect(scope.associatedMessages).toEqual(mockAssociatedMessages);
                expect(scope.showMessageList).toBeTruthy();
            });
        });

        describe('backToDisasters()', function () {
            it('should set scope.showMessageList to false', function () {
                initController();
                scope.backToDisasters();
                expect(scope.showMessageList).toBeFalsy();
            });
        });

    });
});