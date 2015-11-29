function restCollectionTransform (data, headersGetter) {
    data = angular.fromJson(data);
    list = data._items;
    return list;
}

angular.module('obgs')
.factory('Scan', ['$resource',
    function($resource) {
        return $resource('api/scans/:id', null, {
            'get': { method: 'GET' },
            'query': { method: 'GET', isArray: true, transformResponse: restCollectionTransform }
        });
    }
])
.controller('ScanListCtrl', ['$scope', '$timeout', 'Scan',
    function($scope, Scan) {
        $scope.scans = Scan.query();
        $scope.scan = new Scan({
            tstamp: new Date(),
            finished: false,
            launched: false,
            ports: '22,80,443'
        });

        $scope.launchScan = function(scan) {
            scan.tstamp = new Date();
            scan.$save();
        }
    }
])