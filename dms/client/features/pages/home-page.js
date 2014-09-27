var HomePage = function () {
    var request = require('request');

    this.adminPanel = element(by.id('admin-panel'));

    this.navigateToAdminPanel = function ()  {
        this.adminPanel.click();
        return require('./mobile-users-page');
    }
};

module.exports = new HomePage();