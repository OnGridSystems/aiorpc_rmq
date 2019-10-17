rpc_methods = {}


def RPC(queue):
    def inner(func):
        rpc_methods[func.__name__] = {'func': func, 'queue': queue}
        return func
    return inner
