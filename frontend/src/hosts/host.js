function restCollectionTransform (data, headersGetter) {
    data = angular.fromJson(data);
    list = data._items;
    return list;
}

angular.module('obgs')
.factory('Host', ['$resource',
    function($resource) {
        return $resource('api/scans/:scan_id/hosts/:id', {
            'scan_id': '@scan_id'
        }, {
            'get': { method: 'GET' },
            'query': { method: 'GET', isArray: true, transformResponse: restCollectionTransform }
        });
    }
])
.controller('HostListCtrl', ['$scope', '$stateParams', 'Host',
    function($scope, $stateParams, Host) {
        $scope.hosts = Host.query($stateParams);
        $scope.filter = {};

        // /api/hosts?where={"ports.service.name":"X509"}
        // /api/hosts?where={"ports.service.banner":{"$regex":"SSH"}}
    }
])