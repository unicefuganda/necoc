module.exports = function (grunt) {

    require('load-grunt-tasks')(grunt);

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        karma: {
            unit: {
                configFile: 'karma.conf.js'
            }
        }
    });


    grunt.registerTask('ut', function () {
       grunt.task.run('karma:unit');
    });
};