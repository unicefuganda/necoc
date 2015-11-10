(function (module) {

    module.factory('SettingsService', function ($http, Config) {
        return {
            all: function () {
                return $http.get(Config.apiUrl + 'admin-settings/');
            },
            postSettings: function(data){
                return $http.post(Config.apiUrl + 'admin-settings/',  data);
            },
            updateSettings: function(setting, data){
                return $http.post(Config.apiUrl + 'admin-settings/' + setting + '/',  data);
            }
        };
    });

    module.controller('AdminSettingsController', function ($scope, SettingsService, $stateParams) {
        $scope.name = [];
        $scope.yes_no = [];
        $scope.value_str = [];
        $scope.value_int = [];

        SettingsService.all().then(function (response) {
            angular.forEach(response.data, function(setting_dict, k) {
                angular.forEach(setting_dict, function(val, key){
                    if(key == 'name')
                    {
                        $scope.name.push(val);
                    }
                    if(key == 'yes_no')
                    {
                        $scope.yes_no.push(val);
                    }
                    if(key == 'value_str')
                    {
                        (val == null)? $scope.value_str.push('') : $scope.value_str.push(val);
                    }
                    if(key == 'value_int')
                    {
                        (val == null)? $scope.value_int.push('') : $scope.value_int.push(val);
                    }

                });
            });
        });

        $scope.no_underscores = function(name) {
            return name.replace(/_/g, " ");
        };

        $scope.submitSettings = function() {
            var val_obj = {};
            for (i = 0; i < this.name.length; i++) {
                val_obj = {'name': this.name[i], 'yes_no': this.yes_no[i], 'value_str': this.value_str[i], 'value_int': this.value_int[i]};

                var json_val = JSON.stringify(val_obj, function(key, val){
                    return (val == null)? "":val;
                });
                SettingsService.updateSettings(this.name[i], json_val).then(function () {
                    $scope.hasErrors = false;
                    $scope.successful = true;
                });
            }
        }
    });

})(angular.module("dms.admin-settings", ["dms.config"]));