var MobileUsersModal = function () {
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

    this.selectLocation = function (location) {
        element(by.className('selectize-input')).click().then(function () {
            element(by.cssContainingText('.selectize-dropdown-content .option', location)).click()
        });
    }
};

var MobileUsersPage = function () {
    this.createUserButton = element(by.id('create-user'));
    this.createUserModal = new MobileUsersModal();

    this.clickCreateUserButton = function () {
        this.createUserButton.click()
    };

    this.getMobileUsersData = function (row, key) {
        return element(by.repeater('user in users').row(row).column('{[{ user.' + key + ' }]}')).getText();
    };

    this.registerLocation = function (location) {
        require('request').post('http://localhost:7999/api/v1/locations/', {
            form: {
                name: location,
                type: "district"
            }
        });
    };
};

module.exports = new MobileUsersPage();