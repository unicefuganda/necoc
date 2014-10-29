var NewPollModal = function () {
    this.title = element(by.id('new-poll-title'));

    this.pollNameField = element(by.model('poll.name'));

    this.pollQuestionField = element(by.model('poll.question'));

    this.pollKeywordField = element(by.model('poll.keyword'));

    this.sendPollsButton = element(by.id('send-poll-btn'));

    this.selectLocation = function (type_id, location) {
        return element(by.css('#'+type_id+'.selectize-input')).click().then(function () {
            return element(by.cssContainingText('.selectize-dropdown-content .option', location)).click()
        });
    };

    this.getFieldErrors = function (id, index) {
        return element.all(by.css('#' + id + ' .text-danger')).get(index).getText();
    };
};

var PollsPage = function () {
    var request = require('request');

    this.newPollButton = element(by.id('new-poll-btn'));

    this.newPollModal = new NewPollModal();

    this.notification = element(by.css('.growl-message'));

    this.sectionTitle = element.all(by.css('.sub-section-header .title')).get(0);

    this.getPollData = function (row, key) {
        return element(by.repeater('poll in polls').row(row).column('{[{ poll.' + key + ' }]}')).getText();
    };

    this.clickPoll = function (row, key) {
        return element(by.repeater('poll in polls').row(row).column('{[{ poll.' + key + ' }]}')).click();
    };

};

module.exports = new PollsPage();