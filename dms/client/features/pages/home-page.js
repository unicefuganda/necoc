var HomePage = function () {
    var request = require('request');

    this.adminPanel = element(by.id('admin-panel'));

    this.navigateToAdminPanel = function ()  {
        return this.adminPanel.click();
    }
};

module.exports = new HomePage();