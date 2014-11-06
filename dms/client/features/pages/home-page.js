var HomePage = function () {
    var request = require('request');

    this.messagesTab = element(by.id('messages-tab'));
    this.usersTab = element(by.id('users-tab'));
    this.pollsTab = element(by.id('polls-tab'));
    this.title =  element(by.css('.sidebar .navbar-brand .title'));
    this.loggedInUser =  element(by.id('logged-in-user'));
    this.logoutLink = element(by.css('a[href="/logout"]'));
    this.userProfileLink = element(by.id('user_profile_link'));
};

module.exports = new HomePage();