module.exports = function () {
    this.World = require("../support/world").World;

    this.registerHandler('AfterFeatures', function (event, next) {
        next();
    });

};