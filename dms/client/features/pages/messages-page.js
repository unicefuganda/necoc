var MessagesPage = function () {
    var request = require('request');

    this.messages = [
        { phone: "023020302", time: "2014-02-13T02:00:00", relayer: 2, sms: '1', text: "Where are yout",
            relayer_phone: "2939829949", status: "2", direction: "43", event: "43", source: "NECOC Volunteer" },
    ];

    this.postMessage = function () {
        request.post('http://localhost:7999/api/v1/rapid-pro/', {form: this.messages[0]})
    };

    this.postMessages = function (number) {
        for (var i = 0; i < number; i++) {
            var message = { phone: "023020302" + i, time: "2014-02-13T0" + i + ":00:00", relayer: 2, sms: String(i),
                text: "I am message" + i, relayer_phone: "2939829949", status: "2",
                direction: "43", event: "43", source: "NECOC Volunteer" };
            request.post('http://localhost:7999/api/v1/rapid-pro/', {form: message});
        }
    };

    this.numberOfMessages = function () {
        return element.all(by.repeater("message in messages")).count();
    };

    this.getMessageData = function (name, row) {
        return element(by.repeater('message in messages').row(row).column('{[{ message.' + name + ' }]}')).getText();
    }

   this.clickSecondPagination =  function(callback) {
        element(by.repeater("page in showPages").row(1).column('{[{ page }]}')).click();
   }

};

module.exports = new MessagesPage();