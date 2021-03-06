module.exports = function () {

    var zoomLevels = {};

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

    this.When(/^I click "([^"]*)" subcounty in "([^"]*)" district$/, function (subcounty, district, next) {
        browser.executeScript(function () {
            return window.map.getZoom();
        }).then(function (zoomLevel) {
            zoomLevels.district = zoomLevel;
        }).then(function () {
            browser.executeScript(function (district, subcounty) {
                window.map.clickSubCounty(district, subcounty);
            }, district, subcounty);
        }).then(next);
    });

    this.Then(/^the map zooms into "([^"]*)"$/, function (subcounty, next) {
        var self = this;

        //Remove me once the UI changes when selecting a subcounty, giving us something to wait for
        browser.sleep(500);
        browser.executeScript(function () {
            return window.map.getZoom();
        }).then(function (zoomLevel) {
            self.expect(zoomLevel).to.be.above(zoomLevels.district);
        }).then(next);
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


    this.When(/^I click "([^"]*)" district$/, function (district, next) {
        browser.executeScript(function (district) {
            window.map.selectDistrict(district);
        }, district).then(next);
    });

    this.Then(/^I should see Uganda map zoomed into "([^"]*)" district$/, function (arg1, next) {
        var self = this,
            NORMAL_ZOOM_LEVEL = 7;

        browser.wait(mapPage.legend.title.isDisplayed).then(function () {
            browser.executeScript(function () {
                return window.map.getZoom();
            }).then(function (zoomLevel) {
                self.expect(zoomLevel.toString()).to.be.above(NORMAL_ZOOM_LEVEL);
                next();
            });
        });
    });

    this.Then(/^clicking "([^"]*)" subcounty zooms in$/, function (subcounty, next) {
        browser.executeScript(function (subcounty) {
            return window.map.selectSubcounty(district, subcounty);
        }, district).then(next);
    });

    this.Then(/^I should see a message cluster marker with (\d+) incoming messages$/, function (numberOfMessages, next) {
        this.expect(mapPage.messagesBubble.getText()).to.eventually.equal(numberOfMessages)
            .and.notify(next);
    });

    this.Then(/^I should see the map title as "([^"]*)"$/, function (mapTitle, next) {
        this.expect(browser.wait(mapPage.mapTitle.getText)).to.eventually.equal(mapTitle)
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
        this.expect(mapPage.legend.title.isDisplayed()).to.eventually.be.true
            .and.notify(next);
    });

    this.Then(/^I should see the legend title as "([^"]*)"$/, function (legendTitle, next) {
        this.expect(mapPage.legend.title.getText()).to.eventually.equal(legendTitle)
            .and.notify(next);
    });

    this.Then(/^I should see the legend labels as "([^"]*)"$/, function (labelList, next) {
        var labels = mapPage.legend.labels.map(function (element) {
            return element.getText()
        });
        this.expect(labels).to.eventually.eql(labelList.split(',')).and.notify(next);
    });

    this.When(/^I search for "([^"]*)" district$/, function (district, next) {
        mapPage.searchMapField.sendKeys(district).then(next);
    });

    this.When(/^I clear the text I entered in the district field$/, function (next) {
        mapPage.searchMapField.clear().then(next);
    });

    this.When(/^I navigate to map location "([^"]*)"$/, function (url, next) {
        browser.get('#' + url);
        this.expect(browser.wait(mapPage.legend.title.isDisplayed)).to.eventually.equal(true)
            .and.notify(next);
    });

    this.When(/^I zoom out to zoom level (\d+)$/, function (level, next) {
        browser.executeScript(function (level) {
            return window.map.setZoom(level);
        }, parseInt(level)).then(function () {
            self.expect(true).to.equal(true);
            next();
        });
    });

    this.Then(/^I should see a disaster cluster marker with (\d+) disasters$/, function (numberOfDisasters, next) {
        var self = this;
        this.waitForElement(by.css(".disasters-aggregate-marker-icon div"), function () {
            self.expect(mapPage.disastersBubble.getText()).to.eventually.equal(numberOfDisasters)
                .and.notify(next);
        });
    });

    this.Then(/^I should not see a disaster cluster marker$/, function (next) {
        var self = this;
        browser.isElementPresent(by.css('.disasters-aggregate-marker-icon div')).then(function (elementPresent) {
            self.expect(elementPresent).to.be.false;
            next();
        })
    });

    this.Then(/^I should not see a message cluster marker$/, function (next) {
        var self = this;
        browser.isElementPresent(by.css('.messages-aggregate-marker-icon div')).then(function (elementPresent) {
            self.expect(elementPresent).to.be.false;
            next();
        })
    });

    this.Then(/^I see should see (\d+) disasters bubble on the map$/, function (disasters, next) {
        var self = this;

        browser.executeScript(function () {
            return window.map.numberOfLayersIn('disaster_bubbles');
        }).then(function (number) {
            self.expect(number).to.equal(parseInt(disasters));
            next();
        });
    });

    this.When(/^I enter a from date filter as "([^"]*)"$/, function (fromDate, next) {
        mapPage.fromDateField.clear().then(function () {
            mapPage.fromDateField.sendKeys(fromDate);
        }).then(next);
    });

    this.When(/^I enter a to date filter as "([^"]*)"$/, function (toDate, next) {
        mapPage.toDateField.sendKeys(toDate).then(next);
    });

    this.Then(/^I should see map options panel on dashboard$/, function (next) {
        this.expect(mapPage.mapOptions.getText()).to.eventually.equal('Map Options')
            .and.notify(next);
    });

    this.Then(/^I should not see map options panel$/, function (next) {
        this.expect(mapPage.mapOptions.isDisplayed()).to.eventually.equal(false)
            .and.notify(next);
    });

    this.Then(/^I should see a cluster legend on the map$/, function (next) {
        var self = this;
        mapPage.clusterLegend.title.getText().then(function (title) {
            self.expect(title).to.equal('Clusters');
        }).then(function () {
            self.expect(mapPage.clusterLegend.labels.last().getText()).to.eventually.be.equal('Messages')
        }).then(function () {
            self.expect(mapPage.clusterLegend.labels.first().getText()).to.eventually.be.equal('Disasters');
        }).then(function () {
            self.expect(mapPage.clusterLegend.colors.last().isDisplayed()).to.eventually.be.true;
        }).then(function () {
            self.expect(mapPage.clusterLegend.colors.first().isDisplayed()).to.eventually.be.true;
        }).then(next);
    });

};