module.exports = function () {
    var dataSetupPage = require("../pages/data-setup-page");

    this.World = require("../support/world").World;

    this.When(/^I have "([^"]*)" district already registered$/, function (district, next) {
        dataSetupPage.registerDistrict(district, next);
    });

    this.Given(/^I have "([^"]*)" district and "([^"]*)" subcounty already registered$/, function (district, subcounty, next) {
        dataSetupPage.registerSubCounty(district, subcounty, next);
    });
};