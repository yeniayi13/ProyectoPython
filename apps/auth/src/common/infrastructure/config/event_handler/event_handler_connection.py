import pika
import pika.exceptions
import logging
from src.common.infrastructure.config.config import get_settings_auth
settings =get_settings_auth()

try:
    print('Initializing connection with Message Queues in Auth')
    connection_parameters = pika.ConnectionParameters(settings.RMQHOST)
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()

    exchange = channel.exchange_declare(
                exchange='users',
                exchange_type='direct'
                )


    client_created_queue = channel.queue_declare(settings.CLIENT_CREATED_QUEUE)
    manager_created_queue = channel.queue_declare(settings.MANAGER_CREATED_QUEUE)
    superadmin_created_queue = channel.queue_declare(settings.SUPERADMIN_CREATED_QUEUE)
    client_modified_queue = channel.queue_declare(settings.CLIENT_MODIFIED_QUEUE)
    manager_modified_queue = channel.queue_declare(settings.MANAGER_MODIFIED_QUEUE)

    channel.queue_bind(exchange='users', queue=client_created_queue.method.queue,routing_key='users.client_created')
    channel.queue_bind(exchange='users', queue=manager_created_queue.method.queue, routing_key='users.manager_created')
    channel.queue_bind(exchange='users', queue=superadmin_created_queue.method.queue, routing_key='users.superadmin_created')
    channel.queue_bind(exchange='users', queue=client_modified_queue.method.queue, routing_key='users.client_modified')
    channel.queue_bind(exchange='users', queue=manager_modified_queue.method.queue, routing_key='users.manager_modified')
    
    print('Auth Queues Ready')
except pika.exceptions.AMQPConnectionError as e:
    logging.error(f"Connection error: {e}")
    raise e
except Exception as e:
    logging.error(f"Unkwon error: {e}")
    raise e





def get_channel():
    try:
        connection = pika.BlockingConnection(connection_parameters)
        channel = connection.channel()
        print('yielding channel ...')
        yield channel
    except pika.exceptions.AMQPConnectionError as e:
        logging.error(f"Connection error: {e}")
        #return
    except pika.exceptions.StreamLostError:
        logging.error(f"Connection error: {e}")
        #return
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        #return
    finally:
        print('closing channel ...')
        channel.close() 
        connection.close()