(function (module) {

    module.factory('MessageService', function ($http, Config) {
        return {
            all: function () {
                return $http.get(Config.baseUrl + '/api/v1/rapid-pro/');
            }
        }
    });

    module.controller('MessageController', function ($scope, MessageService) {
        MessageService.all()
            .then(function (response) {
                $scope.messages = response.data;
            });
    });

})(angular.module('dms.message', ['dms.config']));