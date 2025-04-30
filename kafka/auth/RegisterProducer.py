from kafka.BaseProduser import BaseProducer

class RegisterProducer(BaseProducer):

    def __init__(self, topik_name="register_event"):
        super().__init__(topik_name=topik_name)



