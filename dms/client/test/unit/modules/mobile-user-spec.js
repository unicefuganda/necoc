describe('dms.mobile-user', function () {
    var httpMock,
        scope,
        apiUrl,
        stateMock;

    var responseStub = {
        "id": "54257147d6f45f6fc1eac346",
        "name": "NavaL",
        "phone": "+3434232324323",
        "location": {
            "created_at": "2014-09-25T22:34:18.218",
            "name": "hhjj",
            "id": "54246e3ad6f45f5de40b137d"
        },
        "email": ""
    };

    beforeEach(function () {
        module('dms.mobile-user');

        inject(function ($httpBackend, $rootScope, Config) {
            httpMock = $httpBackend;
            scope = $rootScope.$new();
            apiUrl = Config.apiUrl;
        });
    });

    describe('MobileUserController', function () {

        beforeEach(function () {
            inject(function ($controller) {
                httpMock.when('GET', apiUrl + 'mobile-users/').respond([responseStub]);
                stateMock = jasmine.createSpyObj('stateMock', ['go']);
                $controller('MobileUserController', {$scope: scope, $state: stateMock});
            })
        });

        it('should add a list of existing users to the scope', function () {
            httpMock.expectGET(apiUrl + 'mobile-users/');
            httpMock.flush();

            expect(scope.users).toEqual([responseStub]);
        });

        it('should add a function to navigate to the use profile', function () {
            scope.showUserProfile(responseStub);
            expect(stateMock.go).toHaveBeenCalledWith('admin.user', {'user': '54257147d6f45f6fc1eac346'});
        });
    });


    describe('MobileUserModalController', function () {
        var initController;

        var errorMessage = {
            phone: [
                "Phone number must be unique"
            ]
        };

        beforeEach(function () {
            inject(function ($controller) {
                httpMock.when('POST', apiUrl + 'mobile-users/').respond(responseStub);

                initController = function (isFormValid) {
                    scope.mobile_user_form = { $valid: isFormValid, phone: { $invalid: false } };
                    scope.user = { name: "Timothy" };
                    scope.users = [];
                    $controller('MobileUserModalController', { $scope: scope });
                };
            })
        });

        it('should post the user to the api endpoint given the form has no errors', function () {
            initController(true);
            scope.saveUser();

            httpMock.expectPOST(apiUrl + 'mobile-users/');
            expect(scope.saveStatus).toBeTruthy();

            httpMock.flush();
            expect(scope.hasErrors).toBeFalsy();
            expect(scope.saveStatus).toBeFalsy();
            expect(scope.user).toBeNull();
            expect(scope.users).toEqual([responseStub]);
        });

        it('should not post the user to the api endpoint given the form has errors', function () {
            initController(false);
            scope.saveUser();
            expect(scope.hasErrors).toBeTruthy();
            expect(scope.user).toEqual({ name: 'Timothy'});
        });

        it('should add error to the scope given the post returns an error code', function () {
            httpMock.expectPOST(apiUrl + 'mobile-users/').respond(400, errorMessage);
            initController(true);
            scope.saveUser();
            httpMock.flush();

            expect(scope.mobile_user_form.phone.$invalid).toBeTruthy();
            expect(scope.hasErrors).toBeTruthy();
            expect(scope.saveStatus).toBeFalsy();
            expect(scope.errors).toEqual(errorMessage);
        });
    });
});