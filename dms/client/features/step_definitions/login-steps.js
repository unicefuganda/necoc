module.exports = function () {
    var loginPage = require("../pages/login-page"),
        homePage = require("../pages/home-page");

    this.World = require("../support/world").World;

    this.Given(/^I am logged in as a NECOC admin$/, function (next) {
        var self = this;
        browser.get('/');
        browser.getCurrentUrl().then(function (url) {
            if (url.match(/login/)) {
                loginPage.username.sendKeys('test_user').then(function () {
                    loginPage.password.sendKeys('password')
                }).then(function () {
                    loginPage.signInButton.click()
                }).then(function () {
                    self.expect(browser.wait(homePage.title.getText)).to.eventually.equal('NECOC DMS')
                }).then(function () {
                    self.expect(browser.wait(homePage.loggedInUser.getText)).to.eventually.match(/test_user/)
                }).then(next)
            } else {
                self.expect(browser.wait(homePage.title.getText)).to.eventually.equal('NECOC DMS')
                    .and.notify(function () {
                        self.expect(browser.wait(homePage.loggedInUser.getText)).to.eventually.match(/test_user/)
                            .and.notify(next)
                    });
            }
        });
    });
};