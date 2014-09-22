var MessagesPage = function () {
    var request = require('request');

    this.title = element(by.className('navbar-brand'));


    this.messages = [
        {
            phone: "023020302",
            time: "2014-02-13T02:00:00",
            relayer: 2,
            sms: '1',
            text: "Where are yout",
            relayer_phone: "2939829949",
            status: "2",
            direction: "43",
            event: "43",
            source: "NECOC Volunteer"
        }
    ];

    this.postMessages =  function () {
        request.post(  'http://localhost:7999/api/v1/rapid-pro/', {form:this.messages[0]})
    }

    this.numberOfMessages = function () {
        return element.all(by.repeater("message in messages")).count();
    };

    this.getMessageData =  function (name, row) {
        return element(by.repeater('message in messages').row(row).column('{[{ message.'+name+' }]}')).getText();
    }

};

module.exports = new MessagesPage();