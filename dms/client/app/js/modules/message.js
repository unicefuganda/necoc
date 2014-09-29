(function (module) {

    module.factory('MessageService', function ($http, Config) {
        return {
            all: function () {
                return $http.get(Config.baseUrl + '/api/v1/rapid-pro/');
            },
            filter: function (location_id) {
                return $http.get(Config.baseUrl + '/api/v1/rapid-pro/?location='+location_id);
            }
        }
    });

    module.controller('MessageController', function ($scope, MessageService) {

        $scope.$watch('location', function (newLocation) {
           if (!newLocation){
               MessageService.all().then(function(response){
                   $scope.messages = response.data;
               });
           }else{
               MessageService.filter(newLocation).then(function(response){
                   $scope.messages = response.data;
               });
           }

        });

        MessageService.all()
            .then(function (response) {
                $scope.messages = response.data;
            });
    });

})(angular.module('dms.message', ['dms.config']));