import logging
from logging.config import dictConfig

LOG_CONFIG = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': 'ext://sys.stdout'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console']
    }
}

def configure_logging(level: str):
    LOG_CONFIG['root']['level'] = level
    dictConfig(LOG_CONFIG)

logger = logging.getLogger(__name__)