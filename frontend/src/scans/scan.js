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
.controller('ScanListCtrl', ['$scope', 'Scan',
    function($scope, Scan) {
        $scope.scans = Scan.query();
        $scope.scan = new Scan({
            tstamp: new Date(),
            finished: false,
            launched: false,
            remaining: "",
            found: 0,
            ports: '21,22,25,80,110,139,443,445,548,3306,3389,8080,8443'
        });

        $scope.launchScan = function(scan) {
            scan.tstamp = new Date().toUTCString();
            scan.$save();

            // refresh scans
            $scope.scans = Scan.query();
        }
    }
])
.controller('ScanDetailsCtrl', ['$scope', '$stateParams', 'Scan',
    function($scope, $stateParams, Scan) {
        $scope.scan = Scan.get($stateParams);
    }
])