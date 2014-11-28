var DisasterModal = function () {

    this.description = element(by.model('disaster.description'));

    this.date = element(by.model('disaster.date'));

    this.saveButton = element(by.id('save-disaster-modal'));

    this.closeButton = element(by.id('close-disaster-modal'));

    this.selectInput = function (id, value) {
        return element(by.css('#disasters-modal #' + id + ' .selectize-input')).click().then(function () {
            return element(by.cssContainingText('#disasters-modal #' + id + ' .selectize-dropdown-content .option', value)).click()
        });
    };

    this.enterInput = function (id, value) {
        return element(by.css('#disasters-modal #' + id + ' .selectize-input')).click()
            .then(function () {
                return element(by.css('#disasters-modal #' + id + ' .selectize-input input')).sendKeys(value)
            })
            .then(function () {
                return element(by.css('#disasters-modal #' + id + ' .selectize-dropdown-content .create')).click();
            });
    };

    this.get = function (errorId) {
        return element(by.css('#disasters-modal #' + errorId + ' .text-danger')).getText();
    };
};

var DisasterPage = function () {
    var request = require('request');

    this.addDisasterButton = element(by.id('add-disaster'));

    this.editDisasterButton = element(by.id('edit-disaster'));

    this.sectionTitle = element.all(by.css('.sub-section-header .title')).get(0);

    this.disasterModal = new DisasterModal();

    this.getDisasterData = function (row, key) {
        return element(by.repeater('disaster in disasters').row(row).column('{[{ disaster.' + key + ' }]}')).getText();
    };

    this.clickDisaster = function (row, key) {
        return element(by.repeater('disaster in disasters').row(row).column('{[{ disaster.' + key + ' }]}')).click();
    };

    this.associatedMessages = function (row, key) {
        return element(by.repeater('message in associatedMessages').row(row).column('{[{ message.' + key + ' }]}')).getText();
    };

    this.numberOfAssociatedMessages = function () {
        return element.all(by.repeater("message in associatedMessages")).count();
    };

    this.selectStatus = function (value) {
        return element(by.css('#status-filter .selectize-input')).click().then(function () {
            return element(by.cssContainingText('#status-filter .selectize-dropdown-content .option', value)).click()
        });
    };

    this.numberOfDistasters = function () {
        return element.all(by.repeater("disaster in disasters")).count();
    };

    this.dateField = function(field){
        return element(by.model('disasterFilter.' + field))};


};

module.exports = new DisasterPage();