module.exports = function () {
    var homePage = require("../pages/home-page");
    var mobileUsersPage = require("../pages/mobile-users-page"),
        dataSetUpPage = require("../pages/data-setup-page"),
        user = { location: {}};

    this.World = require("../support/world").World;

    this.When(/^I click the create new user button$/, function (next) {
        mobileUsersPage.clickCreateUserButton().then(function () {
            browser.sleep(500);
            this.expect(mobileUsersPage.createUserModal.title.getText()).to.eventually.equal('Add Mobile User')
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

    this.Then(/^I should see my details in mobile users table$/, function (next) {
        var self = this;

        mobileUsersPage.getMobileUsersData(0, 'user.name')
            .then(function (name) {
                self.expect(name).to.equal(user.name);
            })
            .then(function () {
                self.expect(mobileUsersPage.getMobileUsersData(0, 'user.phone')).to.eventually.equal(user.phone);
            })
            .then(function () {
                self.expect(mobileUsersPage.getMobileUsersData(0, 'user.email')).to.eventually.equal(user.email);
            })
            .then(function () {
                self.expect(mobileUsersPage.getMobileUsersData(0, '[user.location.parent, user.location] | joinNames'))
                    .to.eventually.equal(user.location.district + ', ' + user.location.subcounty).and.notify(next);
            });

    });

    this.When(/^I click the save button$/, function (next) {
        mobileUsersPage.createUserModal.clickSaveButton().then(function () {
            browser.sleep(200);
            next();
        });
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
        dataSetUpPage.registerMobileUser(phone, 'Mukono', email,  next);
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
                self.expect(error).to.be.equal('Phone number must be unique');
            })
            .then(function () {
                self.expect(mobileUsersPage.createUserModal.getEmailFieldErrors(1)).to.eventually.equal('Email must be unique');
            })
            .then(function () {
                self.expect(mobileUsersPage.createUserModal.getNameFieldErrors()).to.eventually.be.empty;
            })
            .then(function () {
                self.expect(mobileUsersPage.createUserModal.getDistrictFieldErrors()).to.eventually.be.empty
                    .and.notify(next);
            });
    });
};