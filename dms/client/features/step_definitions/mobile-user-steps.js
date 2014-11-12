module.exports = function () {
    var homePage = require("../pages/home-page"),
        dbUtils = require("../feature_utils/db-helpers.js")(),
        mobileUsersPage = require("../pages/mobile-users-page"),
        userProfilePage = require("../pages/user-profile-page"),
        dataSetUpPage = require("../pages/data-setup-page"),
        user = { location: {}};

    this.World = require("../support/world").World;

    this.When(/^I click the create new user button$/, function (next) {
        mobileUsersPage.clickCreateUserButton().then(function () {
            browser.sleep(500);
            this.expect(mobileUsersPage.createUserModal.title.getText()).to.eventually.equal('Add User')
                .and.notify(next);
        }.bind(this));
    });

    this.When(/^I enter my "([^"]*)" as "([^"]*)"$/, function (field, text, next) {
        user[field] = text;
        mobileUsersPage.createUserModal[field].sendKeys(text).then(next);
    });

    this.When(/^I select my "([^"]*)" as "([^"]*)"$/, function (className, location, next) {
        user.location[className] = location;
        mobileUsersPage.createUserModal.selectLocation(className, location).then(next);
    });

    this.When(/^I navigate to the users page$/, function (next) {
        homePage.usersTab.click().then(next);
    });

    this.When(/^I click  save and close$/, function (next) {
        mobileUsersPage.createUserModal.clickSaveButton()
            .then(function () {
                mobileUsersPage.createUserModal.clickCloseButton();
                next();
            });
    });

    this.Then(/^I should see my details in mobile users table in row ([0-9]+)$/, function (index, next) {
        var self = this;

        mobileUsersPage.getMobileUsersData(index, 'user.name')
            .then(function (name) {
                self.expect(name).to.equal(user.name);
            })
            .then(function () {
                self.expect(mobileUsersPage.getMobileUsersData(index, 'user.phone')).to.eventually.equal(user.phone);
            })
            .then(function () {
                self.expect(mobileUsersPage.getMobileUsersData(index, 'user.email')).to.eventually.equal(user.email);
            })
            .then(function () {
                self.expect(mobileUsersPage.getMobileUsersData(index, '[user.location.parent, user.location] | joinNames'))
                    .to.eventually.equal(user.location.district + ', ' + user.location.subcounty).and.notify(next);
            });

    });

    this.When(/^I click the save button$/, function (next) {
        mobileUsersPage.createUserModal.clickSaveButton().then(function () {
            browser.sleep(200);
            next();
        });
    });

    this.When(/^I choose to grant web access$/, function (next) {
        mobileUsersPage.grantWebAccessToggle.click().then(next);
    });

    this.Then(/^I should see fields required error messages$/, function (next) {
        var self = this;

        mobileUsersPage.createUserModal.getPhoneFieldErrors()
            .then(function (error) {
                self.expect(error).to.equal('This field is required');
            })
            .then(function () {
                self.expect(mobileUsersPage.createUserModal.getEmailFieldErrors()).to.eventually.be.empty;
            })
            .then(function () {
                self.expect(mobileUsersPage.createUserModal.getNameFieldErrors()).to.eventually.equal('This field is required');
            })
            .then(function () {
                self.expect(mobileUsersPage.createUserModal.getDistrictFieldErrors()).to.eventually.equal('This field is required')
                    .and.notify(next);
            });
    });

    this.When(/^I have a Mobile User with email "([^"]*)" and phone "([^"]*)"$/, function (email, phone, next) {
        dataSetUpPage.registerMobileUser(phone, 'Mukono', email, next);
    });

    this.Then(/^I should not see the field required error messages$/, function (next) {
        var self = this;

        mobileUsersPage.createUserModal.getPhoneFieldErrors()
            .then(function (error) {
                self.expect(error).to.be.empty;
            })
            .then(function () {
                self.expect(mobileUsersPage.createUserModal.getEmailFieldErrors()).to.eventually.be.empty;
            })
            .then(function () {
                self.expect(mobileUsersPage.createUserModal.getNameFieldErrors()).to.eventually.be.empty;
            })
            .then(function () {
                self.expect(mobileUsersPage.createUserModal.getDistrictFieldErrors()).to.eventually.be.empty
            })
            .then(function () {
                self.expect(mobileUsersPage.createUserModal.getSubcountyFieldErrors()).to.eventually.be.empty
            }).then(next);
    });

    this.Then(/^I should see other server\-side validation errors$/, function (next) {
        var self = this;
        mobileUsersPage.createUserModal.getPhoneFieldErrors(1)
            .then(function (error) {
                self.expect(error).to.be.equal('Phone must be unique');
            })
            .then(function () {
                self.expect(mobileUsersPage.createUserModal.getEmailFieldErrors(1)).to.eventually.equal('Email must be unique');
            })
            .then(function () {
                self.expect(mobileUsersPage.createUserModal.getNameFieldErrors()).to.eventually.be.empty;
            })
            .then(function () {
                self.expect(mobileUsersPage.createUserModal.getUsernameFieldErrors(0)).to.eventually.equal('Username must be unique');
            })
            .then(function () {
                self.expect(mobileUsersPage.createUserModal.getDistrictFieldErrors()).to.eventually.be.empty
                    .and.notify(next);
            });
    });

    this.When(/^I click "([^"]*)" in the mobile users table$/, function (name, next) {
        mobileUsersPage.clickUserRowByName(name, next);
    });

    this.Then(/^I should see my details in the profile page$/, function (next) {
        var self = this;
        browser.driver.navigate().refresh();
        userProfilePage.element_by_ng_binding('profile.name')
            .then(function (username) {
                self.expect(username).to.equal(user.name.toUpperCase());
            })
            .then(function () {
                self.expect(userProfilePage.element_by_ng_binding('profile.phone')).to.eventually.equal(user.phone);
            })
            .then(function () {
                self.expect(userProfilePage.element_by_ng_binding('profile.email')).to.eventually.equal(user.email)
                    .and.notify(next);
            })
    });

    this.Given(/^I have no users$/, function (next) {
        dbUtils.dropDB(function () {
            dataSetUpPage.createUser(next);
        });
    });
};