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

        var subCountyUrlForGulu = 'http://ec2-54-218-182-219.us-west-2.compute.amazonaws.com/geoserver/geonode/ows?' +
                    'service=WFS&version=1.0.0&request=GetFeature&outputFormat=json' +
                    '&typeName=geonode:subcounties_2011_0005&propertyName=the_geom,DNAME_2010,SNAME_2010' +
                    '&filter=<Filter xmlns="http://www.opengis.net/ogc"><PropertyIsEqualTo>' +
                    '<PropertyName>DNAME_2010</PropertyName><Literal>GULU</Literal></PropertyIsEqualTo></Filter>' +
                    '&callback=JSON_CALLBACK';


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