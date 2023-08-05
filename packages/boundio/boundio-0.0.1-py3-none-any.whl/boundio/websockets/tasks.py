import asyncio
from boundio.asyncio.queues import yield_queue, producer_queue
from boundio.asyncio.raw_io import write_file
from boundio.asyncio.tasks import run_tasks
from boundio.websockets.utils import process_frame, connect

# Simplest way to interact with a socket, returns a coroutine that can be directly used as a task
async def get_socket_task(url, on_open=None,
    on_close=None, on_message=print, time_limit=None ):
    async with connect(url) as socket:
        async for item in process_socket(socket, on_open, on_close, on_message, time_limit ):
            yield item

# Gets a pair of consumer and producer coroutines for a given socket
def get_socket_tasks( url, path, on_open=None, on_close=None, on_message=process_frame, time_limit=None ):
    queue = asyncio.Queue()
    producer = producer_queue(queue, get_socket_task(url, on_open, on_close, on_message = on_message, time_limit=time_limit) )
    consumer = write_file(yield_queue(queue),path)
    return producer,consumer

# Runs a single socket
def run_socket(url, path, on_open = None, on_close = None, on_message = process_frame, time_limit=None ):
    producer, consumer = get_socket_tasks(url, path, on_open, on_close, on_message, time_limit)
    run_tasks(producer,consumer)
