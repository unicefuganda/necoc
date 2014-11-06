
function createPromiseSpy (name, methods) {
    var spy = jasmine.createSpyObj(name, methods);

    spy.when = function (method) {
        return {
            returnPromiseOf: function (result) {
                inject(function ($q) {
                    var deferred = $q.defer();
                    deferred.resolve(result);
                    spy[method].andReturn(deferred.promise)
                });
            }
        }
    }

    return spy;
};
