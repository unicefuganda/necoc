(function (module) {

    module.filter('duration', function ($moment) {
        return function (input) {
            if (!input) return;
            return $moment(input, "YYYY-MM-DDThh:mm").fromNow();
        }
    });

    module.filter('prependSlash', function() {
        return function (input) {
            if (!input) return;
            return ' / ' + input;
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

    module.filter('joinNames', function () {
        return function (input) {
            if (!input) return;
            var names = input.filter(function(input) {
                return input != undefined;
            }).map(function (el) {
                return el.name;
            });
            return names.join(', ');
        }
    });

    module.filter('idsAsString', function() {
        return function (input) {
            if (!input) return;
            return input.map(function (el) {
                return el.id;
            }).join();
        }
    })

})(angular.module('dms.filters', []));
