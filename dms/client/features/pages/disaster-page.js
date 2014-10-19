var AddDisasterModel = function () {

    this.description = element(by.model('disaster.description'));

    this.date = element(by.model('disaster.date'));

    this.saveButton = element(by.id('save-disaster-modal'));

    this.closeButton = element(by.id('close-disaster-modal'));

    this.selectInput = function (id, value) {
        return element(by.css('#' + id + ' .selectize-input')).click().then(function () {
            return element(by.cssContainingText('.selectize-dropdown-content .option', value)).click()
        });
    };

    this.get = function (errorId) {
        return element(by.css('#'+ errorId +' .text-danger')).getText();
    };
};

var DisasterPage = function () {
    var request = require('request');

    this.addDisasterButton = element(by.id('add-disaster'));

    this.sectionTitle = element.all(by.css('.sub-section-header .title')).get(0);

    this.addDisasterModal = new AddDisasterModel();

    this.backToDisastersButton = element(by.id('back-to-disasters-btn'));

    this.getDisasterData = function (row, key) {
        return element(by.repeater('disaster in disasters').row(row).column('{[{ disaster.' + key + ' }]}')).getText();
    };

    this.clickDisaster = function (row, key) {
        return element(by.repeater('disaster in disasters').row(row).column('{[{ disaster.' + key + ' }]}')).click();
    };

    this.associatedMessages = function (row, key) {
        return element(by.repeater('message in associatedMessages').row(row).column('{[{ message.' + key + ' }]}')).getText();
    };

    this.registerDisasterType = function (disasterType, next) {
        request.post('http://localhost:7999/api/v1/disaster-types/', {
            form: {
                name: disasterType
            }
        }, next);
    };
};

module.exports = new DisasterPage();