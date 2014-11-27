var UpdateUsersModal = function () {
    this.name = element(by.model('user.name'));
    this.phone = element(by.model('user.phone'));
    this.email = element(by.model('user.email'));
    this.saveUserButton = element(by.id('save-mobile-user-modal'));

    this.clickSaveButton = function () {
        return this.saveUserButton.click();
    };

    this.selectLocation = function (className, location) {
        return element(by.css('.' + className + ' .selectize-input')).click().then(function () {
            browser.sleep(200);
            return element(by.cssContainingText('.' + className + ' .selectize-dropdown-content .option', location)).click()
        });
    };

    this.selectRole = function (role) {
        return element(by.css('.user-role .selectize-input')).click().then(function () {
            browser.sleep(200);
            return element(by.cssContainingText('.user-role .selectize-dropdown-content .option', role)).click()
        });
    };
};

var changePasswordModal = function () {
    this.old_password = element(by.model('user.old_password'));
    this.new_password = element(by.model('user.new_password'));
    this.confirm_password = element(by.model('user.confirm_password'));
    this.saveButton = element(by.id('save-user-password-modal'));

    this.clickSaveButton = function () {
        return this.saveButton.click();
    };
};


var resetPasswordModal = function () {
    this.resetButton = element(by.id('submit-reset-password-modal'));
};

var UserProfilePage = function () {
    this.editUserButton = element(by.id('edit-user'));
    this.updateUserModal = new UpdateUsersModal();
    this.changePasswordModal = new changePasswordModal();
    this.resetPasswordModal = new resetPasswordModal();
    this.location = element(by.binding('{[{ [profile.location.parent, profile.location] | joinNames }]}'));
    this.userName = element(by.binding('profile.name'));
    this.userPhone = element(by.binding('profile.phone'));
    this.userEmail = element(by.binding('profile.email'));
    this.changePasswordButton = element(by.id('change-password'));
    this.resetPasswordButton = element(by.id('reset-password'));
    this.role = element(by.binding('profile.group_name'));


    this.notification = element(by.css('.profile-toast .growl-message'));

    this.element_by_ng_binding = function(binding){
        return element(by.binding(binding)).getText();
    };

    this.getFieldErrors = function (id, index) {
        return element.all(by.css('#' + id + ' .text-danger')).get(index).getText();
    };

};

module.exports = new UserProfilePage();