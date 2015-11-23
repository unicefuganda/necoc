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

    module.controller('MessageController', function ($scope, $moment, MessageService, MessagesPageFilters) {
        $scope.messageFilter = MessagesPageFilters;
        $scope.selected = {};
        $scope.showMessageCheckboxes = true;
        $scope.messageFilter.from = lastWeek();

        $scope.refresh = function () {
            loadMessagesWithFilter($scope.messageFilter);
        };

        $scope.$watch(function () {
                return $scope.messageFilter;
            },
            loadMessagesWithFilter, true);

        MessageService.filter({disaster: ''}).then(function (response) {
            $scope.uncategorizedMessagesCount = response.data.length;
        });

        $scope.setMessages = function (messages) {
            $scope.messages = messages;
        };

        $scope.linkToProfile = function (message) {
            return message.profile_id == null ? false : true;
        }

        function lastWeek() {
            return $moment().subtract(7, 'days').format('YYYY-MM-DD');
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

        function loadMessagesWithFilter(filter) {
            if (filter) {
                $scope.saveStatus = true;
                MessageService.filter(withoutEmptyValues(filter)).then(function (response) {
                    $scope.messages = response.data;
                    $scope.saveStatus = false;
                });
            }
        }
    })

    .directive('openProfile',
       function() {
          return {
             link :   function($document, element, attrs) {
                function openProfile() {
                    var element = angular.element('#sender-profile-modal');
                    var ctrl = element.controller();
                    ctrl.showProfile(attrs.id);
                    element.modal('show');
                }
                element.bind('click', openProfile);
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

    //module.directive('openProfile',
    //   function() {
    //      return {
    //         link :   function($document, element, attrs) {
    //            function openProfile() {
    //                var element = angular.element('#sender-profile-modal');
    //                var ctrl = element.controller();
    //                ctrl.setModel($scope.userId);
    //                element.modal('show');
    //            }
    //            element.bind('click', openProfile);
    //       }
    //   }
    //});

})(angular.module('dms.message', ['dms.config', 'angular-growl', 'dms.utils', 'dms.admin-panel']));
