describe('dms.polls', function () {

    var httpMock,
        apiUrl;

    beforeEach(function () {
        module('dms.polls');

        inject(function ($httpBackend, Config) {
            httpMock = $httpBackend;
            apiUrl = Config.apiUrl;
        });
    });

    describe('NewPollController', function () {
        var initController,
            mockGrowl,
            scope,
            stubPoll,
            errorMessage = {
                keyword: [
                    "Keyword number must be unique"
                ]
            };

        beforeEach(function () {
            mockGrowl = jasmine.createSpyObj('growl', ['success']);
            stubPoll = { target_locations: "location-id-1,location-id-2", name: "Poll name", question: "Poll Question",
                keyword: 'PollKeyWord'};

            inject(function ($controller, $rootScope) {
                scope = $rootScope.$new();
                initController = function (isValid) {
                    scope.new_poll_form = { $valid: isValid, keyword: {$invalid: false}};
                    $controller('NewPollController', {$scope: scope, growl: mockGrowl });
                };
            });
        });

        it('should not send poll given the form has errors', function () {
            initController(false);
            scope.sendPoll();
            expect(scope.hasErrors).toBeTruthy();
        });

        it('should post the send poll given the poll form has no errors', function () {
            initController(true);
            scope.polls = [];
            scope.poll = stubPoll;
            scope.sendPoll();

            stubPoll.target_locations = ["location-id-1", "location-id-2"];
            httpMock.expectPOST(apiUrl + 'polls/', stubPoll).respond(stubPoll);
            expect(scope.saveStatus).toBeTruthy();
            expect(scope.successful).toBeFalsy();

            httpMock.flush();
            expect(scope.hasErrors).toBeFalsy();
            expect(scope.saveStatus).toBeFalsy();
            expect(scope.successful).toBeTruthy();
            expect(scope.poll).toBeNull();
            expect(scope.polls).toEqual([stubPoll]);
            expect(mockGrowl.success).toHaveBeenCalledWith('Poll successfully sent', { ttl: 3000 });
        });

        it('should add error to the scope given the post returns an error code', function () {
            httpMock.expectPOST(apiUrl + 'polls/').respond(400, errorMessage);
            initController(true);
            scope.poll = stubPoll;

            scope.sendPoll();
            httpMock.flush();

            expect(scope.new_poll_form.keyword.$invalid).toBeTruthy();
            expect(scope.hasErrors).toBeTruthy();
            expect(scope.saveStatus).toBeFalsy();
            expect(scope.errors).toEqual(errorMessage);
        });
    });

    describe('PollsController', function () {
        var scope,
            mockState,
            pollsStub = [
                {
                    id: 'poll_id',
                    name: "Number of disasters",
                    question: "How many disasters do you have in your area?",
                    keyword: "frvaa",
                    target_locations: [
                        "542a725f49aa87a205e5c279"
                    ]
                }
            ];

        beforeEach(function () {
            httpMock.when('GET', apiUrl + 'polls/').respond(pollsStub);

            inject(function ($controller, $rootScope) {
                scope = $rootScope.$new();
                mockState = jasmine.createSpyObj('mockState', ['go']);
                $controller('PollsController', {$scope: scope, $state: mockState});
            });
        });

        it('should retrieve polls from the endpoint and add them to the scope.', function () {
            httpMock.expectGET(apiUrl + 'polls/');
            httpMock.flush();
            expect(scope.polls).toEqual(pollsStub);
        });

        describe('ShowPollResponses', function () {
            it('should go to the corresponding poll responses page', function () {
                scope.showPollResponses(pollsStub);
                expect(mockState.go).toHaveBeenCalledWith('admin.poll-responses', {poll: pollsStub.id})
            });
        });

    });
});