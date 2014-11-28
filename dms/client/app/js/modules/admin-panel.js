(function (module) {

    module.controller('AdminPanelController', function ($scope, MessageService, MessagesPageFilters) {
        $scope.messageFilter = MessagesPageFilters;
        MessageService.all()
            .then(function (response) {
                $scope.messages = response.data;
            });

        MessageService.filter({disaster: ''})
            .then(function (response) {
                $scope.uncategorizedMessagesCount = response.data.length;
            });
    });

    module.factory('MessagesPageFilters', function () {
        return {};
    })

})(angular.module('dms.admin-panel', ['dms.message']));