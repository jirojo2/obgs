angular.module('obgs')
.controller('DashboardCtrl', ['$scope', 'Host',
    function($scope, Host) {
        $scope.hosts = Host.query();
    }
])