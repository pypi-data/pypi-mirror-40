import asyncio
import logging

_logger=logging.getLogger('wss.coroutines.read_socket')
_logger.setLevel(logging.DEBUG)
async def read_socket(socket, time_limit = 30 ):
    """
    This coroutine function reads frames from a socket and yields them
    asynchronously
    """
    if time_limit is None:
        end_time = None
    else:
        loop = asyncio.get_running_loop()
        end_time = loop.time() + time_limit

    async for frame in socket:# yield to other processes while IO from socket is happening
        # Give back the frame received
        _logger.info('Received frame from socket')
        yield frame # No longer syntax error: https://stackoverflow.com/questions/37549846/how-to-use-yield-inside-async-function

        # Check for time limit to see if should stop
        if end_time is not None and (loop.time() + 1.0) >= end_time:
            _logger.info('%s second time limit reached, stopping execution...' % time_limit)
            break
