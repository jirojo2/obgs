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
    }
])