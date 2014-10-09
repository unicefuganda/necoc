(function (module) {

    module.config(['growlProvider', function (growlProvider) {
        growlProvider.globalTimeToLive(3000);
    }]);

    module.factory('MessageService', function ($http, $q, Config) {
        return {
            all: function () {
                return $http.get(Config.apiUrl + 'rapid-pro/');
            },
            filter: function (filter, filter_id) {
                return $http.get(Config.apiUrl + 'rapid-pro/?'+filter+'=' + filter_id);
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

    module.controller('MessageController', function ($scope, MessageService) {

        $scope.selected = {};

        $scope.$watch('location', function (newLocation) {
            if (!newLocation) {
                MessageService.all().then(function (response) {
                    $scope.messages = response.data;
                });
            } else {
                MessageService.filter('location', newLocation).then(function (response) {
                    $scope.messages = response.data;
                });
            }
        });

        MessageService.filter('disaster', '').then(function (response) {
                $scope.uncategorizedMessages = response.data;
        });

        MessageService.all()
            .then(function (response) {
                $scope.messages = response.data;
            });

        $scope.setMessages = function (messages) {
            $scope.messages = messages;
        }
    });


    module.controller('SmsModalController', function ($scope, growl, MessageService) {

        $scope.sendBulkSms = function () {
            if ($scope.send_sms_form.$valid) {
                $scope.sms.phone_numbers = formatOptions($scope.sms.phone_numbers);
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

        function formatOptions(options) {
            if (options) {
                return options.split(',').map(function (option) {
                    return option;
                });
            }
            return undefined;
        }

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

})(angular.module('dms.message', ['dms.config', 'angular-growl']));