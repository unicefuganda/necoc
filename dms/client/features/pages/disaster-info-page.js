var DisasterInfoPage = function () {
    this.getDisasterData = function (key) {
        return element(by.binding('{[{ disasterInfo.' + key + ' }]}')).getText();
    };
};

module.exports = new DisasterInfoPage ();