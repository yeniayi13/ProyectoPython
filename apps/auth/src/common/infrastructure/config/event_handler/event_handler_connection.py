import pika
import pika.exceptions
import logging

#logging.basicConfig(level=logging.INFO)

try:
    print('Initializing connection with Message Queues')
    connection_parameters = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()

    exchange = channel.exchange_declare(
                exchange='users',
                exchange_type='direct'
                )

    client_created_queue = channel.queue_declare('client_created')
    manager_created_queue = channel.queue_declare('manager_created')
    superadmin_created_queue = channel.queue_declare('superadmin_created')
    client_modified_queue = channel.queue_declare('client_modified')
    manager_modified_queue = channel.queue_declare('manager_modified')

    channel.queue_bind(exchange='users', queue=client_created_queue.method.queue,routing_key='users.client_created')
    channel.queue_bind(exchange='users', queue=manager_created_queue.method.queue, routing_key='users.manager_created')
    channel.queue_bind(exchange='users', queue=superadmin_created_queue.method.queue, routing_key='users.superadmin_created')
    channel.queue_bind(exchange='users', queue=client_modified_queue.method.queue, routing_key='users.client_modified')
    channel.queue_bind(exchange='users', queue=manager_modified_queue.method.queue, routing_key='users.manager_modified')
except pika.exceptions.AMQPConnectionError as e:
    logging.error(f"Connection error: {e}")
    raise e
except Exception as e:
    logging.error(f"Unkwon error: {e}")
    raise e

print('Queues Ready')



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