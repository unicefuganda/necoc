var Legend  = function () {
    this.title = element(by.css('.info.legend .legend-title'));
    this.labels = element.all(by.css('.info.legend div i'));
};

var MapPage = function () {
    this.mapTitle = element(by.css('.navbar-title a'));
    this.messagesBubble = element(by.css('.messages-aggregate-marker-icon div'));
    this.disastersBubble = element(by.css('.disasters-aggregate-marker-icon div'));
    this.legend = new Legend();
    this.searchMapField = element(by.model('map.search'));
    this.fromDateField = element(by.model('filter.from'));
    this.toDateField = element(by.model('filter.to'));
    this.mapOptions = element(by.css('.filter h4'));
};

module.exports = new MapPage();