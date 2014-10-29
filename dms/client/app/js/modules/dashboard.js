(function (module) {
    module.directive('slidingPanel', function () {
        return {
            link: function (scope, element, attrs) {
                var showing = true,
                    chevron = $('.' + attrs.slidingPanel);

                togglePanel();
                chevron.on('click', togglePanel);

                function togglePanel() {
                    if (showing) {
                        chevron.removeClass('icon-chevron-right-1')
                            .addClass('icon-chevron-left');
                        element.animate({left: '97%'});
                    } else {
                        chevron.removeClass('icon-chevron-left')
                            .addClass('icon-chevron-right-1');
                        element.animate({left: '26%'});
                    }
                    showing = !showing;
                }
            }
        }
    })

})(angular.module('dms.dashboard', []));
