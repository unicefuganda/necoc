module.exports = function () {
    var dbUtils = require("../feature_utils/db-helpers.js")();

    this.World = require("../support/world").World;

    this.registerHandler('BeforeFeatures', function (event, next) {
        browser.driver.manage().window().setSize(1280, 1024);
        next();
    });

    this.After(function (callback) {
        dbUtils.dropDB(callback);
    });
};