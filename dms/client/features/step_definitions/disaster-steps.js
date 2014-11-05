module.exports = function () {
    var disasterPage = require("../pages/disaster-page"),
        dataSetUpPage = require("../pages/data-setup-page"),
        messagesPage = require("../pages/messages-page"),
        associatedMessage = messagesPage.messages[0],
        disaster = {};
    associatedMessage.formattedTime = messagesPage.formattedTime;

    this.Before(function (callback) {
        disaster = {};
        callback();
    });

    this.World = require("../support/world").World;

    this.Given(/^I have "([^"]*)" registered as a disaster type$/, function (disasterType, next) {
        dataSetUpPage.registerDisasterType(disasterType, next);
    });

    this.When(/^I navigate to "([^"]*)"$/, function (url, next) {
        browser.setLocation(url);
        next();
    });

    this.When(/^I click add disaster button$/, function (next) {
        disasterPage.addDisasterButton.click().then(function () {
            browser.sleep(500).then(next);
        });
    });

    this.When(/^I select the disaster type as "([^"]*)"$/, function (disasterType, next) {
        disaster.type = disasterType;
        disasterPage.addDisasterModal.selectInput("disaster-type-field", disasterType).then(next);
    });


    this.When(/^I select district as "([^"]*)"$/, function (district, next) {
        disaster.district = district;
        disasterPage.addDisasterModal.selectInput("district-field", district).then(next);
    });

    this.When(/^I select subcounty as "([^"]*)"$/, function (subcounties, next) {
        disaster.subcounties = subcounties;
        disasterPage.addDisasterModal.selectInput("subcounty-field", subcounties).then(next);
    });

    this.When(/^I enter disaster description as "([^"]*)"$/, function (description, next) {
        disaster.description = description;
        disasterPage.addDisasterModal.description.sendKeys(description).then(next);
    });

    this.When(/^I select disaster status as "([^"]*)"$/, function (status, next) {
        disaster.status = status;
        disasterPage.addDisasterModal.selectInput("status-field", status).then(next);
    });

    this.When(/^I enter the disaster type as "([^"]*)"$/, function (disasterType, next) {
        disaster.type = disasterType;
        disasterPage.addDisasterModal.enterInput("disaster-type-field", disasterType).then(next);
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
                if(disaster.subcounties) {
                    self.expect(disasterPage.getDisasterData(0, 'locations[0].parent.name')).to.eventually.equal(disaster.district);
                } else {
                    self.expect(disasterPage.getDisasterData(0, 'locations | joinNames | capitalize')).to.eventually.equal(disaster.district);
                }
            })
            .then(function () {
                if(disaster.subcounties) {
                    self.expect(disasterPage.getDisasterData(0, 'locations | joinNames | capitalize')).to.eventually.equal(disaster.subcounties);
                }
            })
            .then(function () {
                self.expect(disasterPage.getDisasterData(0, 'description')).to.eventually.equal(disaster.description);
            })
            .then(function () {
                self.expect(disasterPage.getDisasterData(0, 'date | duration')).to.eventually.exist;
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

    this.When(/^I click the disaster in "([^"]*)"$/, function (arg1, next) {
        disasterPage.clickDisaster(0, 'locations[0].parent.name').then(next);
    });

    this.Then(/^I should see the associated message$/, function (next) {
        var self = this;

        disasterPage.associatedMessages(0, 'source')
            .then(function (source) {
                self.expect(source).to.equal(associatedMessage.source + " (" + associatedMessage.phone + ")");
            })
            .then(function () {
                self.expect(disasterPage.associatedMessages(0, 'text')).to.eventually.equal(associatedMessage.text);
            })
            .then(function () {
                self.expect(disasterPage.associatedMessages(0, 'location')).to.eventually.equal('');
            })
            .then(function () {
                self.expect(disasterPage.associatedMessages(0, 'time | date:"MMM dd, yyyy - h:mma"')).to.eventually.equal(associatedMessage.formattedTime);
            })
            .then(next);
    });

    this.When(/^I click the back button$/, function (next) {
        disasterPage.backToDisastersButton.click().then(next);
    });

    this.Then(/^I should see the disasters listing page$/, function (next) {
        this.expect(disasterPage.sectionTitle.getText()).to.eventually.equal('Registered Disasters')
            .and.notify(next);
    });
};