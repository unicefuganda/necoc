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
            all: function (sort_field) {
                return $http.get(Config.apiUrl + 'mobile-users/?ordering=' + sort_field);
            },
            update: function (user, file) {
                return $upload.upload({
                    url: Config.apiUrl + 'mobile-users/' + user.id + '/',
                    file: file,
                    data: user
                });
            },
            changePassword: function (user) {
                return $http.post(Config.apiUrl + 'mobile-users/' + user.id + '/password/', user);
            },
            resetPassword: function (user) {
                return $http.post(Config.apiUrl + 'mobile-users/' + user.id + '/password_reset/');
            }
        };
    });

    module.controller('MobileUserController', function ($scope, $state, MobileUserService) {
        $scope.users = [];
        $scope.sort_field = '-created_at';
        $scope.toggled = false

        listUsers = function(sort_fields){
            MobileUserService.all(sort_fields).then(function (response) {
                $scope.users = response.data;
            });
        }

        $scope.showUserProfile = function (user) {
            $state.go('admin.user', {'user': user.id});
        }

        $scope.notSorted = function(obj){
            if (!obj) {
                return [];
            }
            var sorted = Object.keys(obj);
            //return sorted.sort()
            return sorted
        }

        $scope.toggleAndrebuildList = function(property){
            $scope.toggle(property);
            $scope.rebuildUsersList();
        }

        $scope.toggle = function (property) {
            if(property === 'name'){
                $sort_field = 'name';
                if($scope.nameDesc){
                    $scope.nameDesc = false;
                    $scope.sort_field = 'name';
                }else{
                    $scope.nameDesc = true;
                     $scope.sort_field = '-name';
                }
            }

            if(property === 'location'){
                $sort_field = 'location';
                if($scope.locationDesc){
                    $scope.locationDesc = false;
                    $scope.sort_field = 'location';
                }else{
                    $scope.locationDesc = true;
                     $scope.sort_field = '-location';
                }
            }
        }

        $scope.rebuildUsersList = function() {
            console.log( "Rebuilding list..." );
            $scope.users = listUsers($scope.sort_field);
        };

        //By default list users ordered by created_at descending
        listUsers($scope.sort_field);

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
                user.location = user.subcounty;
                var subcounty = user.subcounty,
                    district = user.district;
                delete user.subcounty;
                delete user.district;

                MobileUserService.create(user, selectedFile)
                    .then(function (response) {
                        $scope.saveStatus = false;
                        $scope.user = {};
                        $scope.hasErrors = false;
                        $scope.users.push(response.data);
                    }, function (error) {
                        user.subcounty = subcounty;
                        user.district = district;
                        user.location = {};
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

        var selectedFile;

        $scope.onFileSelect = function ($files) {
            selectedFile = $files[0];
        };

        $scope.saveUser = function (user) {
            if ($scope.form.user_form.$valid) {
                $scope.successful = false;
                $scope.saveStatus = true;
                user.location = user.subcounty;
                delete user.subcounty;
                delete user.district;
                delete user.username;
                MobileUserService.update(user, selectedFile)
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

    module.controller('ResetPasswordController', function ($scope, MobileUserService, growl) {
        $scope.form = {};
        $scope.resetPassword = function (user) {
            $scope.successful = false;
            $scope.saveStatus = true;
            MobileUserService.resetPassword(user)
                .then(function () {
                    $scope.saveStatus = false;
                    $scope.successful = true;
                    growl.success('Password successfully reset', {ttl: 3000});
                }, function () {
                    $scope.successful = false;
                    $scope.saveStatus = false;
                    growl.error('There was a problem resetting this password', {ttl: 3000});
                });
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
                    offText = attrs.off;

                element.html('<a class="btn btn-xs btn-default">' + onText + '</a>' +
                    '<a class="btn btn-xs btn-primary active">' + offText + '</a>');

                element.find('.btn').click(function () {
                    element.find('.btn').toggleClass('active');
                    element.find('.btn').toggleClass('btn-primary');
                    element.find('.btn').toggleClass('btn-default');
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

                            scope.$watch(attrs.defaultValue, function (defaultValue) {
                                console.log(defaultValue);
                                if (defaultValue) {
                                    $select[0].selectize.setValue(defaultValue);
                                }
                            });
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