var LoginPage = function () {
    this.username = element(by.id('id_username'));
    this.password = element(by.id('id_password'));
    this.signInButton = element(by.id('btn-login'));
};

module.exports = new LoginPage();