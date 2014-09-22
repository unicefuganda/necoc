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
        this.expect(messagesPage.numberOfMessages()).to.eventually.equal(1)
            .and.notify(next);
    });

};