var DataSetupPage = function () {
    var request = require('request'),
        self = this;

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

    this.registerDisasterType = function (disasterType, next) {
        request.post('http://localhost:7999/api/v1/disaster-types/', {
            form: {
                name: disasterType
            }
        }, next);
    };

    this.registerDisaster = function (disasterType, district, subcounty, next) {
        self.registerSubCounty(district, subcounty, function (err, httpResponse, locationBody) {
            self.registerDisasterType(disasterType, function (err, httpResponse, disasterTypeBody) {
                request.post('http://localhost:7999/api/v1/disasters/', {
                    form: {
                        name: JSON.parse(disasterTypeBody).id,
                        status: "Assessment",
                        date: "2014-10-24T17:00:00",
                        description: "big disaster",
                        type: "subcounty",
                        location: JSON.parse(locationBody).id
                    }
                }, next);
            });
        });
    }
};

module.exports = new DataSetupPage();