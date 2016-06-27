#-*- coding:utf-8 -*-
app = {
    'template_path': './templates',
    'static_prefix': '/static',
    'static_path': 'static',
    'locale': 'chinese',
    'debug': False
}
database = {
    'default': 'mysql',
    'connections': {
        'mysql': {
            'host': '127.0.0.1',
            'user': 'root',
            'port': 3306,
            'password': '526114',
                        'database': 'pyblog'
        },
        'mongodb': {
            'host': '127.0.0.1',
            'user': 'xxxx',
            'port': 27017,
            'auth': 'xxxx'
        }
    }
}
session = {
    'default': 'file',
    'drivers': {
        'file': {
            'session_dir': '/tmp/session/',
            'expire_file': 'session_expire',
            'expire': 3600
        },
        'redis': {
            'host': 'localhost',
            'port': 6379,
            'db': 0,
            'expire': 0
        },
        'mongo': {
            'host': 'localhost',
            'port': 27017,
            'db': 'session',
            'collection': 'session',
            'expire': 0
        }
    }
}
authentication = {
    'auth_table': 'users',
    'auth_id': 'email',
    'login_url': '/login'
}
storage = {
    'default': 'qiniu',  # qiniu,s3,file
    'disks': {
        'file': {
            'driver': 'file',
        },
        'qiniu': {
            'driver': 'qiniu',
            'access_key': 'CKQNXugLAXFueA5UlBKQnkWxslYC8rIErwn2ch4I',
            'secret_key': '4lnKaSKUk1SVmbB4alt6PtkL2O1Sm-jP6e-T7EER',
            'bucket': 'static-pyblog-com',
            'domain': '7xs7oc.com1.z0.glb.clouddn.com'
        },
        's3': {

        }
    }
}
cache = {
    'default': 'redis',  # redis,memcache
    'drivers': {
        'redis': {
            'host': "127.0.0.1",
            'port': 6379,
            'db': 0
        },
        'memcache': {
            'host': '127.0.0.1',
            'port': 11211
        }
    }
}
queue = {
    'default': 'redis',  # mysql,mongo,redis
    'drivers': {
        'redis': {
            'port': 6379,
            'host': '127.0.0.1',
            'db': 0,
        },
        'mongo': {
            'port': 27017,
            'host': '127.0.0.1',
            'db': 'queue'
        },
        'mysql': {
            'host': '127.0.0.1',
            'port': 3306,
            'db': 'queue',
            'user': 'root',
            'password': '526114',
        }
    }
}
service = {
    'mail': {
        'default': 'mailtrap',
        'drivers': {
            'mailtrap': {
                'host': 'mailtrap.io',
                        'user': '521521d9dc1cb1b90',
                                'password': '15029ca2bece56',
                                'port': 2525
            }
        }
    }
}
