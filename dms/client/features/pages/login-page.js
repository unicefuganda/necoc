var LoginPage = function () {
    this.username = element(by.id('id_username'));
    this.password = element(by.id('id_password'));
    this.signInButton = element(by.id('btn-login'));

    this.errorMessageFor = function (fieldName) {
        return element(by.id('id_' + fieldName))
            .element(by.xpath('..'))
            .element(by.css('.text-danger'))
            .getText();
    }
};

module.exports = new LoginPage();