(function (module) {


    module.factory('User', function ($http, Config, $q) {
        var cachedPromise,
            cachedGroupPromise

        return {
            getPermissions: function () {
                if (!cachedPromise) {
                    cachedPromise = $http.get(Config.apiUrl + 'current-permissions/');
                }
                return cachedPromise;
            },
            hasPermission: function (permission) {
                return this.getPermissions().then(function (response) {
                    return response.data.permissions.filter(function (perm) {
                        return perm == permission
                    }).length
                }).then(function (exists) {
                    var deferred = $q.defer();
                    exists ? deferred.resolve(true) : deferred.reject();
                    return deferred.promise;
                });
            },
            getAllGroups: function () {
                if (!cachedGroupPromise) {
                    cachedGroupPromise = $http.get(Config.apiUrl + 'groups/');
                }
                return cachedGroupPromise;
            }
        };
    });

    module.directive('ngIfPermissions', function (User, helpers, $q) {
        return {
            link: function (scope, element, attrs) {
                var permissionsList = helpers.stringToArray(attrs.ngIfPermissions, ',');

                var permissionPromises = permissionsList.map(function (permission) {
                    return User.hasPermission(permission)
                });

                $q.all(permissionPromises).then(
                    function () {
                        element.removeClass('hide');
                    },
                    function () {
                        element.addClass('hide');
                    });
            }
        }
    })

})(angular.module('dms.user', ['dms.config', 'dms.utils']));
