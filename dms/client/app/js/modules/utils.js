(function (module) {

    module.directive('saveState', function () {
        return {
            link: function (scope, element) {
                scope.$watch('saveStatus', function (state) {
                    return state ? element.button('loading') : element.button('reset');
                });
            }
        };
    });

    module.directive('closeModal', function () {
        return {
            link: function (scope, element, attrs) {
                scope.$watch('successful', function (success) {
                    return success ? $('#' + attrs['closeModal']).modal('hide') : null;
                });
            }
        }
    });

    module.directive('datepicker', function () {
        return {
            link: function (scope, element, attrs) {
                var options = {};

                if (attrs.timepicker !== 'true') {
                    options.timepicker = false;
                    options.format = 'Y-m-d'
                }

                element.datetimepicker(options);
            }
        }
    });

    module.factory('$moment', function () {
        return moment;
    });

    module.factory('$chroma', function () {
        return chroma;
    });

    module.factory('helpers', function () {
        return {
            stringToArray: function (string, seperator) {
                if (string) {
                    return string.split(seperator).map(function (option) {
                        return option;
                    });
                }
                return [];
            },
            invalidate: function (form, errors) {
                Object.keys(errors).forEach(function (key) {
                    form[key].$invalid = true;
                });
            },
            buildQueryString: function (options) {
                var queryString = '?';
                angular.forEach(options, function (value, key) {
                    queryString += key + '=' + value + '&';
                });
                return queryString.slice(0, -1);
            },
            objArrayToCsv: function(arr) {
                var ret = [];
                ret.push('"' + Object.keys(arr[0]).join('","') + '"');
                for (var i = 0, len = arr.length; i < len; i++) {
                    var line = [];
                    for (var key in arr[i]) {
                        if (arr[i].hasOwnProperty(key)) {
                            line.push('"' + arr[i][key] + '"');
                        }
                    }
                    ret.push(line.join(','));
                }
                return ret.join('\n');
            }
        }
    });

})(angular.module('dms.utils', []));