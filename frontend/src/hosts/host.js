function restCollectionTransform (data, headersGetter) {
    data = angular.fromJson(data);
    list = data._items;
    return list;
}

angular.module('obgs')
.factory('Host', ['$resource',
    function($resource) {
        return $resource('api/hosts/:id', null, {
            'get': { method: 'GET' },
            'query': { method: 'GET', isArray: true, transformResponse: restCollectionTransform }
        });
    }
])
.controller('HostListCtrl', ['$scope', 'Host',
    function($scope, Host) {
        $scope.hosts = Host.query();
        $scope.filter = {};

        // /api/hosts?where={"ports.service.name":"X509"}
        // /api/hosts?where={"ports.service.banner":{"$regex":"SSH"}}
    }
])