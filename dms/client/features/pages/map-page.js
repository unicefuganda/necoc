var MapPage = function () {
    this.mapTitle = element(by.css('.navbar-title a'));
    this.messagesBubble = element(by.css('.messages-aggregate-marker-icon div'));
    this.mapLegend = element(by.css('.info.legend'));
};

module.exports = new MapPage();