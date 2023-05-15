from app import sdx_app, CONFIG
from app.cleanup import process


if __name__ == '__main__':
    sdx_app.add_pubsub_endpoint(process, CONFIG.QUARANTINE_TOPIC_ID)
    sdx_app.run(port=5000)
