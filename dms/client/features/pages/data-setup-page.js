var DataSetupPage = function () {
    var request = require('request');

    this.registerDistrict = function (location, next) {
        request.post('http://localhost:7999/api/v1/locations/', {
            form: {
                name: location,
                type: "district"
            }
        }, next);
    };

    this.registerSubCounty = function (district, subcounty, next) {
        request.post('http://localhost:7999/api/v1/locations/', {
            form: {
                name: district,
                type: "district"
            }
        }, function (err, httpResponse, body) {
            request.post('http://localhost:7999/api/v1/locations/', {
                form: {
                    name: subcounty,
                    type: "subcounty",
                    parent: JSON.parse(body).id
                }
            }, next);
        });
    };
};

module.exports = new DataSetupPage();