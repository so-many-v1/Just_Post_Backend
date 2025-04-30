from .BaseProduser import BaseProducer


class PostProducer(BaseProducer):

    def __init__(self, topik_name="create_post_event"):
        super().__init__(topik_name=topik_name)