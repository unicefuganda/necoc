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
            username: 'cage', first_name: 'nicolas',
            last_name: 'cage', email: 'nic@ol.as',
            phone_no: '235669502'};


        inject(function ($controller, $rootScope, $httpBackend, Config) {
            httpMock = $httpBackend;
            apiUrl = Config.apiUrl;
            $scope = $rootScope.$new();
            initController = function (userId) {
                var mockStateParams = {user: userId};
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
    });
});