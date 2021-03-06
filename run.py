from app import subscriber, cloud_config
import structlog

logger = structlog.get_logger()


if __name__ == '__main__':
    logger.info('Starting SDX Cleanup')
    cloud_config()
    subscriber.start()
