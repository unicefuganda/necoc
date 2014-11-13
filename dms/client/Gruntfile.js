module.exports = function (grunt) {

    require('load-grunt-tasks')(grunt);

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        karma: {
            unit: {
                configFile: 'karma.conf.js'
            }
        },

        protractor: {
            options: {
                configFile: 'protractor.conf.js',
                keepAlive: false
            },
            test: {}
        },

        run: {
            runserver: {
                cmd: '../../manage.py',
                args: [
                    'runserver',
                    '0.0.0.0:7999'
                ],
                options: {
                    wait: false,
                    quite: true
                }
            },
            createUserGroups: {
                cmd: '../../manage.py',
                args: ['create_user_groups',
                       'test_user'],
                options: {
                    wait: false,
                    quite: true
                }
            },
            createUser: {
                cmd: '../../manage.py',
                args: [
                    'create_super_user',
                    'test_user',
                    'password',
                    'test_user@nothing.com',
                    'Test User',
                    'Kampala',
                    '1234567890'
                ],
                options: {
                    wait: false,
                    quite: true
                }
            }
        }
    });

    grunt.registerTask('ut', function () {
        grunt.task.run('karma:unit');
    });

    grunt.registerTask('ft', function () {
        grunt.task.run('run:runserver');
        grunt.task.run('protractor');
    });

};