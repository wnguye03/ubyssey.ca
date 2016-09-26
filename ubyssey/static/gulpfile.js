var gulp = require('gulp');
var gutil = require('gulp-util');
var clean = require('gulp-clean');

var webpack = require('webpack-stream');
var sass = require('gulp-sass');

var argv = require('minimist')(process.argv.slice(2));

var dev = typeof argv.d !== 'undefined';

gulp.task('sass', function () {
  return gulp.src('./src/styles/**/*.scss')
    .pipe(sass({ outputStyle: 'compressed' }).on('error', sass.logError))
    .pipe(gulp.dest('./dist/css/'));
});

gulp.task('webpack', function() {
  return gulp.src('./src/js/**/*.jsx')
    .pipe(webpack( require('./webpack.config.js') ))
    .pipe(gulp.dest('./dist/js/'));
});

gulp.task('copy-images', function() {
  return gulp.src('./src/images/**/*')
    .pipe(gulp.dest('./dist/images/'));
});

gulp.task('copy-fonts', function() {
  return gulp.src('./src/fonts/**/*')
    .pipe(gulp.dest('./dist/fonts/'));
});

gulp.task('clean', ['webpack'], function() {
	return gulp.src('./node_modules', {read: false})
		.pipe(clean());
});

gulp.task('default', ['webpack', 'sass', 'copy-images', 'copy-fonts']);

gulp.task('build', ['webpack', 'sass', 'copy-images', 'copy-fonts', 'clean']);
