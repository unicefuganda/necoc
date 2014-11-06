module.exports = function () {
    var UserProfilePage = require("../pages/user-profile-page"),
        homePage = require("../pages/home-page");

    this.World = require("../support/world").World;

    this.When(/^I click on my profile link$/, function (next) {
        homePage.loggedInUser.click().then(function () {
            homePage.userProfileLink.click().then(next);
        })
    });


    this.Then(/^I should see my profile$/, function (next) {
        var self = this;

        self.expect(UserProfilePage.element_by_ng_binding('user.username')).to.eventually.equal('test_user').then(
            function () {
                self.expect(UserProfilePage.element_by_ng_binding('user.email')).to.eventually.equal('test_user@nothing.com').and.notify(next);
            }
        );
    });
};