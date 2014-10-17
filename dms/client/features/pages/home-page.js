var HomePage = function () {
    var request = require('request');

    this.messagesTab = element(by.id('messages-tab'));
    this.usersTab = element(by.id('users-tab'));
    this.pollsTab = element(by.id('polls-tab'));
};

module.exports = new HomePage();