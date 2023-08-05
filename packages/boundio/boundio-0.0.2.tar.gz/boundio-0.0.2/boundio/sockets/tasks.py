import asyncio
from boundio.sockets.process import process_socket
from boundio.asynchronous.queues import yield_queue, producer_queue
from boundio.asynchronous.raw_io import write_file
from boundio.asynchronous.tasks import run_tasks
from boundio.asynchronous.utils import consume_source
from boundio.sockets.utils import process_frame
from websockets.client import connect, WebSocketClientProtocol

async def get_socket_gen(url, on_open=None,
    on_close=None, on_message=print, time_limit=None, **kwargs ):
    async with connect(url, **kwargs) as socket:
        async for item in process_socket(socket, on_open, on_close, on_message, time_limit ):
            yield item

# Simplest way to interact with a socket, returns a coroutine that can be directly used as a task
async def get_socket_task(url, on_open=None,
    on_close=None, on_message=print, time_limit=None, **kwargs ):
    await consume_source( get_socket_gen( url, on_open,
        on_close, on_message, time_limit, **kwargs ) )

# Gets a pair of consumer and producer coroutines for a given socket
def get_socket_tasks( url, path, on_open=None,
    on_close=None, on_message=process_frame, time_limit=None, **kwargs ):
    queue = asyncio.Queue()
    producer = producer_queue(queue,
        get_socket_gen(url, on_open, on_close, on_message = on_message, time_limit=time_limit, **kwargs) )
    consumer = write_file(yield_queue(queue),path)
    return producer,consumer

# Runs a single socket
def run_socket(url, path, on_open = None,
    on_close = None, on_message = process_frame, time_limit=None, **kwargs ):
    producer, consumer = get_socket_tasks(url, path, on_open, on_close, on_message, time_limit, **kwargs )
    run_tasks(producer,consumer)
