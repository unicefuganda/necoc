var DataSetupPage = function () {
    var request = require('request'),
        moment = require('moment'),
        exec = require('child_process').exec,
        baseRequest,
        self = this;

    function init(callback) {
        request({
            url: 'http://localhost:7999/api-token-auth/',
            method: 'post',
            json: true,
            body: {
                username: "test_user",
                password: "password"
            }
        }, function (error, response, body) {
            baseRequest = request.defaults({
                headers: {'Authorization': 'Token ' + body.token}
            });
            callback && callback();
        });
    };

    init();

    this.createUser = function (callback) {
        exec('./../../manage.py create_super_user test_user password ' +
            'test_user@nothing.com "Test User" Kampala 1234567890', function (error, stdout, stderr) {
            if (error) {
                console.log(error, stdout, stderr);
                return;
            }
            init(callback);
        });
    };

    this.createUserGroup = function (callback) {
        exec('./../../manage.py create_user_groups test_user', function (error, stdout, stderr) {
            if (error) {
                console.log(error, stdout, stderr);
                return;
            }
            callback();
        });
    };

    this.createUserWithPermission = function (options, callback) {
        var params = options.username + ' ' + options.password + ' ' + options.email + ' ' + options.permission;
        exec('./../../manage.py create_user_with_permission ' + params, function (error, stdout, stderr) {
            if (error) {
                console.log(error, stdout, stderr);
                return;
            }
            callback();
        });
    };

    this.registerDisasterType = function (disasterType, next) {
        baseRequest.post('http://localhost:7999/api/v1/disaster-types/', {
            form: {
                name: disasterType
            }
        }, next);
    };

    this.registerDistrict = function (location, next) {
        baseRequest.post('http://localhost:7999/api/v1/locations/', {
            form: {
                name: location,
                type: "district"
            }
        }, next);
    };

    this.registerSubCounty = function (district, subcounty, next) {
        baseRequest.post('http://localhost:7999/api/v1/locations/', {
            form: {
                name: district,
                type: "district"
            }
        }, function (err, httpResponse, body) {
            baseRequest.post('http://localhost:7999/api/v1/locations/', {
                form: {
                    name: subcounty,
                    type: "subcounty",
                    parent: JSON.parse(body).id
                }
            }, next);
        });
    };

    this.registerDisasterType = function (disasterType, next) {
        baseRequest.post('http://localhost:7999/api/v1/disaster-types/', {
            form: {
                name: disasterType
            }
        }, next);
    };

    this.registerDisaster = function (disasterType, district, subcounty, next) {
        self.registerSubCounty(district, subcounty, function (err, httpResponse, locationBody) {
            self.registerDisasterType(disasterType, function (err, httpResponse, disasterTypeBody) {
                baseRequest({
                    url: 'http://localhost:7999/api/v1/disasters/',
                    method: 'post',
                    json: true,
                    body: {
                        name: JSON.parse(disasterTypeBody).id,
                        status: "Assessment",
                        date: moment().format('YYYY-MM-DDTHH:mm'),
                        description: "big disaster",
                        type: "subcounty",
                        locations: [JSON.parse(locationBody).id]
                    }
                }, next);
            });
        });
    };

    this.registerMobileUser = function (phoneNumber, locationName, email, callback) {
        self.registerDistrict(locationName, function (err, httpResponse, location) {
            baseRequest.post('http://localhost:7999/api/v1/mobile-users/', {
                form: {
                    phone: phoneNumber,
                    name: "Somename",
                    email: email,
                    location: JSON.parse(location).id
                }
            }, function (err, httpResponse) {
                callback(err, httpResponse, location);
            });
        });
    };

    this.registerPoll = function (phoneNumber, keyword, locationName, callback) {
        self.registerMobileUser(phoneNumber, locationName, 'some@email.com', function (err, httpResponse, location) {
            baseRequest({
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
            baseRequest.post('http://localhost:7999/api/v1/poll-responses/', {
                form: {
                    phone: phoneNumber,
                    text: pollText,
                    time: "2014-02-13T02:00:00",
                    relayer: 234,
                    run: "23243",
                    poll: poll.id
                }
            }, function () {
                callback(poll);
            });
        });
    };

    this.createPollAndResponseFrom = function (pollResponseAttr, callback) {
        return self.createPollAndResponse(pollResponseAttr.phone, pollResponseAttr.keyword,
            pollResponseAttr.location, pollResponseAttr.text, callback);
    };

    this.postMessage = function (message, callback) {
        var now = moment().format('YYYY-MM-DDTHH:mm');
        var formatedTime = moment().format('MMM DD, YYYY - h:mmA');

        var sms = {
            phone: message.phone || '+25484384389434',
            time: message.time || now,
            relayer: 2,
            run: 1,
            text: message.text,
            source: 'NECOC Volunteer'
        };

        return baseRequest.post('http://localhost:7999/api/v1/rapid-pro/', {
            form: sms
        }, function () {
            sms.formattedTime = formatedTime;
            callback(sms);
        });
    };

    this.postFullMessage = function (content, callback) {
        baseRequest.post('http://localhost:7999/api/v1/rapid-pro/', {form: content}, callback.bind({}, content));
    };

    this.postMessages = function (number, callback) {
        var messages = [];
        for (var index = 0; index < number; index++) {
            var message = { phone: "023020302" + index, time: "2014-02-13T02:00:00", relayer: 2, run: String(index),
                text: "I am message" + index, source: "NECOC Volunteer" };
            baseRequest.post('http://localhost:7999/api/v1/rapid-pro/', {form: message});
            messages.push(message);
        }
        browser.sleep(800).then(callback.bind({}, messages))
    };

    this.postMobileUser = function (callback) {
        var necocVolunteer = { "name": "ayoyo", "phone": "023020302", "email": "haha@ha.ha"};
        baseRequest.get('http://localhost:7999/api/v1/locations/?format=json', function (error, response, location) {
            necocVolunteer["location"] = JSON.parse(location)[0].id;
            baseRequest.post('http://localhost:7999/api/v1/mobile-users/', {form: necocVolunteer}, function () {
                callback();
            });
        });
    };

};

module.exports = new DataSetupPage();