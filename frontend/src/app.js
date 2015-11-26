var app = angular.module('obgs',
        [
                'ui.router',
                'ui.bootstrap',
                'ngResource'
        ]
)

app.config(function($stateProvider, $urlRouterProvider) {
    //
    // For any unmatched url, redirect to /state1
    $urlRouterProvider.otherwise("/");
    //
    // Now set up the states
    $stateProvider
        .state('dashboard', {
            url: "/",
            templateUrl: "src/dashboard.html",
            controller: "DashboardCtrl"
        })
        .state('help', {
            url: "/",
            templateUrl: "src/dashboard.html",
            controller: "DashboardCtrl"
        })
        .state('hosts', {
            url: "/hosts",
            templateUrl: "src/hosts/list.html",
            controller: "HostListCtrl"
        })
        .state('scans', {
            url: "/scans",
            templateUrl: "src/scans/list.html",
            controller: "ScanListCtrl"
        })
})

app.controller('DashboardCtrl', ['$scope',
    function($scope) {
        // TODO: dashboard
    }
])