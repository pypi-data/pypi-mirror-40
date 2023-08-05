# -*- coding: utf-8 -*-

handlers = {
    'utils_debug': {
        'level': 'DEBUG',
        'filters': None,
        'formatter': 'webutils',
    },
    'utils_warning': {
        'level': 'WARNING',
        'filters': None,
        'formatter': 'webutils',
    },
    'auth_debug': {
        'level': 'DEBUG',
        'filters': None,
        'formatter': 'webutils',
    },
    'auth_warning': {
        'level': 'WARNING',
        'filters': None,
        'formatter': 'webutils',
    },
}

logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'webutils': {
            'format': '[%(levelname).1s]%(asctime)s [%(name)s]: %(message)s',
        },
    },

    'loggers': {
        'utils': {
            'handlers': ['utils_debug', 'utils_warning'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'utils.auth': {
            'handlers': ['auth_debug', 'auth_warning'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
