module.exports = function () {
    var dbUtils =  require("../feature_utils/db-helpers.js")();

    this.World = require("../support/world").World;

    this.registerHandler('AfterFeatures', function (event, next) {
        next();
    });

    this.After(function (callback) {
        dbUtils.dropDB(callback);
    });
};