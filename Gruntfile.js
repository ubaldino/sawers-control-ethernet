module.exports = function(grunt) {
    require('load-grunt-tasks')(grunt);
    require('load-grunt-tasks')(grunt);

    grunt.initConfig({
        watch: {
            options: {
                livereload: true,
            },
            shell: {
                files:  [ '**','Control/*' ],
                tasks:  [ 'shell:target' ],
                options: {
                    spawn: false
                }
            }
        },
        shell: {
            options: {
                stderr: false,
                failOnError: false
            },
            target: {
                command: [
                    //'killall python2',
                    'python2 Control/main.py'
                ].join('&&')
            }
        }
    });

    grunt.registerTask('default', ['shell:target','watch']);
};

