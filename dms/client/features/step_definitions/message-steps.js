module.exports = function () {
    var homePage = require("../pages/home-page");

    this.World = require("../support/world").World;

    this.Given(/^I am logged in as a NECOC admin$/, function (next) {
        browser.get('/');
        next();
    });

    this.Then(/^I should see the NECOC dashboard title$/, function (next) {
        this.expect(homePage.title.getText()).to.eventually.equal('NECOC DMS')
            .and.notify(next);
    });

};