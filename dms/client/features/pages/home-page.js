var HomePage = function () {
    var request = require('request');

    this.messagesTab = element(by.id('messages-tab'));
    this.usersTab = element(by.id('users-tab'));
};

module.exports = new HomePage();