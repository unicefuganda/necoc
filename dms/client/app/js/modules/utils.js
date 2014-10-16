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
                element.datetimepicker();
            }
        }
    });

    module.factory('$moment', function () {
        return moment;
    });

    module.filter('duration', function ($moment) {
        return function (input) {
            if (!input) return;
            return $moment(input, "YYYY-MM-DDThh:mm").fromNow();
        }
    });

    module.filter('capitalize', function () {
        return function (input) {
            if (!input) return;
            return input.replace(/\w\S*/g, function (txt) {
                return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
            });
        }
    });

    module.factory('helpers', function () {
        return {
            stringToArray: function (string, seperator) {
                if (string) {
                    return string.split(seperator).map(function (option) {
                        return option;
                    });
                }
                return undefined;
            },
            invalidate: function (form, errors) {
                Object.keys(errors).forEach(function (key) {
                    form[key].$invalid = true;
                });
            }
        }
    });

})(angular.module('dms.utils', []));