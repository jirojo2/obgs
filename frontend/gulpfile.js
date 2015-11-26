var gulp = require('gulp');
var uglify = require('gulp-uglify');
var concat = require('gulp-concat');
var rename = require("gulp-rename");
var copy = require("gulp-copy");
var minifyCss = require('gulp-minify-css');
var templateCache = require('gulp-angular-templatecache');

gulp.task('templatecache', function() {
    return gulp
        .src('src/**/*.html')
        .pipe(templateCache())
        .pipe(gulp.dest('public'));
});

gulp.task('scripts', ['templatecache'], function() {
    return gulp
        .src([
            'src/**/*.js',
            'public/templates.js'
        ])
        .pipe(concat('app.min.js'))
        .pipe(uglify())
        .pipe(gulp.dest('public'))
});

gulp.task('styles', [], function() {
    return gulp
        .src([
            'src/app.css'
        ])
        .pipe(minifyCss({compatibility: 'ie8'}))
        .pipe(rename({suffix: ".min"}))
        .pipe(gulp.dest('public'));
})

gulp.task('bootstrap', [], function() {
    return gulp
        .src('bower_components/bootstrap/**/*')
        .pipe(copy('public', { prefix: 1 }))
});

gulp.task('font-awesome', [], function() {
    return gulp
        .src('bower_components/font-awesome/**/*')
        .pipe(copy('public', { prefix: 1 }))
});

gulp.task('dependencies', ['font-awesome', 'bootstrap'], function() {
    return gulp
        .src([
            'bower_components/angular/angular.min.js',
            'bower_components/angular-resource/angular-resource.min.js',
            'bower_components/angular-ui-router/release/angular-ui-router.min.js',
            'bower_components/angular-bootstrap/ui-bootstrap-tpls.min.js'
        ])
        .pipe(concat('dependencies.min.js'))
        .pipe(gulp.dest('public'))
});

gulp.task('index', [], function() {
    return gulp
        .src('src/app.html')
        .pipe(rename('index.html'))
        .pipe(gulp.dest('public'))
});

gulp.task('default', ['dependencies', 'scripts', 'styles', 'index']);