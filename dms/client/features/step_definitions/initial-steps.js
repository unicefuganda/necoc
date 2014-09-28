module.exports = function () {
    var dbUtils = require("../feature_utils/db-helpers.js")();

    this.World = require("../support/world").World;

    this.registerHandler('AfterFeatures', function (event, next) {
        next();
    });

    this.Before(function (callback) {
        browser.driver.manage().window().setSize(1280, 1024);
        callback();
    });

    this.After(function (callback) {
        dbUtils.dropDB(callback);
    });
};