import asyncio

from aiorpc import RMQ

microservice = RMQ(request_queue='test', response_queue='end')


@microservice.RPC
async def foo():
    print(f'foo get message')
    return {'result': 'lol'}


@microservice.RPC
async def log(temp):
    print(f'log get message: {temp}')
    return {'error': 'kek'}


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_forever()
