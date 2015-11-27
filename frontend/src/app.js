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
            .state('hosts', {
                url: "/hosts",
                templateUrl: "hosts/list.html",
                controller: "HostListCtrl"
            })
            .state('scans', {
                url: "/scans",
                templateUrl: "scans/list.html",
                controller: "ScanListCtrl"
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