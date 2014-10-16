module.exports = function () {

    var mapPage = require("../pages/map-page");

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
            return window.map.selectLayer(district);
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

    this.Then(/^I should see a messages bubble with (\d+) incoming messages$/, function (numberOfMessages, next) {
        this.expect(mapPage.messagesBubble.getText()).to.eventually.equal(numberOfMessages)
            .and.notify(next);
    });

    this.Then(/^I should see the map title as "([^"]*)"$/, function (mapTitle, next) {
        this.expect(mapPage.mapTitle.getText()).to.eventually.equal(mapTitle)
            .and.notify(next);
    });

    this.Then(/^I should see "([^"]*)" district with layer color "([^"]*)"$/, function (district, color, next) {
        var self = this;

        browser.executeScript(function (district) {
            return window.map.getHighlightedLayer()[district].getStyle().fillColor
        }, district).then(function (style) {
            self.expect(String(style)).to.equal(color);
            next();
        });
    });

    this.Then(/^I should see map legend displayed$/, function (next) {
        this.expect(mapPage.mapLegend.isDisplayed()).to.eventually.be.true
            .and.notify(next);
    });

};