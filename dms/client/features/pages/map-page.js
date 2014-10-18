var MapPage = function () {
    this.mapTitle = element(by.css('.navbar-title a'));
    this.messagesBubble = element(by.css('.messages-aggregate-marker-icon div'));
    this.mapLegend = element(by.css('.info.legend'));
    this.searchMapField = element(by.model('map.search'))
};

module.exports = new MapPage();