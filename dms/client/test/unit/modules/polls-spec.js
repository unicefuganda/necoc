describe('dms.polls', function () {

    beforeEach(function () {
        module('dms.polls');
    });


    describe('NewPollController', function () {
        var initController,
            scope;

        beforeEach(function () {
            inject(function ($controller, $rootScope) {
                scope = $rootScope.$new();
                initController = function (isValid) {
                    scope.new_poll_form = { $valid: isValid};
                    $controller('NewPollController', {$scope: scope });
                };
            });
        });

        it('should not send poll given the form has errors', function () {
            initController(false);
            scope.sendPoll();
            expect(scope.hasErrors).toBeTruthy();
        });
    });


});