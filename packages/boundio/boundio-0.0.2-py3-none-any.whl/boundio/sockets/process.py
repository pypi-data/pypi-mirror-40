from boundio.asynchronous.raw_io.sockets import read_socket
from boundio.item_codes import SKIP_ITEM, CLOSE_STREAM, END_IO
from websockets.client import connect
from boundio.asynchronous.utils import execute_async

# Processes a socket asynchronously
async def process_socket( socket, on_open=None, on_close=None, on_message=None, time_limit=None ):
    """
    This is a low-level coroutine that processes a socket object asynchronously and yields
    the result of that processing. Skips instances of boundio.item_codes.SKIP_ITEM,
    executes on_close immediately after receiving boundio.item_codes.CLOSE_STREAM, and
    yields boundio.item_codes.END_IO upon finishing.
    Params:
        socket - instance of socket from websockets.connect(url)
        on_open - function or coroutine function, executed on socket opening. Returned result is yielded
        on_message - function or coroutine function, executed whenever the socket receives something. Returned result is yielded.
        on_close - function or coroutine function, executed before coroutine exits. Returned result is yielded
        time_limit - time limit for socket to be open for (after on_open is finished) in seconds.
        on_open, on_message, and on_close should return boundio.item_codes.SKIP_ITEM if the item shouldn't be yielded.
        on_open and on_message should return boundio.item_codes.CLOSE_STREAM if this function should execute on_close and then exit
    """
    # Run stuff on open, and yield it
    close = False
    if on_open is not None:
        close, item = await __handle_func(on_open, socket)
        if item is not SKIP_ITEM:
            yield item
            if item is END_IO: return


    # Run stuff per message
    if close is False:
        async for item in __handle_messages(socket, time_limit, on_message):
            yield item
            if item is END_IO: return

    # Run stuff on close
    if on_close is not None:
        item = await execute_async(on_close, socket) # Executes the function given as if it were asynchronous
        if item is not SKIP_ITEM:
            yield item
            if item is END_IO: return
    yield END_IO

async def __handle_messages(socket, time_limit, on_message):
    if on_message is not None:
        async for frame in read_socket(socket, time_limit):
            close, item = await __handle_func(on_message, socket, frame)
            if item is not SKIP_ITEM:
                yield item
                if close: break
    else: # If on_message is None, then the above logic isn't necessary
        async for frame in read_socket(socket, time_limit):
            yield frame

async def __handle_func(func, *args): # Handle a function.
    item = await execute_async(func, *args)
    if item is CLOSE_STREAM:
        return True,CLOSE_STREAM(frame)
    elif isinstance(item,CLOSE_STREAM):
        return True, item
    return False, item
