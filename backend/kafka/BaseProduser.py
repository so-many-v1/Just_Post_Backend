from typing import Union
import json
import uuid

from aiokafka import AIOKafkaProducer

from config import KAFKA_BOOTSTRAP_SERVERS
from exceptions import KafkaException

from pydantic import BaseModel

class KafkaUtils:

    def generate_event_id(self) -> str:
        return str(uuid.uuid4())

    async def serialize_payload(self, payload: Union[dict, BaseModel]):

        if isinstance(payload, BaseModel):
            return json.dumps(payload.model_dump()).encode("utf-8")

        return json.dumps(payload).encode("utf-8")

class BaseProducer(KafkaUtils):

    def __init__(
            self,
            topik_name,
            bootstrap_server=KAFKA_BOOTSTRAP_SERVERS,
    ):
        self.bootstrap_server = bootstrap_server
        self.topik_name = topik_name
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_server,
            compression_type="zstd",
        )

    async def start_producer(self):
        await self.producer.start()

    async def stop_producer(self):
        await self.producer.stop()


    async def send_event(self, payload: Union[dict, BaseModel]):
        try:
            if not self.producer._closed:
                await self.start_producer()

            ser_payload = await self.serialize_payload(payload=payload)

            response = await self.producer.send_and_wait(
                topic=self.topik_name,
                value=ser_payload
            )

            if response:
                return True
            else:
                raise KafkaException(message="Error recording event", topic=self.topik_name)

        except Exception as e:
            print(e)






