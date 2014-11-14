(function (module) {


    module.factory('User', function ($http, Config, $q) {
        var cachedPromise;

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
                    exists ? deferred.resolve(2) : deferred.reject();
                    return deferred.promise;
                });
            }
        };
    });

})(angular.module('dms.user', ['dms.config']));
