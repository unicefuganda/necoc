var WorldConstructor = function (callback) {

    function wait(elementSelector, callback) {
        setTimeout(function () {
            browser.isElementPresent(elementSelector).then(function (state) {
                if (!state) {
                    wait(elementSelector, callback);
                } else {
                    callback(state);
                }
            });
        }, 100);
    }

    var world = {
        visit: function (url, callback) {
            this.browser.visit(url, callback)
        },
        expect: (function () {
            var chaiAsPromised = require('chai-as-promised');
            var chai = require('chai');
            chai.use(chaiAsPromised);
            return chai.expect;
        })(),
        ignoreSync: function (state) {
            ptor = protractor.getInstance();
            ptor.ignoreSynchronization = state;
        },
        waitForElement: function (elementSelector, callback) {
            wait(elementSelector, callback);
        }
    };

    callback(world);
};

exports.World = WorldConstructor;