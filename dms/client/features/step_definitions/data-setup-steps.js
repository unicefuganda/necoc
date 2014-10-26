module.exports = function () {
    var dataSetupPage = require("../pages/data-setup-page");

    this.World = require("../support/world").World;

    this.When(/^I have "([^"]*)" district already registered$/, function (district, next) {
        dataSetupPage.registerDistrict(district, next);
    });

    this.Given(/^I have "([^"]*)" district and "([^"]*)" subcounty already registered$/, function (district, subcounty, next) {
        dataSetupPage.registerSubCounty(district, subcounty, next);
    });

    this.Given(/^I have a "([^"]*)" disaster in "([^"]*)" district, "([^"]*)" subcounty already registered$/,
        function (disaster, district, subcounty, next) {
            dataSetupPage.registerDisaster(disaster, district, subcounty, next);
        });

};