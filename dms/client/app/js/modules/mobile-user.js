(function (module) {

    module.factory('MobileUserService', function ($http, Config, $upload) {
        return {
            create: function (user, file) {
                return $upload.upload({
                    url: Config.apiUrl + 'mobile-users/',
                    file: file,
                    data: user
                });
            },
            all: function () {
                return $http.get(Config.apiUrl + 'mobile-users/');
            },
            update: function (user) {
                return $http.post(Config.apiUrl + 'mobile-users/' + user.id + '/', user);
            },
            changePassword: function (user) {
                return $http.post(Config.apiUrl + 'mobile-users/' + user.id + '/password/', user);
            }
        };
    });

    module.controller('MobileUserController', function ($scope, $state, MobileUserService) {
        $scope.users = [];

        MobileUserService.all().then(function (response) {
            $scope.users = response.data;
        });

        $scope.showUserProfile = function (user) {
            $state.go('admin.user', {'user': user.id});
        }
    });

    module.controller('AddUserController', function ($scope, MobileUserService, helpers) {
        $scope.modalTitle = 'Add User';
        $scope.user = {};
        $scope.form = {};

        var selectedFile;

        $scope.onFileSelect = function ($files) {
            selectedFile = $files[0];
        };

        $scope.saveUser = function (user) {

            if ($scope.form.user_form.$valid) {
                $scope.saveStatus = true;
                MobileUserService.create(user, selectedFile)
                    .then(function (response) {
                        $scope.saveStatus = false;
                        $scope.user = {};
                        $scope.hasErrors = false;
                        $scope.users.push(response.data);
                    }, function (error) {
                        $scope.errors = error.data;
                        helpers.invalidate($scope.form.user_form, $scope.errors);
                        $scope.saveStatus = false;
                        $scope.hasErrors = true;
                    });

            } else {
                $scope.hasErrors = true;
            }
        };
    });

    module.controller('EditUserController', function ($scope, MobileUserService, helpers) {
        $scope.modalTitle = 'Edit User Profile';
        $scope.form = {};
        $scope.saveUser = function (user) {
            if ($scope.form.user_form.$valid) {
                $scope.successful = false;
                $scope.saveStatus = true;
                delete user.username;
                MobileUserService.update(user)
                    .then(function (response) {
                        $scope.saveStatus = false;
                        $scope.setProfile(response.data);
                        $scope.successful = true;
                        $scope.hasErrors = false;
                    }, function (error) {
                        $scope.errors = error.data;
                        $scope.saveStatus = false;
                        $scope.successful = false;
                        helpers.invalidate($scope.form.user_form, $scope.errors);
                        $scope.hasErrors = true;
                    });
            } else {
                $scope.hasErrors = true;
            }
        }
    });

    module.controller('ChangePasswordController', function ($scope, MobileUserService, growl, helpers) {
        $scope.form = {};
        $scope.changePassword = function (user) {
            if ($scope.form.user_form.$valid) {
                $scope.successful = false;
                $scope.saveStatus = true;
                MobileUserService.changePassword(user)
                    .then(function (response) {
                        $scope.saveStatus = false;
                        $scope.successful = true;
                        $scope.hasErrors = false;
                        growl.success('Password successfully changed', {ttl: 3000});
                    }, function (error) {
                        $scope.errors = error.data;
                        $scope.saveStatus = false;
                        $scope.successful = false;
                        helpers.invalidate($scope.form.user_form, $scope.errors);
                        $scope.hasErrors = true;
                    });
            } else {
                $scope.hasErrors = true;
            }
        }
    });

    module.directive('recipients', function (MobileUserService) {
        return {
            link: function (scope, element) {
                var $select = element.selectize({
                    persist: false,
                    valueField: 'phone',
                    labelField: 'name',
                    searchField: ['name', 'phone'],
                    maxItems: null,
                    create: true,
                    preload: true,
                    createOnBlur: true,
                    load: function (query, callback) {
                        MobileUserService.all().then(function (response) {
                            callback(response.data);
                        });
                    },
                    render: {
                        item: function (item, escape) {
                            return '<div>' +
                                (item.name ? '<span class="name">' + escape(item.name) + '</span>' : '') +
                                (item.phone ? '<span class="phone">' + escape(item.phone) + '</span>' : '') +
                                '</div>';
                        },
                        option: function (item, escape) {
                            var label = item.name || item.phone;
                            var caption = item.phone ? item.phone : null;
                            var location = item.location.name ? item.location.name : null;
                            return '<div>' +
                                '<span class="list-label">' + escape(label) + '</span>' +
                                (location ? '<span class="location">' + escape(location) + '</span>' : '') +
                                (caption ? '<span class="caption">' + escape(caption) + '</span>' : '') +
                                '</div>';
                        }
                    }
                });

                scope.$watch('sms', function (sms) {
                    if (!sms) {
                        var selectize = $select[0].selectize;
                        selectize.clear();
                    }
                });
            }
        }
    });

    module.directive('buttonSwitch', function () {
        return {
            link: function (scope, element, attrs) {
                var onText = attrs.on,
                    offText = attrs.off,
                    sectionIdToToggle = attrs.toggleSection;

                element.html('<a class="btn btn-xs btn-default">' + onText + '</a>' +
                    '<a class="btn btn-xs btn-primary active">' + offText + '</a>');

                element.find('.btn').click(function () {
                    element.find('.btn').toggleClass('active');
                    element.find('.btn').toggleClass('btn-primary');
                    element.find('.btn').toggleClass('btn-default');
                    console.log($('#' + sectionIdToToggle));
                    $('#' + sectionIdToToggle).toggleClass('hide');
                });
            }
        }
    });


    module.directive('userRole', function (User) {
        return {
            link: function (scope, element, attrs) {
                var $select = element.selectize({
                    valueField: 'id',
                    labelField: 'name',
                    searchField: 'name',
                    maxItems: 1,
                    create: false,
                    preload: true,
                    load: function (query, callback) {
                        User.getAllGroups().then(function (response) {
                            callback(response.data)
                        });
                    }
                });

                scope.$watch(attrs.userRole, function (role) {
                    if (!role || Object.keys(role).length == 0) {
                        $select[0].selectize.clear();
                    }
                });
            }
        }
    });

})(angular.module('dms.mobile-user', ['angularFileUpload', 'dms.config', 'angular-growl', 'dms.utils', 'dms.user']));