from kafka.BaseProduser import BaseProducer

class DeleteProducer(BaseProducer):

    def __init__(self, topik_name="delete_user_event"):
        super().__init__(topik_name=topik_name)