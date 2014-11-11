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
}
;