
class KafkaException(Exception):

    def __init__(self, message, topic):
        full_message = f"Topic: {topic} | Msg: {message}"
        super().__init__(full_message)