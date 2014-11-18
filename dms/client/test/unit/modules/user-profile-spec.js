describe('dms.user-profile', function () {
    var $scope;
    var httpMock;
    var userStub;
    var apiUrl;
    var initController;

    beforeEach(function () {
        module('dms.user-profile');
        module('dms.config');

        userStub = {
            username: 'cage',
            first_name: 'nicolas',
            last_name: 'cage',
            email: 'nic@ol.as',
            phone_no: '235669502',
            "location": {
                "name": "LWAMATA",
                "parent": {
                    "name": "KIBOGA",
                    "id": "54590707d6f45f80b7eb6c53"
                },
                "id": "54590707d6f45f80b7eb6c56"
            }
        };


        inject(function ($controller, $rootScope, $httpBackend, Config) {
            httpMock = $httpBackend;
            apiUrl = Config.apiUrl;
            $scope = $rootScope.$new();
            initController = function (userId, valid) {
                var mockStateParams = {user: userId};
                $scope.user_form = {$valid: valid || false, phone: { $invalid: false } };
                $controller('UserProfileController', {$scope: $scope, $stateParams: mockStateParams});
            };
        });

    });

    it('should retrieve user profile from api endpoint and add them to the scope.', function () {
        var userId = 'user_id';
        initController(userId);
        httpMock.expectGET(apiUrl + 'mobile-users/' + userId + '/').respond(userStub);
        httpMock.flush();
        expect($scope.user).toEqual(userStub);
        expect($scope.profile).toEqual(userStub);
    });

    it('should set onEdit to true', function () {
        var userId = 'user_id';
        initController(userId);
        httpMock.expectGET(apiUrl + 'mobile-users/' + userId + '/').respond(userStub);
        httpMock.flush();
        expect($scope.onEdit).toBeTruthy();
    });

    it('should set profileImageSrc', function () {
        var userId = 'user_id';
        initController(userId);
        userStub.id = '12345678'
        httpMock.expectGET(apiUrl + 'mobile-users/' + userId + '/').respond(userStub);
        httpMock.flush();
        expect($scope.profileImageSrc).toMatch(/\/api\/v1\/photo\/12345678\?decache=/);
    });
});