var MobileUsersModal = function () {
    this.title = element(by.id('mu-modal-title'));
    this.name = element(by.model('user.name'));
    this.phone = element(by.model('user.phone'));
    this.email = element(by.model('user.email'));
    this.saveButton = element(by.id('save-mobile-user-modal'));
    this.closeButton = element(by.id('close-mobile-user-modal'));

    this.clickCloseButton = function () {
        return this.closeButton.click();
    };

    this.clickSaveButton = function () {
        return this.saveButton.click();
    };

    this.selectLocation = function (location, next) {
        return element(by.css('.district .selectize-input')).click().then(function () {
            browser.sleep(200);
            return element(by.cssContainingText('.district .selectize-dropdown-content .option', location)).click()
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

    this.getLocationFieldErrors = function () {
        return element(by.css('#location-errors .text-danger')).getText();
    };
};

var MobileUsersPage = function () {
    var request = require('request');
    this.createUserButton = element(by.id('create-user'));
    this.createUserModal = new MobileUsersModal();

    this.clickCreateUserButton = function () {
        return this.createUserButton.click()
    };

    this.getMobileUsersData = function (row, key) {
        return element(by.repeater('user in users').row(row).column('{[{ user.' + key + ' }]}')).getText();
    };

    this.registerUserWith = function (email, phone, callback) {
        request.post('http://localhost:7999/api/v1/locations/', {
            form: {
                name: "Kampala",
                type: "district"
            }
        }, function (err, httpResponse, body) {
            request.post('http://localhost:7999/api/v1/mobile-users/', {
                form: {
                    name: "Timothy Akampa",
                    phone: phone,
                    location: JSON.parse(body).id,
                    email: email
                }
            }, function () {
                callback();
            });
        });
    }
};

module.exports = new MobileUsersPage();