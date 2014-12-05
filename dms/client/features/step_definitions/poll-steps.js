module.exports = function () {

    var homePage = require("../pages/home-page"),
        pollsPage = require("../pages/polls-page"),
        poll = {};

    this.World = require("../support/world").World;

    this.sectionTitle = element.all(by.css('.sub-section-header .title')).get(0);

    this.Given(/^I navigate to polls page$/, function (next) {
        homePage.pollsTab.click().then(function() {
            browser.refresh().then(next);
        });
    });

    this.Given(/^I click new poll button$/, function (next) {
        var isModalPresent = pollsPage.newPollButton.click().then(function () {
            return browser.wait(pollsPage.newPollModal.title.isDisplayed)
        });

        this.expect(isModalPresent).to.eventually.be.true.and.notify(next);
    });

    this.Then(/^I should not see the new poll button/, function (next) {
        this.expect(pollsPage.newPollButton.isDisplayed()).to.eventually.be.false.and.notify(next);
    });

    this.Then(/^I should see the new poll button/, function (next) {
        this.expect(browser.wait(pollsPage.newPollButton.isDisplayed)).to.eventually.be.true.and.notify(next);
    });

    this.Given(/^I enter a poll name as "([^"]*)"$/, function (pollName, next) {
        poll.name = pollName;
        this.ignoreSync(false);
        pollsPage.newPollModal.pollNameField.sendKeys(pollName).then(next);
    });

    this.Given(/^I enter a poll question as "([^"]*)"$/, function (pollQuestion, next) {
        poll.question = pollQuestion;
        pollsPage.newPollModal.pollQuestionField.sendKeys(pollQuestion).then(next);
    });

    this.Given(/^I enter a poll keyword as "([^"]*)"$/, function (pollKeyword, next) {
        poll.keyword = pollKeyword;
        pollsPage.newPollModal.pollKeywordField.sendKeys(pollKeyword).then(next);
    });

    this.Given(/^I click the send poll button$/, function (next) {
        pollsPage.newPollModal.sendPollsButton.click().then(next);
    });

    this.Then(/^I should see poll successfully sent$/, function (next) {
        this.expect(pollsPage.newPollModal.title.isDisplayed()).to.eventually.be.false
            .and.notify(next)
    });

    this.Then(/^I should see the polls fields required error messages$/, function (next) {
        var self = this;

        pollsPage.newPollModal.getFieldErrors('poll-name-errors', 0)
            .then(function (error) {
                self.expect(error).to.be.equal('This field is required');
            })
            .then(function () {
                self.expect(pollsPage.newPollModal.getFieldErrors('poll-question-errors', 0)).to
                    .eventually.be.equal('This field is required');
            })
            .then(function () {
                self.expect(pollsPage.newPollModal.getFieldErrors('poll-keyword-errors', 0)).to
                    .eventually.be.equal('This field is required');
            })
            .then(function () {
                self.expect(pollsPage.newPollModal.getFieldErrors('poll-location-errors', 0)).to
                    .eventually.be.equal('This field is required');
            }).then(next);
    });

    this.Then(/^I enter a more than (\d+) characters "([^"]*)"$/, function (characters, field, next) {
        var string = Array(parseInt(characters) + 2).join("a");
        pollsPage.newPollModal[field].sendKeys(string).then(next);
    });

    this.Then(/^I should see character limit errors$/, function (next) {
        var self = this;

        pollsPage.newPollModal.getFieldErrors('poll-question-errors', 1)
            .then(function (error) {
                self.expect(error).to.be.equal('Please enter not more than 130 characters');
            })
            .then(function () {
                self.expect(pollsPage.newPollModal.getFieldErrors('poll-keyword-errors', 1)).to
                    .eventually.be.equal('Please enter not more than 10 characters');
            }).then(next);
    });

    this.Then(/^I should see key word must me unique$/, function (next) {
        var self = this;

        pollsPage.newPollModal.getFieldErrors('poll-keyword-errors', 2)
            .then(function (error) {
                self.expect(error).to.be.equal('Keyword must be unique');
            }).then(next);
    });

    this.Then(/^I should see the poll in the poll\-list$/, function (next) {
        var self = this;

        pollsPage.getPollData(0, 'name')
            .then(function (name) {
                self.expect(name).to.equal(poll.name);
            })
            .then(function () {
                self.expect(pollsPage.getPollData(0, 'question')).to.eventually.equal(poll.question);
            })
            .then(function () {
                self.expect(pollsPage.getPollData(0, 'created_at | date:"MMM dd, yyyy - h:mma"')).to.eventually.exist;
            }).then(next);
    });

    this.When(/^I click the poll in "([^"]*)"$/, function (arg1, next) {
        pollsPage.clickPoll(0, 'name').then(next);
    });

    this.Given(/^I select poll districts as "([^"]*)" and "([^"]*)"$/, function (district1, district2, next) {
        pollsPage.newPollModal.selectLocation('poll-districts-field', district1).then(function () {
            pollsPage.newPollModal.selectLocation('poll-districts-field', district2).then(next);
        });
    });

    this.Given(/^I select poll subcounties as "([^"]*)" and "([^"]*)"$/, function (subcounty1, subcounty2, next) {
        pollsPage.newPollModal.selectLocation('poll-subcounties-field', subcounty1).then(function () {
            pollsPage.newPollModal.selectLocation('poll-subcounties-field', subcounty2).then(next);
        });
    });


};