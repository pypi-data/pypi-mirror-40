import logging
import aiofiles as aiof

# Writer to files in data/raw
# The default process makes each event its own line. so that block by block file reading works correctly
_logger=logging.getLogger('wss.coroutines.write_file')
_logger.setLevel(logging.DEBUG)
async def write_file( source,path ):
    async with aiof.open(path,'w') as f: # Asynchronous file opening
        _logger.info('Opened file at %s' % path)
        try:
            async for item in source:
                await __write_file( item,f )
                _logger.info('Wrote event to %s...' % path)
        except TypeError:
            for item in source:
                await __write_file( item,f )
                _logger.info('Wrote event to %s...' % path)
        _logger.info('Stopping execution...')


async def __write_file( item,file ):
    _logger.info('Received event from queue, awaiting file processing...')
    await file.write( item ) # Async file write
    await file.flush()

async def read_lines( path ):
    async with aiof.open(path) as f:
        async for line in f:
            yield line

async def read_file( path ):
    async with aiof.open(path) as f:
        return await f.read()
