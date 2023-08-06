import logging
import logging.config


def config_logger():
    config = {
        'version': 1,
        'formatters': {
            'brief': {
                'format': '[contacter] %(levelname)s %(asctime)s %(message)s',
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
            }
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            }
        }
    }

    logging.config.dictConfig(config)
