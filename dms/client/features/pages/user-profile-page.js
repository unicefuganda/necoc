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
};

var UserProfilePage = function () {
    this.editUserButton = element(by.id('edit-user'));
    this.updateUserModal = new UpdateUsersModal();
    this.location = element(by.binding('{[{ [profile.location.parent, profile.location] | joinNames }]}'));
    this.userName = element(by.binding('profile.name'));
    this.userPhone = element(by.binding('profile.phone'));
    this.userEmail = element(by.binding('profile.email'));

    this.element_by_ng_binding = function(binding){
        return element(by.binding(binding)).getText();
    };
};

module.exports = new UserProfilePage();