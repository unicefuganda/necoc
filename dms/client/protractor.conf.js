exports.config = {
    seleniumServerJar: 'node_modules/selenium-standalone/.selenium/2.43.1/server.jar',
    chromeDriver: 'node_modules/selenium-standalone/.selenium/2.43.1/chromedriver',

    framework: 'cucumber',

    specs: [
        'features/*.feature'
    ],

    capabilities: {
        'browserName': 'phantomjs'
    },

    baseUrl: 'http://localhost:7999',

    cucumberOpts: {
        require: 'features/step_definitions/',
        format: 'pretty'
        // tags: '@dev'
    }
};