import asyncio

from aiorpc import OGAIO_RMQ

microservice = OGAIO_RMQ(request_queue='test', response_queue='end')


@microservice.RPC
async def foo():
    print(f'foo get message')
    return {'result': 'some result'}


@microservice.RPC
async def log(temp):
    print(f'log get message: {temp}')
    return {'error': {'code': 32001, 'message': 'internal Error'}}


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_forever()
