var gulp = require('gulp');
var uglify = require('gulp-uglify');
var concat = require('gulp-concat');
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

gulp.task('default', ['scripts']);