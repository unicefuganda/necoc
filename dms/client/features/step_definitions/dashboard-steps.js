module.exports = function () {
    var dashboardPage = require("../pages/dashboard-page"),
        disasterPage = require("../pages/disaster-page");

    this.World = require("../support/world").World;

    this.When(/^I click the messages panel chevron$/, function (next) {
        var animationLength = 800;
        dashboardPage.messageSliderButton.click().then(function () {
            browser.sleep(animationLength).then(next);
        });
    });

    this.Then(/^I should see the messages panel open/, function (next) {
        var self = this;
        browser.sleep(1000).then(function () {
            self.expect(dashboardPage.messagesTitle.isDisplayed()).to.eventually.be.true
                .and.notify(next);
        });
    });

    this.Then(/^I should see the messages panel closed/, function (next) {
        var self = this;
        browser.sleep(1000).then(function () {
            self.expect(dashboardPage.messagesTitle.isDisplayed()).to.eventually.be.false
                .and.notify(next);
        });
    });

    this.When(/^I add the disaster type as "([^"]*)"$/, function (disasterType, next) {
        disasterPage.addDisasterModal.enterInput("dashboard-disaster-type-field", disasterType).then(next);
    });

    this.When(/^I select in the dashboard the disaster type as "([^"]*)"$/, function (disasterType, next) {
        disasterPage.addDisasterModal.selectInput("dashboard-disaster-type-field", disasterType).then(next);
    });

    this.When(/^I click the stats summary panel chevron$/, function (next) {
        var animationLength = 800;
        dashboardPage.summaryStatsSliderButton.click().then(function () {
            browser.sleep(animationLength).then(next);
        });
    });

    var seeInSummaryStats = function (self, locationName, disasterCount, affectedAreas, subLocation, next) {

        self.expect(dashboardPage.getTextbyBinding('locationTitles.name')).to.eventually.equal(locationName)
            .then(function () {
                self.expect(dashboardPage.getTextbyBinding('stats.disasters.count')).to.eventually.equal(disasterCount)
            })
            .then(function () {
                self.expect(dashboardPage.getTextbyBinding('stats.disasters.affected')).to.eventually.equal(affectedAreas)
            })
            .then(function () {
                self.expect(dashboardPage.getTextbyBinding('locationTitles.subLocation')).to.eventually.equal(subLocation)
            })
            .then(next);
    };

    this.Then(/^I should see the disaster stats$/, function (next) {
        seeInSummaryStats(this, 'Uganda', '1', '1', 'Districts', next);
    });

    this.Then(/^I should see in "([^"]*)" district the disaster stats$/, function (districtName, next) {
        seeInSummaryStats(this, districtName.toUpperCase() + ' District', '1', '1', 'Subcounties', next);
    });

    this.Then(/^I should see in goma the disaster stats$/, function (next) {
        seeInSummaryStats(this, 'GOMA Subcounty', '1', '1', 'Subcounty', next);
    });


    this.Then(/^I should see in "([^"]*)" district zero disaster stats$/, function (districtName, next) {
        seeInSummaryStats(this, districtName.toUpperCase() + ' District', '0', '0', 'Subcounties', next);
    });

};