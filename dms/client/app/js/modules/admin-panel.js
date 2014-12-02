(function (module) {

    module.controller('MessagesAdminPanelController', function ($scope, MessagesPageFilters) {
        $scope.messageFilter = MessagesPageFilters;
    });

    module.controller('DisastersAdminPanelController', function ($scope, DisastersPageFilters) {
        $scope.disasterFilter = DisastersPageFilters;
    });

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

    module.factory('MessagesPageFilters', function () {
        return {};
    });

    module.factory('DisastersPageFilters', function () {
        return {};
    });

})(angular.module('dms.admin-panel', ['dms.message']));