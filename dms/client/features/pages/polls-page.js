var NewPollModal = function () {
    this.title = element(by.id('new-poll-title'));

    this.pollNameField = element(by.model('poll.name'));

    this.pollQuestionField = element(by.model('poll.question'));

    this.pollKeywordField = element(by.model('poll.keyword'));

    this.sendPollsButton = element(by.id('send-poll-btn'));

    this.selectLocation = function (location) {
        return element(by.css('.selectize-input')).click().then(function () {
            return element(by.cssContainingText('.selectize-dropdown-content .option', location)).click()
        });
    };

    this.getFieldErrors = function (id, index) {
        return element.all(by.css('#'+id+ ' .text-danger')).get(index).getText();
    };
};

var PollsPage = function () {
    var request = require('request');

    this.newPollButton = element(by.id('new-poll-btn'));

    this.newPollModal = new NewPollModal();

    this.notification = element(by.css('.growl-message'));

    this.getPollData = function (row, key) {
        return element(by.repeater('poll in polls').row(row).column('{[{ poll.' + key + ' }]}')).getText();
    };
};

module.exports = new PollsPage();