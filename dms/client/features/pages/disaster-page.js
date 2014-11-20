var DisasterModel = function () {

    this.description = element(by.model('disaster.description'));

    this.date = element(by.model('disaster.date'));

    this.saveButton = element(by.id('save-disaster-modal'));

    this.closeButton = element(by.id('close-disaster-modal'));

    this.selectInput = function (id, value) {
        return element(by.css('#' + id + ' .selectize-input')).click().then(function () {
            return element(by.cssContainingText('.selectize-dropdown-content .option', value)).click()
        });
    };

    this.enterInput = function (id, value) {
        return element(by.css('#' + id + ' .selectize-input')).click()
            .then(function () {
                return element(by.css('#' + id + ' .selectize-input input')).sendKeys(value)
            })
            .then(function () {
                return element(by.css('.selectize-dropdown-content .create')).click();
            });
    };

    this.get = function (errorId) {
        return element(by.css('#' + errorId + ' .text-danger')).getText();
    };
};

var DisasterPage = function () {
    var request = require('request');

    this.addDisasterButton = element(by.id('add-disaster'));

    this.editDisasterButton = element(by.id('edit-disaster'));

    this.sectionTitle = element.all(by.css('.sub-section-header .title')).get(0);

    this.disasterModal = new DisasterModel();

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

};

module.exports = new DisasterPage();