var gulp = require('gulp');
var gutil = require('gulp-util');

var webpack = require('webpack-stream');
var sass = require('gulp-sass');

var shell = require('gulp-shell');
var argv = require('minimist')(process.argv.slice(2));

var dev = typeof argv.d !== 'undefined';

var collectstatic = 'python ../manage.py collectstatic -i node_modules --noinput';

gulp.task('sass', function () {
  return gulp.src('./sass/**/*.scss')
    .pipe(sass({ outputStyle: 'compressed' }).on('error', sass.logError))
    .pipe(gulp.dest('./static/css'));
});

gulp.task('webpack', function(callback) {
  return gulp.src('./sass/**/*.jsx')
    .pipe(webpack( require('./webpack.config.js') ))
    .pipe(gulp.dest('static/js/'));
});

gulp.task('static', ['webpack', 'sass'], shell.task(collectstatic));

gulp.task('default', ['webpack', 'sass', 'static']);
