var BulkSMSModal = function () {
    this.recipient = element(by.css('.recipient .selectize-input input'));
    this.message = element(by.id('message'));
    this.notification = element(by.css('.sms-toast .growl-item .growl-message'));
    this.sendMessagesButton = element(by.id('send-sms-btn'));

    this.enterRecipientNumber = function (number) {
        return this.recipient.sendKeys(number)
    };

    this.getRecipientsFieldErrors = function (index) {
        return element.all(by.css('#recipient-errors .text-danger')).get(index).getText();
    };

    this.getTextMessageErrors = function (index) {
        return element.all(by.css('#message-errors .text-danger ')).get(index).getText();
    };
};

var MessagesPage = function () {
    var moment = require('moment');

    this.bulkSMSButton = element(by.id('send-bulk-sms'));

    this.senderLocation = { "name": "Kampala", "type": "district"};

    this.messages = [
        { phone: "023020302", time: "2014-02-13T02:00:00", relayer: 2, run: '1',
            text: "NECOC " + this.senderLocation['name'] + " Fire ayoyoooo",
            source: "NECOC Volunteer" }
    ];

    this.createdFormatedTime = function() {
        var format = 'MMM DD, YYYY - h:mmA',
            timeAsString = 'Feb 13, 2014 - 2:00AM',
            timezoneOffset = (-1)* (new Date().getTimezoneOffset()) / 60;
        return moment(timeAsString, format).add(timezoneOffset, 'hours').format(format);
    };

    this.formattedTime = this.createdFormatedTime();

    this.actionsButton = element(by.id('actions-btn'));

    this.associateToDisasterButton = element(by.id('add-to-disaster'));

    this.addToDisasterButton = element(by.id('add-to-disaster-btn'));

    this.associatedStatus = element(by.css('.status .label-success'));

    this.bulkSMSModal = new BulkSMSModal();

    this.checkMessage = function () {
        return element(by.css('input[type="checkbox"]')).click();
    };

    this.getTextByCss = function (selector) {
        return element(by.css(selector)).getText();
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

    this.selectLocation = function (location) {
        return element(by.css('.district-filter .selectize-input')).click().then(function () {
            browser.sleep(200);
            return element(by.cssContainingText('.selectize-dropdown-content .option', location)).click()
        });
    };

    this.selectDisasterBy = function (location) {
        return element(by.css('.add-to-disaster .selectize-input')).click().then(function () {
            browser.sleep(200);
            return element(by.cssContainingText('.selectize-dropdown-content .caption   ', location)).click()
        });
    };

    this.getAddToDisasterErrors = function () {
        return element(by.css("#disaster-errors .text-danger")).getText();
    };

};

module.exports = new MessagesPage();