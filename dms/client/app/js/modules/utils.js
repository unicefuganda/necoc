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

})(angular.module('dms.utils', []));