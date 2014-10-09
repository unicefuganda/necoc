(function (module) {

    module.controller('AdminPanelController', function ($scope, MessageService) {

        MessageService.all()
            .then(function (response) {
                $scope.messages = response.data;
            });
    });


})(angular.module('dms.admin-panel',['dms.message']));