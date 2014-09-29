module.exports = function () {
    var dbUtils = require("../feature_utils/db-helpers.js")();

    this.World = require("../support/world").World;

    this.registerHandler('AfterFeatures', function (event, next) {
        next();
    });

    this.registerHandler('BeforeFeatures', function (event, next) {
        browser.driver.manage().window().setSize(1580, 1380);
        next();
    });

    this.After(function (callback) {
        dbUtils.dropDB(callback);
    });
};