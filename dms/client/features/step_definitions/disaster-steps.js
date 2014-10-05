module.exports = function () {
    var disasterPage = require("../pages/disaster-page"),
        disaster = {};

    this.World = require("../support/world").World;

    this.Given(/^I have "([^"]*)" registered as a disaster type$/, function (disasterType, next) {
        disasterPage.registerDisasterType(disasterType, next);
    });

    this.When(/^I navigate to "([^"]*)"$/, function (url, next) {
        browser.setLocation(url);
        next();
    });

    this.When(/^I click add disaster button$/, function (next) {
        disasterPage.addDisasterButton.click().then(function () {
            browser.sleep(500);
            next();
        });
    });

    this.When(/^I select the disaster type as "([^"]*)"$/, function (disasterType, next) {
        disaster.type = disasterType
        disasterPage.addDisasterModal.selectInput("disaster-type-field", disasterType).then(next);
    });


    this.When(/^I select district as "([^"]*)"$/, function (district, next) {
        disaster.district = district;
        disasterPage.addDisasterModal.selectInput("district-field", district).then(next);
    });

    this.When(/^I enter disaster description as "([^"]*)"$/, function (description, next) {
        disaster.description = description;
        disasterPage.addDisasterModal.description.sendKeys(description).then(next);
    });

    this.When(/^I select disaster status as "([^"]*)"$/, function (status, next) {
        disaster.status = status;
        disasterPage.addDisasterModal.selectInput("status-field", status).then(next);
    });

    this.When(/^I enter disaster date as "([^"]*)"$/, function (date, next) {
        disaster.date = date;
        disasterPage.addDisasterModal.date.sendKeys(date).then(next);
    });

    this.When(/^I click save and close$/, function (next) {
        disasterPage.addDisasterModal.saveButton.click().then(function () {
            return disasterPage.addDisasterModal.closeButton.click();
        }).then(next);
    });

    this.Then(/^I should see the disaster in the disasters table$/, function (next) {
        var self = this;

        disasterPage.getDisasterData(0, 'name.name')
            .then(function (name) {
                self.expect(name).to.equal(disaster.type);
            })
            .then(function () {
                self.expect(disasterPage.getDisasterData(0, 'location.name')).to.eventually.equal(disaster.district);
            })
            .then(function () {
                self.expect(disasterPage.getDisasterData(0, 'description')).to.eventually.equal(disaster.description);
            })
            .then(function () {
                self.expect(disasterPage.getDisasterData(0, 'date | duration')).to.eventually.exit
            })
            .then(function () {
                self.expect(disasterPage.getDisasterData(0, 'status')).to.eventually.equal(disaster.status)
                    .and.notify(next);
            });
    });

    this.When(/^I click save$/, function (next) {
        disasterPage.addDisasterModal.saveButton.click().then(next);
    });

    this.Then(/^I should see required fields error messages$/, function (next) {
        var self = this;

         disasterPage.addDisasterModal.get('name-errors')
            .then(function (error) {
                self.expect(error).to.equal('This field is required');
            })
            .then(function () {
                self.expect(disasterPage.addDisasterModal.get('district-errors')).to.eventually.be.equal('This field is required');
            })
            .then(function () {
                self.expect(disasterPage.addDisasterModal.get('description-errors')).to.eventually.empty;
            })
            .then(function () {
                self.expect(disasterPage.addDisasterModal.get('status-errors')).to.eventually.equal('This field is required');
            })
            .then(function () {
                self.expect(disasterPage.addDisasterModal.get('date-errors')).to.eventually.equal('This field is required')
                    .and.notify(next);
            });
    });
};