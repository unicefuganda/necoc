var WorldConstructor = function (callback) {
    var world = {
        visit: function (url, callback) {
            this.browser.visit(url, callback)
        },
        expect: (function () {
            var chaiAsPromised = require('chai-as-promised');
            var chai = require('chai');
            chai.use(chaiAsPromised);
            return chai.expect;
        })()


    };

    callback(world);
};

exports.World = WorldConstructor;