"""Logging configuration."""

import logging


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'formatters': {
            'simple': {
                'format': '{levelname} | {asctime} | {module}: {message}',
                'style': '{',
            },
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/tiaas/main.log',
            'backupCount': 5,
            'maxBytes': 1000000,  # 1MB ~ 20k rows
            'formatter': 'simple',
        },
    },
    'django': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG',
    },
}
