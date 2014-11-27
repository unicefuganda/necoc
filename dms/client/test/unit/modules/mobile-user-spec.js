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
    });

    describe('Controllers', function () {

        beforeEach(function () {
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

                    scope.user = { name: "Timothy" };
                    scope.users = [];
                    initController = function (isFormValid) {
                        $controller('AddUserController', { $scope: scope });
                        scope.form.user_form = { $valid: isFormValid, phone: { $invalid: false } };
                    };
                })
            });

            it('should post the user to the api endpoint given the form has no errors', function () {
                initController(true);
                scope.saveUser({subcounty: '', district: ''});

                httpMock.expectPOST(apiUrl + 'mobile-users/');
                expect(scope.saveStatus).toBeTruthy();

                httpMock.flush();
                expect(scope.hasErrors).toBeFalsy();
                expect(scope.saveStatus).toBeFalsy();
                expect(scope.user).toEqual({});
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
                scope.saveUser({subcounty: '', district: ''});
                httpMock.flush();

                expect(scope.form.user_form.phone.$invalid).toBeTruthy();
                expect(scope.hasErrors).toBeTruthy();
                expect(scope.saveStatus).toBeFalsy();
                expect(scope.errors).toEqual(errorMessage);
            });

            it('should set modalTitle', function () {
                initController(false);
                expect(scope.modalTitle).toEqual('Add User');
            });
        });

        describe('EditUserController', function () {

            var initController,
                errorMessage = {
                    phone: [
                        "Phone number must be unique"
                    ]
                };

            beforeEach(function () {
                inject(function ($controller) {
                    httpMock.when('POST', apiUrl + 'mobile-users/', {}).respond(responseStub);

                    initController = function (isFormValid) {
                        scope.user = { name: "Timothy", subcounty: "", district: "" };
                        scope.users = [];
                        scope.setProfile = jasmine.createSpy();
                        $controller('EditUserController', { $scope: scope });
                        scope.form.user_form = { $valid: isFormValid, phone: { $invalid: false } };
                    };
                })
            });

            it('should update profile with edited information given form is valid', function () {
                initController(true);
                responseStub.phone_no = '2560760540321';
                responseStub.id = '1';
                httpMock.expectPOST(apiUrl + 'mobile-users/1/').respond(responseStub);

                scope.saveUser(responseStub);
                expect(scope.saveStatus).toBeTruthy();
                expect(scope.successful).toBeFalsy();
                httpMock.flush();
                expect(scope.setProfile).toHaveBeenCalledWith(responseStub);
                expect(scope.saveStatus).toBeFalsy();
                expect(scope.successful).toBeTruthy();
                expect(scope.hasErrors).toBeFalsy();
            });

            it('should not send username or subcounty to server', function () {
                initController(true);
                responseStub.phone_no = '2560760540321';
                responseStub.id = '1';
                var formData = angular.copy(responseStub);
                formData.username = 'username';
                httpMock.expectPOST(apiUrl + 'mobile-users/1/').respond(formData);

                scope.saveUser(formData);
                expect(scope.saveStatus).toBeTruthy();
                httpMock.flush();
                expect(scope.saveStatus).toBeFalsy();
                expect(scope.hasErrors).toBeFalsy();
                expect(scope.successful).toBeTruthy();
            });

            it('should not try to update if the form is invalid', function () {
                initController(false);
                scope.saveUser(responseStub);
                expect(scope.hasErrors).toBeTruthy();
                expect(scope.setProfile).not.toHaveBeenCalled();
                expect(scope.successful).toBeFalsy();
            });

            it('should set modalTitle', function () {
                initController(false);
                expect(scope.modalTitle).toEqual('Edit User Profile');
            });

            it('should not update profile with edited information given form is invalid', function () {
                initController(true);
                responseStub.phone_no = '2560760540321';
                responseStub.id = '1';
                httpMock.expectPOST(apiUrl + 'mobile-users/1/').respond(409, errorMessage);

                scope.saveUser(responseStub);
                expect(scope.saveStatus).toBeTruthy();
                httpMock.flush();
                expect(scope.form.user_form.isValid).toBeFalsy();
                expect(scope.setProfile).not.toHaveBeenCalled();
                expect(scope.errors).toEqual(errorMessage);
                expect(scope.saveStatus).toBeFalsy();
                expect(scope.successful).toBeFalsy();
                expect(scope.hasErrors).toBeTruthy();
            });
        });

        describe('ChangePasswordController', function () {
            var initController, mockGrowl,
                newUser = {
                    "id": "54257147d6f45f6fc1eac346",
                    "old_password": "haha",
                    "new_password": "hehe",
                    "confirm_password": "hoho"
                },
                errorMessage = {
                    old_password: [
                        "Current password incorrect."
                    ]
                };

            beforeEach(function () {
                inject(function ($controller) {
                    mockGrowl = jasmine.createSpyObj('growl', ['success']);

                    initController = function (isFormValid) {
                        scope.user = { name: "Timothy" };
                        scope.users = [];
                        $controller('ChangePasswordController', { $scope: scope, growl: mockGrowl });
                        scope.form.user_form = { $valid: isFormValid, old_password: { $invalid: false }};
                    };
                })
            });

            it('should update password given form is valid', function () {
                initController(true);
                httpMock.expectPOST(apiUrl + 'mobile-users/' + newUser.id + '/password/', newUser).respond({});

                scope.changePassword(newUser);

                expect(scope.saveStatus).toBeTruthy();
                expect(scope.successful).toBeFalsy();
                httpMock.flush();
                expect(scope.saveStatus).toBeFalsy();
                expect(scope.successful).toBeTruthy();
                expect(scope.hasErrors).toBeFalsy();
                expect(mockGrowl.success).toHaveBeenCalledWith('Password successfully changed', { ttl: 3000 });
            });

            it('should not try to update if the form is invalid', function () {
                initController(false);
                scope.changePassword(newUser);
                expect(scope.hasErrors).toBeTruthy();
                expect(scope.successful).toBeFalsy();
            });

            it('should not update password given form is invalid server-side', function () {
                initController(true);
                httpMock.expectPOST(apiUrl + 'mobile-users/' + newUser.id + '/password/', newUser).respond(400, errorMessage);

                scope.changePassword(newUser);
                expect(scope.saveStatus).toBeTruthy();
                httpMock.flush();
                expect(scope.form.user_form.isValid).toBeFalsy();
                expect(scope.errors).toEqual(errorMessage);
                expect(scope.saveStatus).toBeFalsy();
                expect(scope.successful).toBeFalsy();
                expect(scope.hasErrors).toBeTruthy();
            });
        });
        describe('ResetPasswordController', function () {
            var initController, mockGrowl,
                newUser = {
                    "id": "54257147d6f45f6fc1eac346"
                };

            beforeEach(function () {
                inject(function ($controller) {
                    mockGrowl = jasmine.createSpyObj('growl', ['success', 'error']);

                    initController = function () {
                        scope.user = { name: "Timothy" };
                        $controller('ResetPasswordController', { $scope: scope, growl: mockGrowl });
                    };
                })
            });

            it('should reset password', function () {
                initController();
                httpMock.expectPOST(apiUrl + 'mobile-users/' + newUser.id + '/password_reset/').respond(200, {});

                scope.resetPassword(newUser);

                expect(scope.saveStatus).toBeTruthy();
                expect(scope.successful).toBeFalsy();
                httpMock.flush();
                expect(scope.saveStatus).toBeFalsy();
                expect(scope.successful).toBeTruthy();
                expect(mockGrowl.success).toHaveBeenCalledWith('Password successfully reset', { ttl: 3000 });
            });

            it('should flash an error if there is a problem resetting', function () {
                initController();
                httpMock.expectPOST(apiUrl + 'mobile-users/' + newUser.id + '/password_reset/').respond(400, {});

                scope.resetPassword(newUser);
                expect(scope.saveStatus).toBeTruthy();
                httpMock.flush();
                expect(scope.saveStatus).toBeFalsy();
                expect(scope.successful).toBeFalsy();
                expect(mockGrowl.error).toHaveBeenCalledWith('There was a problem resetting this password', { ttl: 3000 });
            });
        })
    });

    describe('Stubbed uploading', function () {
        var uploadService,
            initController;

        beforeEach(function () {

            uploadService = createPromiseSpy('$upload', ['upload']);
            module(function ($provide) {
                $provide.value('$upload', uploadService)
            });

            uploadService.when('upload').returnPromiseOf({});

            initController = function (controllerName) {
                inject(function ($controller, Config, $rootScope) {
                    apiUrl = Config.apiUrl;
                    scope = $rootScope.$new();
                    $controller(controllerName, { $scope: scope });
                    scope.form.user_form = { $valid: true, phone: { $invalid: false } };
                });
            }
        });

        it('should post the image to the server during Add', function () {
            initController('AddUserController')
            var imageFile = {data: 'some-image-binary'};
            var user = { name: 'Username', phone: 'PhoneNumber' };

            scope.onFileSelect([imageFile]);
            scope.saveUser(user);
            expect(uploadService.upload).toHaveBeenCalledWith({
                url: apiUrl + 'mobile-users/',
                file: imageFile,
                data: user
            })
        });

        it('should post the image to the server during Edit', function () {
            initController('EditUserController')
            var imageFile = {data: 'some-image-binary'};
            var user = { name: 'Username', phone: 'PhoneNumber', id: 'id' };

            scope.onFileSelect([imageFile]);
            scope.saveUser(user);
            expect(uploadService.upload).toHaveBeenCalledWith({
                url: apiUrl + 'mobile-users/id/',
                file: imageFile,
                data: user
            })
        });
    })
});