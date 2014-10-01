(function (module) {

    module.factory('MessageService', function ($http, Config) {
        return {
            all: function () {
                return $http.get(Config.apiUrl + 'rapid-pro/');
            },
            filter: function (location_id) {
                return $http.get(Config.apiUrl + 'rapid-pro/?location=' + location_id);
            },
            sendBulkSms: function (sms) {
                return $http.post(Config.apiUrl + 'sent-messages/', sms);
            }
        }
    });

    module.controller('MessageController', function ($scope, MessageService) {

        $scope.$watch('location', function (newLocation) {
            if (!newLocation) {
                MessageService.all().then(function (response) {
                    $scope.messages = response.data;
                });
            } else {
                MessageService.filter(newLocation).then(function (response) {
                    $scope.messages = response.data;
                });
            }

        });

        MessageService.all()
            .then(function (response) {
                $scope.messages = response.data;
            });


    });

    module.config(['growlProvider', function (growlProvider) {
          growlProvider.globalTimeToLive(3000);
    }]);


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

})(angular.module('dms.message', ['dms.config',  'angular-growl']));