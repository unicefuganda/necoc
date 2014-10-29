var DashboardPage = function () {
    this.sliderButton = element(by.className('back-arrow'));
    this.messagesTitle = element(by.css('.message-container .sub-section-header'));
};

module.exports = new DashboardPage();