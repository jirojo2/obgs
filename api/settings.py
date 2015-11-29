# Please note that MONGO_HOST and MONGO_PORT could very well be left
# out as they already default to a bare bones local 'mongod' instance.
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_USERNAME = ''
MONGO_PASSWORD = ''
MONGO_DBNAME = 'obgs'
MONGO_QUERY_BLACKLIST = ['$where']

# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
RESOURCE_METHODS = ['GET']

# Enable reads (GET), edits (PATCH), replacements (PUT) and deletes of
# individual items  (defaults to read-only item access).
ITEM_METHODS = ['GET']

# Disable XML when browser
XML = False

# Timestamps
LAST_UPDATED = 'tstamp'
DATE_CREATED = 'tstamp'

# Schema
# Hosts
hosts = {
    # 'title' tag used in item links. Defaults to the resource title minus
    # the final, plural 's' (works fine in most cases but not for 'people')
    'item_title': 'host',

    # by default the standard item entry point is defined as
    # '/people/<ObjectId>'. We leave it untouched, and we also enable an
    # additional read-only entry point. This way consumers can also perform
    # GET requests at '/people/<lastname>'.
    #'additional_lookup': {
    #    'url': 'regex("[\w]+")',
    #    'field': 'lastname'
    #},

    # We choose to override global cache-control directives for this resource.
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,

    # most global settings can be overridden at resource level
    #'resource_methods': ['GET', 'POST'],

    'schema': {
        # Schema definition, based on Cerberus grammar. Check the Cerberus project
        # (https://github.com/nicolaiarocci/cerberus) for details.
        'ports': {
            'type': 'dict',
            'schema': {
                'status': {'type': 'string'},
                'reason': {'type': 'string'},
                'port': {'type': 'integer'},
                'proto': {'type': 'string'},
                'banner': {'type': 'string'},
                'service': {
                    'type': 'dict',
                    'schema': {
                        'name': {'type': 'string'},
                        'banner': {'type': 'string'}
                    }
                }
            },
        },
        'ip': {
            'type': 'string'
        },
        'tstamp': {
            'type': 'datetime',
        }
    }
}
# Scans
scans = {
    # 'title' tag used in item links. Defaults to the resource title minus
    # the final, plural 's' (works fine in most cases but not for 'people')
    'item_title': 'scan',

    # by default the standard item entry point is defined as
    # '/people/<ObjectId>'. We leave it untouched, and we also enable an
    # additional read-only entry point. This way consumers can also perform
    # GET requests at '/people/<lastname>'.
    #'additional_lookup': {
    #    'url': 'regex("[\w]+")',
    #    'field': 'lastname'
    #},

    'resource_methods': ['GET', 'POST'],

    # We choose to override global cache-control directives for this resource.
    'cache_control': 'max-age=10,must-revalidate',
    'cache_expires': 10,

    # most global settings can be overridden at resource level
    #'resource_methods': ['GET', 'POST'],

    'schema': {
        # Schema definition, based on Cerberus grammar. Check the Cerberus project
        # (https://github.com/nicolaiarocci/cerberus) for details.
        'target': {
            'type': 'string',
        },
        'remaining': {
            'type': 'string',
        },
        'ports': {
            'type': 'string',
        },
        'progress': {
            'type': 'float',
        },
        'found': {
            'type': 'float',
        },
        'finished': {
            'type': 'boolean',
        },
        'launched': {
            'type': 'boolean',
        },
        'error': {
            'type': 'boolean',
        },
        'tstamp': {
            'type': 'datetime',
        }
    }
}

# Resources
DOMAIN = { 'hosts': hosts, 'scans': scans }

# Open API for dev
X_DOMAINS = '*'