(function (module) {

	module.constant('Config', {
		baseUrl: window.location.origin,
        apiUrl: window.location.origin + "/api/v1/"
	});

})(angular.module('dms.config', []));