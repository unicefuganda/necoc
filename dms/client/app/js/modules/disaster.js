(function (module) {

    module.factory('DisasterService', function ($http, Config, $moment, helpers) {
        return {
            create: function (disaster) {
                disaster.date = $moment(disaster.date, "YYYY/MM/DD hh:mm").format('YYYY-MM-DDTHH:mm');
                return $http.post(Config.apiUrl + 'disasters/', disaster);
            },
            update: function (disaster) {
                disaster.date = $moment(disaster.date, "YYYY/MM/DD hh:mm").format('YYYY-MM-DDTHH:mm');
                return $http.post(Config.apiUrl + 'disasters/' + disaster.id + '/', disaster);
            },
            all: function () {
                return $http.get(Config.apiUrl + 'disasters/');
            },
            filter: function (options) {
                var queryString = helpers.buildQueryString(options);
                return   $http.get(Config.apiUrl + 'disasters/' + queryString);
            },
            disaster: function (disasterId) {
                return $http.get(Config.apiUrl + 'disasters/' + disasterId + '/');
            },
            downloadDisasters: function (dstatus, dfrom, dto) {
                return $http.get(Config.apiUrl + 'csv-disasters/?status=' + dstatus + '&from=' + dfrom + '&to=' + dto);
            }
        };
    });

    module.controller('DisastersController', function ($scope, DisasterService, $state, DisastersPageFilters) {

        DisasterService.all().then(function (response) {
            $scope.disasters = response.data;
            $scope.statusOptions = response.data[0]
        });

        this.showDisasterDetail = function(disaster) {
            $scope.$apply( function() {
                DisasterService.disaster(disaster).then(function (response) {
                    $scope.setDisaster(response.data);
                });
            });
        }

        $scope.showDisasterDetail = this.showDisasterDetail;
        $scope.disaster = {};
        $scope.disasterInfo = {};
        $scope.setDisaster = function (data) {
            $scope.disaster = data;
            $scope.disasterInfo = angular.copy($scope.disaster);
        };

        $scope.$watch(function () {
                return DisastersPageFilters;
            }, function (filter) {
                DisasterService.filter(filter)
                    .then(function (response) {
                        $scope.disasters = response.data;
                    });

            }, true);

        $scope.showDisasterInfo = function (disaster) {
            $state.go('admin.disaster-info', {'disaster': disaster.id});
        };
    });

    module.controller('DisasterInfoController', function ($scope, MessageService, DisasterService, $stateParams) {
        var disasterId = $stateParams.disaster;
        $scope.disaster = {};
        $scope.disasterInfo = {};
        $scope.setDisaster = function (data) {
            $scope.disaster = data;
            $scope.disasterInfo = angular.copy($scope.disaster);
        };
        MessageService.filter({disaster: disasterId})
            .then(function (response) {
                $scope.associatedMessages = response.data;
            });
        DisasterService.disaster(disasterId)
            .then(function (response) {
                $scope.setDisaster(response.data);
            });
    });

    module.controller('AddDisastersModalController', function ($scope, DisasterService, helpers) {
        $scope.modalTitle = 'Add Disaster';
        $scope.form = {};
        $scope.disaster = {};
        $scope.saveDisaster = function () {
            if ($scope.form.disasters_form.$valid) {
                $scope.saveStatus = true;
                $scope.disaster.locations = $scope.disaster.subcounties ?
                    helpers.stringToArray($scope.disaster.subcounties, ',') : [ $scope.disaster.district ];

                delete $scope.disaster.district;
                delete $scope.disaster.subcounties;
                DisasterService.create($scope.disaster).then(function (response) {
                    $scope.disaster = {};
                    $scope.saveStatus = false;
                    $scope.hasErrors = false;
                    $scope.disasters.push(response.data);
                });

            } else {
                $scope.hasErrors = true;
            }
        }
    });

    module.controller('EditDisastersModalController', function ($scope, DisasterService, helpers) {
        $scope.modalTitle = 'Edit Disaster';
        $scope.form = {};

        $scope.saveDisaster = function () {
            if ($scope.form.disasters_form.$valid) {
                $scope.successful = false;
                $scope.saveStatus = true;

                $scope.disaster.locations = $scope.disaster.subcounties ?
                    helpers.stringToArray($scope.disaster.subcounties, ',') : [ $scope.disaster.district ];

                delete $scope.disaster.district;
                delete $scope.disaster.subcounties;

                DisasterService.update($scope.disaster).then(function (response) {
                    $scope.setDisaster(response.data);
                    $scope.saveStatus = false;
                    $scope.successful = true;
                    $scope.hasErrors = false;
                });

            } else {
                $scope.hasErrors = true;
            }
        }
    });

    module.controller('DownloadDisastersModalController', function ($scope, growl, DisasterService, helpers) {
        $scope.disaster = {}
        $scope.statusOptions = {
            availableOptions: [
              {id: '1', name: 'Option A'},
              {id: '2', name: 'Option B'},
              {id: '3', name: 'Option C'}
            ]
        }

        $scope.downloadDisasters = function (disaster) {
            $scope.saveStatus = true;

            DisasterService.downloadDisasters(disaster.status, disaster.dfrom, disaster.dto).then(function (response) {
                var data = helpers.objArrayToCsv(response.data);
                var anchor = angular.element('<a/>');
                 anchor.attr({
                     href: 'data:attachment/csv;charset=utf-8,' + encodeURI(data),
                     target: '_blank',
                     download: 'disasters.csv'
                 })[0].click();
                $scope.saveStatus = false;

                //Clean up, remove anchor and call directive to close modal
                anchor.remove();
                $scope.dismiss();

                growl.success('Disasters downloaded successfully', {
                    ttl: 5000
                });
            });

        };

    });

    module.directive('modalClose', function() {
       return {
         restrict: 'A',
         link: function(scope, element, attr) {
           scope.dismiss = function() {
               element.modal('hide');
           };
         }
       }
    });

    module.directive('disasterStatus', function (DisasterConfig) {
        return {
            link: function (scope, element, attrs) {
                var createOptions = function () {
                    var opts = [];
                    DisasterConfig.statuses.forEach(function (status) {
                        opts.push({value: status, name: status});
                    });
                    return opts;
                };

                var $select = element.selectize({
                    valueField: 'value',
                    labelField: 'name',
                    searchField: 'name',
                    maxItems: 1,
                    create: false,
                    preload: true,
                    options: createOptions()
                });

                scope.$watch(attrs.defaultValue, function (defaultValue) {
                    if (defaultValue) {
                        $select[0].selectize.setValue(defaultValue);
                    }
                });

                scope.$watch(attrs.disasterStatus, function (disaster) {
                    if (!disaster) {
                        $select[0].selectize.clear();
                    }
                });
            }
        }
    });

    module.directive('disasters', function (DisasterService, $filter) {
        function locationNameFromDisaster(disaster) {
            var disasterLocation = '';
            if (disaster.locations && disaster.locations[0]) {
                disasterLocation = disaster.locations[0].parent ? disaster.locations[0].parent.name : disaster.locations[0].name
            }
            return disasterLocation;
        }

        return function (scope, element, attrs) {
            var $select = element.selectize({
                valueField: 'id',
                labelField: 'name',
                searchField: ['name', 'location', 'date'],
                maxItems: 1,
                preload: true,
                load: function (query, callback) {
                    DisasterService.all().then(function (response) {
                        var disasters = response.data.map(function (disaster) {
                            return {
                                id: disaster.id,
                                name: disaster.name.name,
                                location: locationNameFromDisaster(disaster),
                                date: $filter('date')(disaster.date, "MMM dd, yyyy - h:mma")
                            };
                        });
                        callback(disasters);
                    });
                },
                render: {
                    item: function (item, escape) {
                        return '<div>' +
                            (item.name ? '<span class="name">' + escape(item.name) + '</span>' : '') +
                            (item.location ? '<span class="phone">' + escape(item.location) + '</span>' : '') +
                            '</div>';
                    },
                    option: function (item, escape) {
                        var label = item.name || item.location;
                        var caption = item.location ? item.location : null;
                        var date = item.date ? item.date : null;
                        return '<div>' +
                            '<span class="list-label">' + escape(label) + '</span>' +
                            (date ? '<span class="caption-right">' + escape(date) + '</span>' : '') +
                            (caption ? '<span class="caption">' + escape(caption) + '</span>' : '') +
                            '</div>';
                    }
                }
            });

            scope.$watch(attrs.disasters, function (disasters) {
                if (!disasters) {
                    $select[0].selectize.clear();
                }
            });
        };

    });

})(angular.module('dms.disaster', ['dms.config', 'dms.utils', 'dms.message', 'dms.utils', 'dms.admin-panel']));
