module.exports = function () {
    var dbUtils = require("../feature_utils/db-helpers.js")(),
        dataSetUpPage = require("../pages/data-setup-page");

    this.World = require("../support/world").World;

    this.registerHandler('BeforeFeatures', function (event, next) {
        browser.driver.manage().window().setSize(1280, 1024);
        dbUtils.dropDB(function () {
            dataSetUpPage.createUserGroup(function () {
                dataSetUpPage.createUser(next);
            });
        });
    });

    this.After(function (callback) {
        dbUtils.dropCollections(callback);
    });

    this.Before(function (callback) {
        this.ignoreSync(false);
        callback();
    });

    this.registerHandler('AfterFeatures', function (event, callback) {
        dbUtils.dropDB(callback);
    });

};