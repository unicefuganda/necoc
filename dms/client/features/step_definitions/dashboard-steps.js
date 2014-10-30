module.exports = function () {
    var dashboardPage = require("../pages/dashboard-page");

    this.World = require("../support/world").World;

    this.When(/^I click the messages panel chevron$/, function (next) {
        var animationLength = 1000;
        dashboardPage.sliderButton.click().then(function () {
            browser.sleep(animationLength).then(next);
        });
    });

    this.Then(/^I should see the messages panel (.*)/, function(stateText, next) {
        var state = stateText == 'open';
        this.expect(dashboardPage.messagesTitle.isDisplayed()).to.eventually.be[state.toString()]
            .and.notify(next);
    });
}