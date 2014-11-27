module.exports = function () {
    var userProfilePage = require("../pages/user-profile-page"),
        homePage = require("../pages/home-page"),
        user = {};

    this.World = require("../support/world").World;

    this.When(/^I click on my profile link$/, function (next) {
        homePage.loggedInUser.click().then(function () {
            homePage.userProfileLink.click().then(next);
        })
    });

    this.Then(/^I should see my updated profile$/, function (next) {
        var self = this;

        userProfilePage.userName.getText()
            .then(function (userName) {
                self.expect(userName).to.equal(user.name.toUpperCase());
            })
            .then(function () {
                self.expect(userProfilePage.userPhone.getText()).to.eventually.equal(user.phone);
            })
            .then(function () {
                self.expect(userProfilePage.userEmail.getText()).to.eventually.equal(user.email);
            })
            .then(function () {
                self.expect(userProfilePage.role.getText()).to.eventually.equal(user.role);
            })
            .then(function () {
                self.expect(userProfilePage.location.getText())
                    .to.eventually.equal(user.location.district + ', ' + user.location.subcounty);
            })
            .then(next);
    });

    this.When(/^I edit the user$/, function (next) {
        var self = this;
        userProfilePage.editUserButton.click().then(function () {
            self.expect(browser.wait(userProfilePage.updateUserModal.saveUserButton.isDisplayed)).to.eventually.be.true
                .and.notify(next);
        });
    });

    this.When(/^I save the updated user details$/, function (next) {
        userProfilePage.updateUserModal.clickSaveButton().then(next);
    });

    this.When(/^I update my "([^"]*)" as "([^"]*)"$/, function (field, text, next) {
        user[field] = text;
        userProfilePage.updateUserModal[field].clear().then(function () {
            userProfilePage.updateUserModal[field].sendKeys(text).then(next);
        });
    });

    this.When(/^I update by selecting my "([^"]*)" as "([^"]*)"$/, function (className, location, next) {
        user.location = user.location || {};
        user.location[className] = location;
        userProfilePage.updateUserModal.selectLocation(className, location).then(next);
    });

    this.When(/^I update by selecting my role as "([^"]*)"$/, function (role, next) {
        user.role = role
        userProfilePage.updateUserModal.selectRole(role).then(next);
    });

    this.When(/^I change my password$/, function (next) {
        var self = this;
        userProfilePage.changePasswordButton.click().then(function () {
            self.expect(browser.wait(userProfilePage.changePasswordModal.saveButton.isDisplayed)).to.eventually.be.true
                .and.notify(next);
        });
    });

    this.When(/^I input my "([^"]*)" as "([^"]*)"$/, function (field, value, next) {
        userProfilePage.changePasswordModal[field].clear().then(function () {
            userProfilePage.changePasswordModal[field].sendKeys(value).then(next);
        });
    });

    this.When(/^I proceed to click the save button$/, function (next) {
        userProfilePage.changePasswordModal.clickSaveButton().then(next);
    });

    this.Then(/^I should see password successfully updated message$/, function (next) {
        var self = this;
        self.ignoreSync(true);

        browser.wait(userProfilePage.notification.getText).then(function (text) {
            self.expect(text).to.equal('Password successfully changed');
            next();
        });
    });

    this.Then(/^I should be logged In$/, function (next) {
        this.expect(homePage.loggedInUser.isDisplayed()).to.eventually.be.true
            .and.notify(next);
    });

    this.Then(/^I see "([^"]*)" number (\d+) error message "([^"]*)"$/, function (fieldId, number, error, next) {
        this.expect(userProfilePage.getFieldErrors(fieldId + '-errors', number)).to
            .eventually.be.equal(error).and.notify(next);
    });

    this.When(/^I reset the password$/, function (next) {
        userProfilePage.resetPasswordButton.click().then(function () {
            browser.wait(userProfilePage.resetPasswordModal.resetButton.isDisplayed).then(function () {
                userProfilePage.resetPasswordModal.resetButton.click().then(next);
            })
        })
    });

    this.Then(/^I should see the change password button$/, function (next) {
        this.expect(userProfilePage.changePasswordButton.isDisplayed()).to.eventually.be.true
            .and.notify(next)
    });

    this.Then(/^I should not see the change password button$/, function (next) {
        this.expect(userProfilePage.changePasswordButton.isDisplayed()).to.eventually.be.false
            .and.notify(next)
    });

    this.Then(/^I should see the reset password button$/, function (next) {
        this.expect(userProfilePage.resetPasswordButton.isDisplayed()).to.eventually.be.true
            .and.notify(next)
    });

    this.Then(/^I should not see the reset password button$/, function (next) {
        this.expect(userProfilePage.resetPasswordButton.isDisplayed()).to.eventually.be.false
            .and.notify(next)
    });
};