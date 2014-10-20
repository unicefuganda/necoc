describe('dms.polls-response', function () {

    var httpMock,
        apiUrl,
        pollResponseStub;

    beforeEach(function () {
        module('dms.poll-responses');

        pollResponseStub = [
            {   phone: "+256775019449",
                text: "NECOCPoll keyword whatever",
                time: "2014-02-13T02:00:00",
                relayer: 234,
                run: "23243"
            }
        ];

        inject(function ($httpBackend, Config) {
            httpMock = $httpBackend;
            apiUrl = Config.apiUrl;
        });
    });

    describe('PollResponsesController', function () {
        var initController,
            state,
            stateMock,
            scope;

        beforeEach(function () {

            inject(function ($controller, $rootScope) {
                scope = $rootScope.$new();
                httpMock.when('GET', apiUrl + 'poll-responses/').respond(pollResponseStub);
                stateMock = jasmine.createSpyObj('stateMock', ['go']);

                initController = function (pollId) {
                    var mockStateParams = { poll: pollId };
                    $controller('PollResponsesController', {$scope: scope, $stateParams: mockStateParams,
                        $state: stateMock});
                };
            });
        });

        it('should retrieve responses from the poll and add them to the scope.', function () {
            var poll_id = 'poll_id';
            initController(poll_id);

            httpMock.expectGET(apiUrl + 'poll-responses/?poll=' + poll_id).respond(pollResponseStub);
            httpMock.flush();
            expect(scope.poll_responses).toEqual(pollResponseStub);
        });

        it('should retrieve all poll responses and add to scope when poll id not supplied.', function () {
            initController();

            httpMock.expectGET(apiUrl + 'poll-responses/');
            httpMock.flush();
            expect(scope.poll_responses).toEqual(pollResponseStub);
        });

        describe('backToPolls', function () {
            it('should go back to url "/admin/polls/" ', function () {
                initController();
                scope.backToPolls();
                expect(stateMock.go).toHaveBeenCalledWith('admin.polls');
            });
        });
    });
});