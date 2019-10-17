import asyncio

from aiorpc import RPC, init_rmq


@RPC('end')
async def foo():
    print(f'foo get message')
    return {'queue': 'end', 'result': 'lol'}


@RPC('end')
async def log(temp):
    print(f'log get message: {temp}')
    return {'queue': 'end', 'error': 'kek'}


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_rmq(loop, 'test'))
    loop.run_forever()
