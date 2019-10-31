import asyncio

from aiorpc import OGAIO_RMQ

microservice = OGAIO_RMQ(request_queue='test', response_queue='end')


@microservice.RPC
async def foo():
    print(f'foo get message')
    return 'foo'


@microservice.RPC
async def bar(var):
    print(f'log get message: {var}')
    if isinstance(var, int):
        return var ** 2
    else:
        raise TypeError('var must be int')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        print(vars(microservice))
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(microservice.close())
