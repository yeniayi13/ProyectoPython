from src.common.application.ports.event_handler import Event_handler
import pika
from pika.adapters.blocking_connection import BlockingChannel
import json

class Pika_event_handler(Event_handler):

    def __init__(self, channel:BlockingChannel):
        self.channel  = channel  

    def publish(self, event, key ,exchange =''):
        print('holaa')
        print(key, exchange)
        print(event)
        
        self.channel.basic_publish(
            exchange=exchange,
            routing_key= key,
            body=json.dumps(event)
        )
        
    

    def consume():
        pass



