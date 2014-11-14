module.exports = function () {
    var loginPage = require("../pages/login-page"),
        homePage = require("../pages/home-page"),
        dataSetUpPage = require("../pages/data-setup-page");

    this.World = require("../support/world").World;

    var login = function (self, username, password, next) {
        browser.get('/');
        browser.getCurrentUrl().then(function (url) {
            if (url.match(/login/)) {
                loginPage.username.sendKeys(username).then(function () {
                    loginPage.password.sendKeys(password)
                }).then(function () {
                    loginPage.signInButton.click()
                }).then(function () {
                    self.expect(browser.wait(homePage.title.getText)).to.eventually.equal('NECOC DMS')
                }).then(function () {
                    self.expect(browser.wait(homePage.loggedInUser.getText)).to.eventually.match(new RegExp(username))
                }).then(next)
            } else {
                self.expect(browser.wait(homePage.title.getText)).to.eventually.equal('NECOC DMS')
                    .and.notify(function () {
                        browser.wait(homePage.loggedInUser.getText).then(function (currentUsername) {
                            if(currentUsername != username) {
                                browser.get('/logout').then(function () {
                                    login(self, username, password, next)
                                });
                            }
                        })
                    });
            }
        });
    }

    this.Given(/^I am logged in as a NECOC admin$/, function (next) {
        var self = this;
        login(self, 'test_user', 'password', next);
    });

    this.Given(/^I log in with "([^"]*)" permission$/, function (permission, next) {
        var self = this,
            params = {
                username: "some_user",
                password: "test_user",
                email: "user@email.com",
                permission: permission
            };

        dataSetUpPage.createUserWithPermission(params, function () {
            login(self, params.username, params.password, next);
        });
    });

    this.When(/^I try to login in with username "([^"]*)" and password "([^"]*)"$/, function (username, password, next) {
        browser.get('/login').then(function () {
            loginPage.username.sendKeys(username).then(function () {
                loginPage.password.sendKeys(password)
            }).then(function () {
                loginPage.signInButton.click()
            }).then(next);
        });
    });

    this.Then(/^I should see "([^"]*)" error message "([^"]*)"$/, function (fieldName, message, next) {
        this.expect(loginPage.errorMessageFor(fieldName)).to.eventually.equal(message).and.notify(next);
    });

    this.When(/^I logout$/, function (next) {
        homePage.loggedInUser.click().then(function () {
            homePage.logoutLink.click().then(next);
        })
    });

    this.Given(/^I am logged out$/, function (next) {
        browser.get('/logout').then(next);
    });

    this.Then(/^I should be redirected to login page$/, function (next) {
        var self = this;
        browser.getCurrentUrl().then(function (url) {
            self.expect(url).to.match(/login/);
            next();
        });
    });

    this.Then(/^I should see "([^"]*)"$/, function (text, next) {
        this.expect(element(by.css('.alert-dismissable')).getText()).to.eventually.equal(text).and.notify(next);
    });
};