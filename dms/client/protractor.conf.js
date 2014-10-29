exports.config = {
    seleniumServerJar: 'node_modules/selenium-standalone/.selenium/2.44.0/server.jar',
    chromeDriver: 'node_modules/selenium-standalone/.selenium/2.44.0/chromedriver',

    framework: 'cucumber',

    specs: [
        'features/*.feature'
    ],

    capabilities: {
        'browserName': 'chrome'
    },

    baseUrl: 'http://localhost:7999',

    cucumberOpts: {
        require: 'features/step_definitions/',
        format: 'pretty'
//        tags: '@dev'
    }
};