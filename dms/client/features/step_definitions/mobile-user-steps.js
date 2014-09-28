module.exports = function () {
    var homePage = require("../pages/home-page");
    var mobileUsersPage,
        user = {};

    this.World = require("../support/world").World;

    this.When(/^I navigate to the Admin Panel$/, function (next) {
        mobileUsersPage = homePage.navigateToAdminPanel();
        next();
    });

    this.When(/^I have "([^"]*)" district already registered$/, function (district, next) {
        mobileUsersPage.registerLocation(district);
        next();
    });

    this.When(/^I click the create new user button$/, function (next) {
        mobileUsersPage.clickCreateUserButton();
        next();
    });

    this.When(/^I enter my "([^"]*)" as "([^"]*)"$/, function (field, text, next) {
        user[field] = text;
        mobileUsersPage.createUserModal[field].sendKeys(text);
        next();
    });

    this.When(/^I select my "([^"]*)" as "([^"]*)"$/, function (arg1, location, next) {
        user.location = location;
        mobileUsersPage.createUserModal.selectLocation(location);
        next();
    });

    this.When(/^I click  save and close$/, function (next) {
        mobileUsersPage.createUserModal.clickSaveButton()
            .then(function () {
                mobileUsersPage.createUserModal.clickCloseButton();
                next();
            });
    });

    this.Then(/^I should see my details in mobile users table$/, function (next) {
        var self = this;

        mobileUsersPage.getMobileUsersData(0, 'name')
            .then(function (name) {
                self.expect(name).to.equal(user.name);
            })
            .then(function () {
                self.expect(mobileUsersPage.getMobileUsersData(0, 'phone')).to.eventually.equal(user.phone);
            })
            .then(function () {
                self.expect(mobileUsersPage.getMobileUsersData(0, 'email')).to.eventually.equal(user.email);
            })
            .then(function () {
                self.expect(mobileUsersPage.getMobileUsersData(0, 'location.name')).to.eventually.equal(user.location)
                    .and.notify(next);
            });

    });
};