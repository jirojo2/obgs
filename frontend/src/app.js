angular.module('templates', []);

var app = angular.module('obgs',
        [
                'ui.router',
                'ngMaterial',
                'ngResource',
                'templates'
        ]
)

app.config(['$stateProvider', '$urlRouterProvider',
    function($stateProvider, $urlRouterProvider) {
        //
        // For any unmatched url, redirect to /state1
        $urlRouterProvider.otherwise("/");
        //
        // Now set up the states
        $stateProvider
            .state('dashboard', {
                url: "/",
                templateUrl: "dashboard.html",
                controller: "DashboardCtrl"
            })
            .state('help', {
                url: "/",
                templateUrl: "dashboard.html",
                controller: "DashboardCtrl"
            })
            .state('scans', {
                url: "/scans",
                templateUrl: "scans/list.html",
                controller: "ScanListCtrl"
            })
            .state('scan', {
                url: "/scan/:scan_id",
                templateUrl: "scans/details.html",
                controller: "ScanDetailsCtrl"
            })
            .state('scan.hosts', {
                url: "/hosts",
                templateUrl: "hosts/list.html",
                controller: "HostListCtrl"
            })
    }
])

app.config(['$mdThemingProvider', '$mdIconProvider',
    function($mdThemingProvider, $mdIconProvider){
        $mdThemingProvider.theme('default')
            .primaryPalette('blue')
            .accentPalette('red');
    }
])

app.controller('DashboardCtrl', ['$scope',
    function($scope) {
        // TODO: dashboard
    }
])