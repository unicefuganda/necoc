var MobileUsersModal = function () {
    this.title = element(by.id('mu-modal-title'));
    this.name = element(by.model('user.name'));
    this.phone = element(by.model('user.phone'));
    this.email = element(by.model('user.email'));
    this.username = element(by.model('user.username'));
    this.saveButton = element(by.id('save-mobile-user-modal'));
    this.closeButton = element(by.id('close-mobile-user-modal'));
    this.closeButton = element(by.id('close-mobile-user-modal'));

    this.clickCloseButton = function () {
        return this.closeButton.click();
    };

    this.clickSaveButton = function () {
        return this.saveButton.click();
    };

    this.selectLocation = function (className, location) {
        return element(by.css('.' + className + ' .selectize-input')).click().then(function () {
            browser.sleep(200);
            return element(by.cssContainingText('.' + className + ' .selectize-dropdown-content .option', location)).click()
        });
    };

    this.getPhoneFieldErrors = function (index) {
        var i = index || 0;
        return element.all(by.css('#phone-errors .text-danger')).get(i).getText();
    };

    this.getNameFieldErrors = function () {
        return element(by.css('#name-errors .text-danger')).getText();
    };

    this.getEmailFieldErrors = function (index) {
        var i = index || 0;
        return element.all(by.css('#email-errors .text-danger')).get(i).getText();
    };

    this.getDistrictFieldErrors = function () {
        return element(by.css('#district-errors .text-danger')).getText();
    };

    this.getSubcountyFieldErrors = function () {
        return element(by.css('#subcounty-errors .text-danger')).getText();
    };
};

var MobileUsersPage = function () {
    var request = require('request');
    this.createUserButton = element(by.id('create-user'));
    this.grantWebAccessToggle = element(by.id('grant-web-access-button'));
    this.createUserModal = new MobileUsersModal();

    this.clickUserRowByName = function (name, next) {
        element(by.cssContainingText('tr.ng-scope', name)).click().then(next);
    }

    this.clickCreateUserButton = function () {
        return this.createUserButton.click()
    };

    this.getMobileUsersData = function (index, key) {
        return element(by.repeater('user in users').row(index).column('{[{ ' + key + ' }]}')).getText();
    };
};

module.exports = new MobileUsersPage();