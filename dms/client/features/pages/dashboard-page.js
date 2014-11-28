var DashboardPage = function () {
    this.messageSliderButton = element(by.className('message-panel-arrow'));
    this.summaryStatsSliderButton = element(by.className('summary-stats-panel-arrow'));
    this.messagesTitle = element(by.css('.message-container .sub-section-header'));
    this.getTextbyBinding = function(binding){
        return element(by.binding(binding)).getText();
    };

    this.selectInput = function (id, value) {
        return element(by.css('.filter #' + id + ' .selectize-input')).click().then(function () {
            return element(by.cssContainingText('.filter #' + id + ' .selectize-dropdown-content .option', value)).click()
        });
    };

    this.enterInput = function (id, value) {
        return element(by.css('.filter  #' + id + ' .selectize-input')).click()
            .then(function () {
                return element(by.css('.filter  #' + id + ' .selectize-input input')).sendKeys(value)
            })
            .then(function () {
                return element(by.css('.filter  #' + id + ' .selectize-dropdown-content .create')).click();
            });
    };
};

module.exports = new DashboardPage();