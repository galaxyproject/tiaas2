"""Logging configuration."""

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} | {asctime} | {module}: {message}',
            'style': '{',
        },
    },
    'handlers': {
        'stdout': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['stdout'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
