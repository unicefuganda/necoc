describe('dms.geojson', function () {

    beforeEach(function () {
        module('dms.geojson');
    });

    describe('GeoJsonService', function () {

        var httpMock,
            districtsGeoJsonUrl,
            geoJsonService,
            districtsGeoJsonStub = {
                type: "Feature",
                geometry: {
                    type: "Point",
                    coordinates: [125.6, 10.1]
                },
                properties: {
                    name: "Dinagat Islands"
                }
            },
            subCountyGeoJsonStub = {
                type: "Feature",
                geometry: {
                    type: "Point",
                    coordinates: [125.6, 10.1]
                },
                properties: {
                    name: "Dinagat Islands"
                }
            };

        var subCountyUrlForGulu = 'http://178.62.69.21:8080/geoserver/wfs?service=WFS&version=1.0.0&' +
            'request=GetFeature&outputFormat=text/javascript&typeNames=subcounties:UGANDA_SUBCOUNTIES_2014' +
            '&propertyName=the_geom,DNAME2014,SNAME2014&filter=<Filter xmlns="http://www.opengis.net/ogc">' +
            '<PropertyIsEqualTo><PropertyName>DNAME2014</PropertyName><Literal>GULU</Literal></PropertyIsEqualTo>' +
            '</Filter>&format_options=callback:JSON_CALLBACK';


        beforeEach(function () {

            inject(function (GeoJsonService, Config, $httpBackend) {
                httpMock = $httpBackend;
                geoJsonService = GeoJsonService;
                districtsGeoJsonUrl = Config.districtsGeoJsonUrl;
                httpMock.when('GET', districtsGeoJsonUrl).respond(districtsGeoJsonStub);
                httpMock.when('JSONP', subCountyUrlForGulu).respond(subCountyGeoJsonStub);
            });
        });

        describe('GeoJsonService.district', function () {
            it('should fetch districts GeoJSON', function () {
                var obtainedGeoJson = geoJsonService.districts();
                httpMock.expectGET(districtsGeoJsonUrl);
                httpMock.flush();
                expect(obtainedGeoJson).toBeDefined();
            });
        });

        describe('GeoJsonService.subCounties', function () {
            it('should fetch subCounties GeoJSON', function () {
                var obtainedGeoJson = geoJsonService.subCounties('gulu');
                httpMock.expectJSONP(subCountyUrlForGulu);
                httpMock.flush();
                expect(obtainedGeoJson).toBeDefined();
            });
        });
    });
});