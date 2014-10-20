module.exports = function () {

    var pollsPage = require("../pages/polls-page"),
        pollResponsesPage = require("../pages/poll-responses-page"),
        poll_response = {phone: "+256775019449", text: "", time: "2014-02-13T02:00:00", relayer: 234,
            run: "23243"},
        poll_payload = {name: "Disaster", question: "How many disasters are in your area?", keyword: "",
            target_locations: []},
        poll_response_location;

    this.World = require("../support/world").World;

    this.Given(/^I have a poll and response with keyword "([^"]*)" in "([^"]*)"$/, function (keyword, location, next) {
        poll_response.text = 'NECOCPoll ' + keyword + ' It has been very slow.';
        poll_response_location = location;
        poll_payload.keyword = keyword;

        pollResponsesPage.createPollAndResponse(poll_response, poll_payload, location, next);
    });

    this.When(/^I visit the poll responses listing page$/, function (next) {
        browser.setLocation('/admin/poll-responses/');
        next();
    });

    var seePollMessages = function (next) {
        var self = this;

        pollResponsesPage.getPollResponseData(0, 'source')
            .then(function (source) {
                self.expect(source).to.equal('NECOC Volunteer (' + poll_response.phone + ')');
            })
            .then(function () {
                self.expect(pollResponsesPage.getPollResponseData(0, 'text')).to.eventually.equal(poll_response.text);
            })
            .then(function () {
                self.expect(pollResponsesPage.getPollResponseData(0, 'location')).to.eventually.equal(poll_response_location);
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
};