var PollResponsesPage = function () {
    var request = require('request');

    this.getPollResponseData = function (row, key) {
        return element(by.repeater('poll_response in poll_responses').row(row).column('{[{ poll_response.' + key + ' }]}')).getText();
    };

    this.title = element(by.css('.sub-section-header .title'));

    this.backToPollsPageButton = element(by.id('back-to-polls-btn'));

    this.exportPollResponseButton = function(pollId) {
       return element(by.css('a[href="http://localhost:7999/export/poll-responses/' + pollId + '/"]'));
    };

};

module.exports = new PollResponsesPage();