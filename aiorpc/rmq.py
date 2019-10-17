import json
from functools import partial

import aio_pika

from aiorpc.methods import rpc_methods
from aiorpc.utils import get_logger

logger = get_logger()


async def send(body, queue, exchange):
    await exchange.publish(
        aio_pika.Message(body=json.dumps(body).encode()), routing_key=queue
    )


async def listener(exchange, message):
    async with message.process():
        body = json.loads(message.body.decode())
        response_body = {'jsonrpc': '2.0', 'id': body['id']}

        # check for json-rpc
        method_name = body.get('method')
        if not method_name:
            logger.error(f'message {body} don\'t have "method" field')
            return
        response_queue = rpc_methods[method_name]['queue']

        if body.get('jsonrpc') != '2.0':
            error_text = f'message {body} "jsonrpc" field \'2.0\' was expected'
            logger.error(error_text)
            response_body['error'] = error_text
            send(response_body, response_queue, exchange)
            return

        if not body.get('id'):
            logger.error(f'message {body} don\'t have "id" field')
            send(response_body, response_queue, exchange)
        
        # call rpc method with params
        method = rpc_methods[method_name]
        params = body.get('params')
        try:
            if isinstance(params, list):
                response = await method(*params)
            elif isinstance(params, dict):
                response = await method(**params)
            else:
                response = await method()
        except Exception as e:
            logger.error(f'message {body} raise exception {e}')
            return

        # building response json
        if response.get('result'):
            response_body['result'] = response['result']
        elif response.get('error'):
            response_body['error'] = response['error']
        else:
            response_body['error'] = 'RPC method return nothing'
            await send(response_body, response_body, exchange)
            return

        await send(response_body, response_body, exchange)


async def init_rmq(loop, queue_name, rmq_url='amqp://guest:guest@127.0.0.1/'):
    connection = await aio_pika.connect(loop=loop, url=rmq_url)
    channel = await connection.channel()
    queue = await channel.declare_queue(queue_name)

    await queue.consume(partial(listener, channel.default_exchange))
    return connection, channel.default_exchange
