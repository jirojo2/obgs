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

        $scope.getHostIP = function(host) {
            var ip = host._id
            var part1 = ip & 255;
            var part2 = ((ip >> 8) & 255);
            var part3 = ((ip >> 16) & 255);
            var part4 = ((ip >> 24) & 255);
            return part4 + "." + part3 + "." + part2 + "." + part1;
        }
    }
])