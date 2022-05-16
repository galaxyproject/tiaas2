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
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/tmp/main.log',
            'backupCount': 5,
            'maxBytes': 1000000,  # 1MB ~ 20k rows
            'formatter': 'verbose',
        },
    },
    'django': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG',
    },
}
