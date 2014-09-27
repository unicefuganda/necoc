describe('dms.mobile-user', function () {
    var httpMock,
        scope,
        apiUrl;

    var responseStub = {
        "id": "54257147d6f45f6fc1eac346",
        "name": "NavaL",
        "phone": "+3434232324323",
        "location": {
            "created_at": "2014-09-25T22:34:18.218",
            "name": "hhjj",
            "id": "54246e3ad6f45f5de40b137d"
        },
        "email": ""
    };

    beforeEach(function () {
        module('dms.mobile-user');

        inject(function ($httpBackend, $rootScope, Config) {
            httpMock = $httpBackend;
            scope = $rootScope.$new();
            apiUrl = Config.apiUrl;
        });
    });

    describe('MobileUserController', function () {

        beforeEach(function () {
            inject(function ($controller) {
                httpMock.when('POST', apiUrl + 'mobile-users/').respond(responseStub);
                httpMock.when('GET', apiUrl + 'mobile-users/').respond([responseStub]);

                $controller('MobileUserController', {$scope: scope});
            })
        });

        it('should post the user to the api endpoint', function () {
            scope.saveUser();
            httpMock.expectPOST(apiUrl + 'mobile-users/');
            httpMock.flush();

            expect(scope.users).toEqual([responseStub, responseStub]);
        });

        it('should add existing users to the scope', function () {
            httpMock.expectGET(apiUrl + 'mobile-users/');
            httpMock.flush();

            expect(scope.users).toEqual([responseStub]);
        });
    });
});