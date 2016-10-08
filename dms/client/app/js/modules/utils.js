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

    module.factory('$ulocation', function($rootScope){
        return $rootScope;
    })

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
                if (arr.length>0) {
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
                } else {
                    return ret;
                }
            },
            csvToArray: function( strData, strDelimiter ){
                // ref: http://stackoverflow.com/a/1293163/2343
                // This will parse a delimited string into an array of
                // arrays. The default delimiter is the comma, but this
                // can be overriden in the second argument.

                // Check to see if the delimiter is defined. If not,
                // then default to comma.
                strDelimiter = (strDelimiter || ",");

                // Create a regular expression to parse the CSV values.
                var objPattern = new RegExp(
                    (
                        // Delimiters.
                        "(\\" + strDelimiter + "|\\r?\\n|\\r|^)" +

                        // Quoted fields.
                        "(?:\"([^\"]*(?:\"\"[^\"]*)*)\"|" +

                        // Standard fields.
                        "([^\"\\" + strDelimiter + "\\r\\n]*))"
                    ),
                    "gi"
                    );


                // Create an array to hold our data. Give the array
                // a default empty first row.
                var arrData = [[]];

                // Create an array to hold our individual pattern
                // matching groups.
                var arrMatches = null;


                // Keep looping over the regular expression matches
                // until we can no longer find a match.
                while (arrMatches = objPattern.exec( strData )){

                    // Get the delimiter that was found.
                    var strMatchedDelimiter = arrMatches[ 1 ];

                    // Check to see if the given delimiter has a length
                    // (is not the start of string) and if it matches
                    // field delimiter. If id does not, then we know
                    // that this delimiter is a row delimiter.
                    if (
                        strMatchedDelimiter.length &&
                        strMatchedDelimiter !== strDelimiter
                        ){

                        // Since we have reached a new row of data,
                        // add an empty row to our data array.
                        arrData.push( [] );

                    }

                    var strMatchedValue;

                    // Now that we have our delimiter out of the way,
                    // let's check to see which kind of value we
                    // captured (quoted or unquoted).
                    if (arrMatches[ 2 ]){

                        // We found a quoted value. When we capture
                        // this value, unescape any double quotes.
                        strMatchedValue = arrMatches[ 2 ].replace(
                            new RegExp( "\"\"", "g" ),
                            "\""
                            );

                    } else {

                        // We found a non-quoted value.
                        strMatchedValue = arrMatches[ 3 ];

                    }


                    // Now that we have our value string, let's add
                    // it to the data array.
                    arrData[ arrData.length - 1 ].push( strMatchedValue );
                }

                // Return the parsed data.
                return( arrData );
            },
            clone: function(obj) {
                var copy;

                // Handle the 3 simple types, and null or undefined
                if (null == obj || "object" != typeof obj) return obj;

                // Handle Date
                if (obj instanceof Date) {
                    copy = new Date();
                    copy.setTime(obj.getTime());
                    return copy;
                }

                // Handle Array
                if (obj instanceof Array) {
                    copy = [];
                    for (var i = 0, len = obj.length; i < len; i++) {
                        copy[i] = this.clone(obj[i]);
                    }
                    return copy;
                }

                // Handle Object
                if (obj instanceof Object) {
                    copy = {};
                    for (var attr in obj) {
                        if (obj.hasOwnProperty(attr)) copy[attr] = this.clone(obj[attr]);
                    }
                    return copy;
                }

                throw new Error("Unable to copy obj! Its type isn't supported.");
            }
        }
    });

})(angular.module('dms.utils', []));