module.exports = function () {
    var dashboardPage = require("../pages/dashboard-page");

    this.World = require("../support/world").World;

    this.When(/^I click the messages panel chevron$/, function (next) {
        var animationLength = 800;
        dashboardPage.sliderButton.click().then(function () {
            browser.sleep(animationLength).then(next);
        });
    });

    this.Then(/^I should see the messages panel open/, function(next) {
        var self = this;
        browser.sleep(1000).then(function () {
            self.expect(dashboardPage.messagesTitle.isDisplayed()).to.eventually.be.true
                .and.notify(next);
        });
    });

    this.Then(/^I should see the messages panel closed/, function(next) {
        var self = this;
        browser.sleep(1000).then(function () {
            self.expect(dashboardPage.messagesTitle.isDisplayed()).to.eventually.be.false
                .and.notify(next);
        });
    });

}