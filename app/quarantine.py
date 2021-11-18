from app import CONFIG


def quarantine_receipt(message: object, error: str):
    data = message.data
    future = CONFIG.QUARANTINE_PUBLISHER.publish(CONFIG.QUARANTINE_TOPIC_PATH, data, error=error)
    return future.result()
