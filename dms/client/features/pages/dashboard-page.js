var DashboardPage = function () {
    this.messageSliderButton = element(by.className('message-panel-arrow'));
    this.summaryStatsSliderButton = element(by.className('summary-stats-panel-arrow'));
    this.messagesTitle = element(by.css('.message-container .sub-section-header'));
    this.getTextbyBinding = function(binding){
        return element(by.binding(binding)).getText();
    }
};

module.exports = new DashboardPage();