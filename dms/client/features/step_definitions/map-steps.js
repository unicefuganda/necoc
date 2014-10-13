module.exports = function () {

    this.World = require("../support/world").World;

    this.Then(/^I should see a map of Uganda centered at latitude "([^"]*)" and longitude "([^"]*)"$/,
        function (latitude, longitude, next) {
            var self = this;

            browser.executeScript(function () {
                return window.map.getCenter();
            }).then(function (center) {
                self.expect(center.lat.toString()).to.equal(latitude);
                self.expect(center.lng.toString()).to.equal(longitude);
                next();
            });
        });

    this.Then(/^I should see a map of Uganda zoomed at level "([^"]*)"$/, function (zoom, next) {
        var self = this;

        browser.executeScript(function () {
            return window.map.getZoom();
        }).then(function (zoomLevel) {
            self.expect(zoomLevel.toString()).to.equal(zoom);
            next();
        });
    });

    this.When(/^hover over "([^"]*)"$/, function (district, next) {
        browser.executeScript(function (district) {
            return window.map.highlightLayer(district);
        }, district).then(next);
    });

    this.Then(/^"([^"]*)" should be highlighted$/, function (district, next) {
        var self = this;

        browser.executeScript(function () {
            return window.map.getHighlightedLayer();
        }).then(function (districtLayer) {
            self.expect(Object.keys(districtLayer)[0]).to.equal(district.toLowerCase());
            next();
        })
    });


    this.When(/^click "([^"]*)" district$/, function (district, next) {
        browser.executeScript(function (district) {
            return window.map.clickLayer(district);
        }, district).then(next);
    });

    this.Then(/^I should see Uganda map zoomed into "([^"]*)" district$/, function (arg1, next) {
        var self = this,
            NORMAL_ZOOM_LEVEL = 7;

        browser.sleep(500);
        browser.executeScript(function () {
            return window.map.getZoom();
        }).then(function (zoomLevel) {
            self.expect(zoomLevel.toString()).to.be.above(NORMAL_ZOOM_LEVEL);
            next();
        });
    });

};