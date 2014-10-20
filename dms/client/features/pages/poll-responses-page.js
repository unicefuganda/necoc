var PollResponsesPage = function () {
    var request = require('request');

    this.createPollAndResponse = function (poll_response, poll_payload, location, callback) {
        request.post('http://localhost:7999/api/v1/locations/', {
            form: {
                name: location,
                type: "district"
            }
        }, function (err, httpResponse, location) {
                var location_id = JSON.parse(location).id.toString();
                var mobile_user = {phone: poll_response.phone, name: "thumbbb", email:"haha@ha.ha",
                                   location: location_id};
                request.post('http://localhost:7999/api/v1/mobile-users/', {form: mobile_user},
                function(err, httpResponse) {
                    poll_payload.target_locations = [location_id];
                    request({
                            url: 'http://localhost:7999/api/v1/polls/',
                            method: 'post',
                            body: poll_payload,
                            json: true
                        },
                        function (err, httpResponse, poll) {
                            poll_response.poll = poll.id;
                            request.post('http://localhost:7999/api/v1/poll-responses/',
                                {form: poll_response}, callback);
                        });
                });
        });
    };

    this.getPollResponseData = function (row, key) {
        return element(by.repeater('poll_response in poll_responses').row(row).column('{[{ poll_response.' + key + ' }]}')).getText();
    };

    this.backToPollsPageButton = element(by.id('back-to-polls-btn'));

};

module.exports = new PollResponsesPage();