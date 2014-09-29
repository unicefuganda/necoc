var MessagesPage = function () {
    var request = require('request');

    this.messages = [
        { phone: "023020302", time: "2014-02-13T02:00:00", relayer: 2, run: '1', text: "Where are yout",
            source: "NECOC Volunteer" }
    ];

    this.formattedTime = 'Feb 13, 2014 - 2:00AM';

    this.senderLocation = { "name": "Kampala",  "type": "district"};

    this.NecocVolunteer = { "name": "ayoyo",  "phone": this.messages[0].phone, "email": "haha@ha.ha"};


    this.postMessage = function (callback) {
        request.post('http://localhost:7999/api/v1/rapid-pro/', {form: this.messages[0]}, function(){
            callback();
        })
    };

    this.postMessages = function (number, next) {
        var index = 0;
        postInIntervals();

        function postInIntervals () {
            var message = { phone: "023020302" + index, time: "2014-02-13T02:00:00", relayer: 2, run: String(index),
                text: "I am message" + index, source: "NECOC Volunteer" };

            setTimeout(function () {
                if (index < number) {
                    request.post('http://localhost:7999/api/v1/rapid-pro/', {form: message});
                    index ++;
                    postInIntervals();
                } else {
                    next();
                }
            }, 100);
        }
    };

    this.numberOfMessages = function () {
        return element.all(by.repeater("message in messages")).count();
    };

    this.getMessageData = function (name, row) {
        return element(by.repeater('message in messages').row(row).column('{[{ message.' + name + ' }]}')).getText();
    };

    this.clickSecondPagination = function (callback) {
        element(by.repeater("page in showPages").row(1).column('{[{ page }]}')).click();
    };

    this.postLocation = function(callback){
        request.post('http://localhost:7999/api/v1/locations/', {form: this.senderLocation}, function(){
            callback();
        });
    };

    this.selectLocation = function (location) {
        return element(by.className('selectize-input')).click().then(function () {
            element(by.className('option', location)).click()
        });
    };

    this.postMobileUser = function(callback){
        var necocVolunteer = this.NecocVolunteer;
        request.get('http://localhost:7999/api/v1/locations/?format=json', function(error, response, location1){
                var location = JSON.parse(location1);
                necocVolunteer["location"] = location[0].id;
                request.post('http://localhost:7999/api/v1/mobile-users/', {form: necocVolunteer}, function(){
                    callback();
                });
            });
    };

};

module.exports = new MessagesPage();