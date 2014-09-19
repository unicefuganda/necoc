describe('dms.message', function () {
    var $scope;

    beforeEach(function () {
        module('dms.message');

        inject(function ($controller, $rootScope) {
            $scope = $rootScope.$new();
            $controller('MessageController', {$scope: $scope});
        });
    });

    it('should add title to the scope', function () {
        expect($scope.title).toEqual('Messages');
    });

});