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
                request({
                    url: 'http://localhost:7999/api/v1/disasters/',
                    method: 'post',
                    json: true,
                    body: {
                        name: JSON.parse(disasterTypeBody).id,
                        status: "Assessment",
                        date: "2014-10-24T17:00:00",
                        description: "big disaster",
                        type: "subcounty",
                        locations: [JSON.parse(locationBody).id]
                    }
                }, next);
            });
        });
    };

    this.registerMobileUser = function (phoneNumber, locationName, callback) {
        self.registerDistrict(locationName, function (err, httpResponse, location) {
            request.post('http://localhost:7999/api/v1/mobile-users/', {
                form: {
                    phone: phoneNumber,
                    name: "Somename",
                    email: "haha@ha.ha",
                    location: JSON.parse(location).id
                }
            }, function(err, httpResponse, mobileUser){
                callback(err, httpResponse, location);
            });
        });
    };

    this.registerPoll = function (phoneNumber, keyword, locationName, callback) {
        self.registerMobileUser(phoneNumber, locationName, function (err, httpResponse, location) {
            request({
                url: 'http://localhost:7999/api/v1/polls/',
                method: 'post',
                body: {
                    name: "Disaster Poll",
                    question: "How many disasters are in your area?",
                    keyword: keyword,
                    target_locations: [JSON.parse(location).id]
                },
                json: true
            }, callback)
        });
    };


    this.createPollAndResponse = function (phoneNumber, keyword, location, pollText, callback) {
        self.registerPoll(phoneNumber, keyword, location, function (err, httpResponse, poll) {
            request.post('http://localhost:7999/api/v1/poll-responses/', {
                form: {
                    phone: phoneNumber,
                    text: pollText,
                    time: "2014-02-13T02:00:00",
                    relayer: 234,
                    run: "23243",
                    poll: poll.id
                }
            }, function(err, httpResponse, pollResponse){
                callback(poll);
            });
        });
    };

    this.createPollAndResponseFrom = function (pollResponseAttr, callback) {
       return self.createPollAndResponse(pollResponseAttr.phone, pollResponseAttr.keyword,
            pollResponseAttr.location, pollResponseAttr.text, callback);
    };

    this.createMessage = function(messageText) {

    }

}

module.exports = new DataSetupPage();