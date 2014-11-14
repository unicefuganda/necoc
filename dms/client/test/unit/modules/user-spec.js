describe('dms.user', function () {

    beforeEach(function () {
        module('dms.user');
    });

    describe('User', function () {

        var httpMock,
            user,
            apiUrl,
            scope,
            userPermissionsStub = {
                permissions: [
                    'can_view_profile',
                    'can_edit_others'
                ]
            };

        beforeEach(function () {
            inject(function (User, Config, $rootScope, $httpBackend) {
                httpMock = $httpBackend;
                user = User;
                scope = $rootScope.$new();
                apiUrl = Config.apiUrl;
                httpMock.when('GET', apiUrl + 'current-permissions/').respond(userPermissionsStub);
            });
        });


        describe('METHOD: getPermissions', function () {
            it('should retrieve current users permissions', function () {
                var obtainedPermissions = user.getPermissions();
                httpMock.expectGET(apiUrl + 'current-permissions/');
                httpMock.flush();

                var done = false,
                    permissions;

                runs(function () {
                    obtainedPermissions.then(function (response) {
                        done = true;
                        permissions = response.data
                    });
                    scope.$apply();
                });

                waitsFor(function () {
                    return done;
                });

                runs(function () {
                    expect(permissions).toEqual(userPermissionsStub)
                });
            });
        });

        describe('METHOD: hasPermission', function () {
            it('should return resolved promise if user has a certain permission', function () {
                var hasPermissionPromise = user.hasPermission('can_view_profile');
                httpMock.flush();

                var done = false,
                    hasPermission;

                runs(function () {
                    hasPermissionPromise.then(function () {
                        done = true;
                        hasPermission = true;
                    }, function () {
                        done = true;
                        hasPermission = false;
                    });
                    scope.$apply();
                });

                waitsFor(function () {
                    return done;
                });

                runs(function () {
                    expect(hasPermission).toBeTruthy();
                });
            });

            it('should return rejected promise if user doesnt have a certain permission', function () {
                var hasPermissionPromise = user.hasPermission('can_view_polls');
                httpMock.flush();

                var done = false,
                    hasPermission;

                runs(function () {
                    hasPermissionPromise.then(function () {
                        done = true;
                        hasPermission = true;
                    }, function () {
                        done = true;
                        hasPermission = false;
                    });
                    scope.$apply();
                });

                waitsFor(function () {
                    return done;
                });

                runs(function () {
                    expect(hasPermission).toBeFalsy();
                });
            });
        });
    });

    describe('ngIfPermissions', function () {
        var scope,
            compile,
            element,
            ngElement,
            httpMock,
            apiUrl,
            html = "<div id='test'>" +
                "<div ng-if-permissions='can_view_tests' id='test_view'>Test Tab</div>" +
                "</div>";

        beforeEach(inject(function ($compile, $rootScope, $httpBackend, Config) {
            compile = $compile;
            httpMock = $httpBackend;
            scope = $rootScope;
            apiUrl = Config.apiUrl;
        }));

        function compileDirective() {
            ngElement = angular.element(html);
            element = compile(ngElement)(scope);
            scope.$digest();
            httpMock.flush();
        }

        it('should show element if user has permission', function () {
            httpMock.when('GET', apiUrl + 'current-permissions/').respond({
                permissions: ['can_view_tests']
            });
            ngElement = angular.element(html);
            element = compile(ngElement)(scope);
            scope.$digest();
            httpMock.flush();
            expect(element.find('#test_view').css('display') == 'none').toBeFalsy();
        });

        it('should not show element if user has no permission', function () {
            httpMock.when('GET', apiUrl + 'current-permissions/').respond({
                permissions: ['cannot_view_tests']
            });
            compileDirective();
            expect(element.find('#test_view').css('display') == 'none').toBeTruthy();
        });
    })
});