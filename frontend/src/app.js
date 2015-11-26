angular.module('templates', []);

var app = angular.module('obgs',
        [
                'ui.router',
                'ui.bootstrap',
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

app.controller('DashboardCtrl', ['$scope',
    function($scope) {
        // TODO: dashboard
    }
])