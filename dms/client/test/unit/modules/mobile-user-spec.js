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


    describe('AddUserController', function () {
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
                    scope.user_form = { $valid: isFormValid, phone: { $invalid: false } };
                    scope.user = { name: "Timothy" };
                    scope.users = [];
                    $controller('AddUserController', { $scope: scope });
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
        });

        it('should add error to the scope given the post returns an error code', function () {
            httpMock.expectPOST(apiUrl + 'mobile-users/').respond(400, errorMessage);
            initController(true);
            scope.saveUser();
            httpMock.flush();

            expect(scope.user_form.phone.$invalid).toBeTruthy();
            expect(scope.hasErrors).toBeTruthy();
            expect(scope.saveStatus).toBeFalsy();
            expect(scope.errors).toEqual(errorMessage);
        });


    });

    describe('EditUserController', function () {

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
                    scope.user_form = { $valid: isFormValid, phone: { $invalid: false } };
                    scope.user = { name: "Timothy" };
                    scope.users = [];
                    $controller('EditUserController', { $scope: scope });
                };
            })
        });

        it('should update profile with edited information given form is valid', function () {
            initController(true);
            responseStub.phone_no = '2560760540321';
            responseStub.id = '1';
            httpMock.expectPOST(apiUrl + 'mobile-users/1/', responseStub).respond(responseStub);

            scope.editUser(responseStub);
            expect(scope.saveStatus).toBeTruthy();
            httpMock.flush();
            expect(scope.profile).toEqual(responseStub);
            expect(scope.saveStatus).toBeFalsy();
            expect(scope.hasErrors).toBeFalsy();
        });

        it('should not send username to server', function () {
            initController(true);
            responseStub.phone_no = '2560760540321';
            responseStub.id = '1';
            var formData = angular.copy(responseStub);
            formData.username = 'username';
            httpMock.expectPOST(apiUrl + 'mobile-users/1/', responseStub).respond(formData);

            scope.editUser(formData);
            expect(scope.saveStatus).toBeTruthy();
            httpMock.flush();
            expect(scope.profile).toEqual(responseStub);
            expect(scope.saveStatus).toBeFalsy();
            expect(scope.hasErrors).toBeFalsy();
        });

        it('should not try to update if the form is invalid', function () {
            initController(false);
            scope.editUser(responseStub);
            expect(scope.hasErrors).toBeTruthy();
        });

        it('should not update profile with edited information given form is invalid', function () {
            initController(true);
            responseStub.phone_no = '2560760540321';
            responseStub.id = '1';
            httpMock.expectPOST(apiUrl + 'mobile-users/1/', responseStub).respond(409, errorMessage);

            scope.editUser(responseStub);
            expect(scope.saveStatus).toBeTruthy();
            httpMock.flush();
            expect(scope.user_form.isValid).toBeFalsy();
            expect(scope.errors).toEqual(errorMessage);
            expect(scope.saveStatus).toBeFalsy();
            expect(scope.hasErrors).toBeTruthy();
        });
    })
});