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

    describe('AddDisastersModalController', function () {
        var initController;
        var scope;

        beforeEach(function () {
            inject(function ($controller, $rootScope) {
                scope = $rootScope.$new();
                httpMock.when('POST', apiUrl + 'disasters/').respond(disastersStub);
                initController = function (isValid) {
                    $controller('AddDisastersModalController', {$scope: scope});
                    scope.form = {};
                    scope.form.disasters_form = { $valid: isValid  };
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
            expect(scope.disaster).toEqual({});
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

        it('should set modal title', function () {
            initController(true);
            expect(scope.modalTitle).toEqual('Add Disaster');
        });
    });

    describe('EditDisastersModalController', function () {
        var initController,
            scope,
            setDisasterStub,
            disasterStub = {
                name: 'FLOOD',
                description: 'Some description',
                id: 'disaster_id'
            };

        beforeEach(function () {
            inject(function ($controller, $rootScope) {
                scope = $rootScope.$new();
                setDisasterStub = jasmine.createSpy('setDisaster');
                scope.setDisaster = setDisasterStub;
                httpMock.when('POST', apiUrl + 'disasters/' + disasterStub.id + '/').respond(disasterStub);
                initController = function (isValid) {
                    $controller('EditDisastersModalController', {$scope: scope});
                    scope.form = {};
                    scope.form.disasters_form = { $valid: isValid};
                };
            });
        });

        it('should post single disaster given the form is valid', function () {
            var postData = {name: "Flood", date: "2014-10-02T19:13", locations: ['subcounty_id'], id: 'disaster_id' };
            initController(true);
            scope.disaster = { name: "Flood", date: "2014/10/02 19:13", subcounties: 'subcounty_id', id: 'disaster_id'};
            scope.disasters = [];
            scope.hasErrors = true;

            scope.saveDisaster();
            httpMock.expectPOST(apiUrl + 'disasters/' + disasterStub.id + '/', postData);
            expect(scope.saveStatus).toBeTruthy();
            httpMock.flush();
            expect(setDisasterStub).toHaveBeenCalledWith(disasterStub);
            expect(scope.saveStatus).toBeFalsy();
            expect(scope.hasErrors).toBeFalsy();
        });

        it('should not post the disaster given the form has errors', function () {
            initController(false);
            scope.saveDisaster();
            expect(setDisasterStub).not.toHaveBeenCalled();
            expect(scope.hasErrors).toBeTruthy();
        });

        it('should post the disaster with location as subcounty if it is given', function () {
            initController(true);
            scope.disaster = { name: "Flood",
                date: "2014/10/02 19:13",
                id: 'disaster_id',
                district: {name: 'district-name'}, subcounties: 'sub-county-id1,sub-county-id2' };
            scope.disasters = [];

            scope.saveDisaster();
            httpMock.expectPOST(apiUrl + 'disasters/' + disasterStub.id + '/',
                { name: "Flood",
                    id: 'disaster_id',
                    date: "2014-10-02T19:13",
                    locations: ['sub-county-id1', 'sub-county-id2'] });
            httpMock.flush();
        });

        it('should post disaster with location as district if no subcounty is given', function () {
            initController(true);
            scope.disaster = { name: "Flood",
                date: "2014/10/02 19:13",
                id: 'disaster_id',
                district: 'district-id' };
            scope.disasters = [];

            scope.saveDisaster();
            httpMock.expectPOST(apiUrl + 'disasters/' + disasterStub.id + '/',
                {   name: "Flood",
                    date: "2014-10-02T19:13",
                    id: 'disaster_id',
                    locations: ['district-id'] });
            httpMock.flush();
        });

        it('should set modal title', function () {
            initController(true);
            expect(scope.modalTitle).toEqual('Edit Disaster');
        });
    });


    describe('DisastersController', function () {
        var initController,
            scope,
            mockMessageService,
            stateMock;

        beforeEach(function () {
            mockMessageService = createPromiseSpy('mockMessageService', ['filter', 'all']);

            inject(function ($controller, $rootScope) {
                scope = $rootScope.$new();

                httpMock.when('GET', apiUrl + 'disasters/').respond(disastersStub);
                stateMock = jasmine.createSpyObj('stateMock', ['go']);

                initController = function () {
                    scope.associatedMessages = [];
                    $controller('DisastersController', { $scope: scope, MessageService: mockMessageService, $state: stateMock });
                };
            });
        });

        it('should add a list of existing disasters to the scope', function () {
            initController();
            httpMock.expectGET(apiUrl + 'disasters/');
            httpMock.flush();

            expect(scope.disasters).toEqual(disastersStub);
        });

        describe('showDisasterInfo()', function () {
            it('should direct user to disaster info page on click', function () {
                initController();
                scope.showDisasterInfo({id: "disaster_id"});
                expect(stateMock.go).toHaveBeenCalledWith('admin.disaster-info', {'disaster': 'disaster_id'});
            });
        });
    });

    describe('DisasterInfoController', function () {
        var initController,
            scope,
            mockMessageService,
            mockStateParams,
            mockHttp,
            mockState,
            disasterStub = {
                "status": "Assessment",
                "id": "546c5e39a4a12563242a9e91",
                "name": { "name": "FLOOD" },
                "locations": [
                    {
                        "name": "AWACH",
                        "parent": {
                            "name": "GULU"
                        }
                    }
                ],
                "description": "There is a Fire in Kampala",
                "date": "2014-11-19T13:22:00"
            };

        beforeEach(function () {
            mockMessageService = createPromiseSpy('mockMessageService', ['filter', 'all']);
            mockState = jasmine.createSpyObj('mockState', ['go']);
            mockStateParams = { disaster: 'disaster_id' }
            inject(function ($controller, $rootScope, $httpBackend) {
                initController = function () {
                    scope = $rootScope.$new();
                    mockHttp = $httpBackend;
                    scope.associatedMessages = [];
                    $controller('DisasterInfoController', {
                        $scope: scope,
                        MessageService: mockMessageService,
                        $state: mockState,
                        $stateParams: mockStateParams });
                };
            });
        });

        it('should add messages associated to a disaster to the scope', function () {
            var mockAssociatedMessages = [
                { name: "mockMessages" }
            ];

            mockMessageService.when('filter').returnPromiseOf({ data: mockAssociatedMessages });
            initController();
            httpMock.expectGET(apiUrl + 'disasters/disaster_id/').respond({});
            httpMock.flush();
            scope.$apply();
            expect(mockMessageService.filter).toHaveBeenCalledWith({disaster: 'disaster_id'});
            expect(scope.associatedMessages).toEqual(mockAssociatedMessages);
        });

        it('should add disaster information to the scope', function () {
            mockMessageService.when('filter').returnPromiseOf({});
            initController();
            httpMock.expectGET(apiUrl + 'disasters/disaster_id/').respond(disasterStub);
            httpMock.flush();
            scope.$apply();
            expect(scope.disaster).toEqual(disasterStub);
        });
    })
})
;