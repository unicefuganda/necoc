(function (module) {
    module.config(['growlProvider', function (growlProvider) {
        growlProvider.globalTimeToLive(3000);
    }]);

    module.factory('MessageService', function ($http, $q, Config, helpers) {
        return {
            all: function () {
                return $http.get(Config.apiUrl + 'rapid-pro/');
            },
            filter: function (options) {
                var queryString = helpers.buildQueryString(options);
                return $http.get(Config.apiUrl + 'rapid-pro/' + queryString);
            },
            sendBulkSms: function (sms) {
                return $http.post(Config.apiUrl + 'sent-messages/', sms);
            },
            mapToDisaster: function (disasterId, messageIds) {
                var messages = messageIds.map(function (messageId) {
                    return $http.post(Config.apiUrl + 'rapid-pro/' + messageId + '/', {disaster: disasterId});
                });
                return $q.all(messages);
            }
        }
    });

    module.controller('MessageController', function ($scope, MessageService, MessagesPageFilters) {
        $scope.messageFilter = MessagesPageFilters;
        $scope.selected = {};
        $scope.showMessageCheckboxes = true;
        $scope.refresh = function () {
            reloadMessagesWithFilter($scope.messageFilter);
        };
        getAllMessages();
        $scope.$watch(function () {
                return MessagesPageFilters;
            },
            reloadMessagesWithFilter,
            objectEquality = true);

        MessageService.filter({disaster: ''}).then(function (response) {
            $scope.uncategorizedMessagesCount = response.data.length;
        });

        $scope.setMessages = function (messages) {
            $scope.messages = messages;
        };

        function getAllMessages() {
            $scope.saveStatus = true;
            MessageService.all().then(function (response) {
                $scope.saveStatus = false;
                $scope.messages = response.data;
            });
        }

        function withoutEmptyValues(obj) {
            var newObject = angular.copy(obj);
            for (var i in newObject) {
                if (newObject[i] === null || newObject[i] === undefined || newObject[i] == '') {
                    delete newObject[i];
                }
            }
            return newObject
        }

        function reloadMessagesWithFilter(filter) {
            if (!filter) {
                getAllMessages();
            } else {

                $scope.saveStatus = true;
                MessageService.filter(withoutEmptyValues(filter)).then(function (response) {
                    $scope.messages = response.data;
                    $scope.saveStatus = false;
                });
            }
        }
    });


    module.controller('SmsModalController', function ($scope, growl, MessageService, helpers) {

        $scope.sendBulkSms = function () {
            if ($scope.send_sms_form.$valid) {
                $scope.sms.phone_numbers = helpers.stringToArray($scope.sms.phone_numbers, ',');
                $scope.saveStatus = true;
                $scope.successful = false;

                MessageService.sendBulkSms($scope.sms).then(function () {
                    $scope.saveStatus = false;
                    $scope.hasErrors = false;
                    $scope.successful = true;
                    $scope.sms = null;
                    growl.success('Message successfully sent', {
                        ttl: 3000
                    });
                });

            } else {
                $scope.hasErrors = true;
            }
        };
    });

    module.controller('AddToDisasterController', function ($scope, MessageService) {

        $scope.addToDisaster = function () {
            if ($scope.add_to_disaster_form.$valid) {
                $scope.saveStatus = true;
                $scope.successful = false;

                MessageService.mapToDisaster($scope.disaster, $scope.selected.messages)
                    .then(function () {
                        return MessageService.all();
                    })
                    .then(function (response) {
                        $scope.setMessages(response.data);
                        $scope.saveStatus = false;
                        $scope.hasErrors = false;
                        $scope.disaster = null;
                        $scope.successful = true;
                    });

            } else {
                $scope.hasErrors = true;
            }
        }
    });

})(angular.module('dms.message', ['dms.config', 'angular-growl', 'dms.utils', 'dms.admin-panel']));
