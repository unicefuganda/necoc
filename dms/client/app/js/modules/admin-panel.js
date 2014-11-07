(function (module) {

    module.controller('AdminPanelController', function ($scope, MessageService) {

        MessageService.all()
            .then(function (response) {
                $scope.messages = response.data;
            });

        MessageService.filter({disaster: ''})
            .then(function (response) {
                $scope.uncategorizedMessagesCount = response.data.length;
            });
    });

})(angular.module('dms.admin-panel', ['dms.message']));