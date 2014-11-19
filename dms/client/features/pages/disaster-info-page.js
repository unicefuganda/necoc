var DisasterInfoPage = function () {
    this.getDisasterData = function (key) {
        return element(by.binding('{[{ disaster.' + key + ' }]}')).getText();
    };
};

module.exports = new DisasterInfoPage ();