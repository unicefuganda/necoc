module.exports = function () {
    var messagesPage = require("../pages/messages-page");


    this.World = require("../support/world").World;

    this.Given(/^I am logged in as a NECOC admin$/, function (next) {
        next();
    });

    this.When(/^I POST messages to the NECOC DMS$/, function (next) {
        messagesPage.postMessages();
        next();
    });

    this.When(/^I visit the messages listing page$/, function (next) {
        browser.get('/');
        next();
    });

    this.Then(/^I should see my messages$/, function (next) {
        var self = this;

        messagesPage.numberOfMessages()
            .then(function (noOfMessages) {
                self.expect(noOfMessages).to.equal(1);
            })
            .then(function () {
                self.expect(messagesPage.getMessageData('sms', 0)).to.eventually.equal(messagesPage.messages[0].sms);
            })
            .then(function () {
                self.expect(messagesPage.getMessageData('text', 0)).to.eventually.equal(messagesPage.messages[0].text);
            })
            .then(function () {
                self.expect(messagesPage.getMessageData('time', 0)).to.eventually.equal(messagesPage.messages[0].time);
            })
            .then(function () {
                self.expect(messagesPage.getMessageData('source', 0)).to.eventually.equal(messagesPage.messages[0].source)
                    .and.notify(next);
            })
    });

};