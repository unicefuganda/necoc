module.exports = function () {

    var pollsPage = require("../pages/polls-page"),
        pollResponsesPage = require("../pages/poll-responses-page"),
        dataSetupPage = require("../pages/data-setup-page"),
        pollId,
        pollResponseAttr = {};

    this.World = require("../support/world").World;

    this.Given(/^I have a poll and response with keyword "([^"]*)" in "([^"]*)"$/, function (keyword, location, next) {
        pollResponseAttr.text = 'NECOCPoll ' + keyword + ' It has been very slow.';
        pollResponseAttr.location = location;
        pollResponseAttr.keyword = keyword;
        pollResponseAttr.phone = '+234567';

        var callback = function(poll){
            pollId=poll.id;
            next();
        };

        dataSetupPage.createPollAndResponseFrom(pollResponseAttr, callback);
    });

    this.When(/^I visit the poll responses listing page$/, function (next) {
        browser.setLocation('/admin/poll-responses/');
        next();
    });

    var seePollMessages = function (next) {
        var self = this;

        pollResponsesPage.getPollResponseData(0, 'source')
            .then(function (source) {
                self.expect(source).to.equal('NECOC Volunteer (' + pollResponseAttr.phone + ')');
            })
            .then(function () {
                self.expect(pollResponsesPage.getPollResponseData(0, 'text')).to.eventually.equal(pollResponseAttr.text);
            })
            .then(function () {
                self.expect(pollResponsesPage.getPollResponseData(0, 'location')).to.eventually.equal(pollResponseAttr.location);
            })
            .then(function () {
                self.expect(pollResponsesPage.getPollResponseData(0, 'time | date:"MMM dd, yyyy - h:mma"')).to.eventually.exist;
            }).then(next);
    };

    this.Then(/^I should see my poll response$/, seePollMessages);

    this.When(/^I click the poll in "([^"]*)"$/, function (arg1, next) {
        pollsPage.clickPoll(0, 'name').then(next);
    });

    this.Then(/^I should see the associated poll responses$/, seePollMessages);

    this.When(/^I click the poll page back button$/, function (next) {
        pollResponsesPage.backToPollsPageButton.click().then(next);
    });

    this.Then(/^I should see the poll listing page$/, function (next) {
        var self = this;
        self.expect(pollsPage.sectionTitle.getText()).to.eventually.equal('All Polls')
            .then(function () {
                self.expect(pollsPage.getPollData(0, 'number_of_responses')).to.eventually.equal('1');
            }).
            then(next);
    });

    this.Then(/^I should see the export poll button$/, function (next) {
        this.expect(pollResponsesPage.exportPollResponseButton(pollId).isDisplayed()).to.eventually.be.true.and.notify(next);
    });

};