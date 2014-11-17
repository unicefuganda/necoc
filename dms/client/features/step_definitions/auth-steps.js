module.exports = function () {
    var homePage = require("../pages/home-page"),
        dataSetUpPage = require("../pages/data-setup-page");

    this.World = require("../support/world").World;


    this.Then(/^I should not see the users tab$/, function (next) {
        this.expect(homePage.usersTab.isDisplayed()).to.eventually.be.false.and.notify(next);
    });

    this.Then(/^I should see the users tab$/, function (next) {
        this.expect(homePage.usersTab.isDisplayed()).to.eventually.be.true.and.notify(next);
    });

    this.Then(/^I should not see the disasters tab$/, function (next) {
        this.expect(homePage.disastersTab.isDisplayed()).to.eventually.be.false.and.notify(next);
    });

    this.Then(/^I should see the disasters tab$/, function (next) {
        this.expect(homePage.disastersTab.isDisplayed()).to.eventually.be.true.and.notify(next);
    });

    this.Then(/^I should not see the messages tab$/, function (next) {
        this.expect(homePage.messagesTab.isDisplayed()).to.eventually.be.false.and.notify(next);
    });

    this.Then(/^I should see the messages tab$/, function (next) {
        this.expect(homePage.messagesTab.isDisplayed()).to.eventually.be.true.and.notify(next);
    });

    this.Then(/^I should not route to "([^"]*)"$/, function (location, next) {
        var self = this;
        browser.setLocation(location).then(function () {
            browser.getCurrentUrl().then(function (url) {
                self.expect(url.match(/dashboard/).length > 0).to.be.true;
                next()
            });
        });
    });

    this.Then(/^I can route to "([^"]*)"$/, function (location, next) {
        var self = this;
        browser.setLocation(location).then(function () {
            browser.getCurrentUrl().then(function (url) {
                self.expect(url.match(new RegExp(location)).length > 0).to.be.true;
                next()
            });
        });
    });
};