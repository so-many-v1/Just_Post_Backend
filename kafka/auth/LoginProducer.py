from kafka.BaseProduser import BaseProducer

class LoginProducer(BaseProducer):

    def __init__(self, topik_name="login_event"):
        super().__init__(topik_name=topik_name)