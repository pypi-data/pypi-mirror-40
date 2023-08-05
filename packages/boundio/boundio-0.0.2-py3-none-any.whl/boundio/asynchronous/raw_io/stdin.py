import asyncio, sys

# Credit goes to github user nathan-hoad and his gist:
# https://gist.github.com/nathan-hoad/8966377

# As well as this page by wangluowenzhang:
# https://www.e-learn.cn/content/wangluowenzhang/843583

# Please don't edit these because they're very precious to my heart
_LOOP = None
_READER = None
__all__ = ['input_async','stdin_stream']

async def stdin_reader():
    # Creates and returns a reader to the standard input stream
    global _LOOP, _READER
    loop = asyncio.get_event_loop()
    if _LOOP is loop:
        return _READER
    _LOOP = loop

    _READER = asyncio.StreamReader()
    reader_protocol = asyncio.StreamReaderProtocol(_READER)
    await _LOOP.connect_read_pipe(lambda: reader_protocol, sys.stdin)
    return _READER

async def input_async(prompt, until='\n', encoding='utf8'):
    # Acts similarly to the input() built-in function
    # Asynchronously reads from standard input, until some separator `sep`
    # `sep` is encoded with `encoding`, and data is decoded with `encoding` as well.
    reader = await stdin_reader()
    if isinstance(until,str):
        until = until.encode(encoding)
    print(prompt,end='')
    out = ( await reader.readuntil(separator=until) )
    if encoding is not None:
        return out.decode(encoding)
    return out

async def stdin_stream(line_prompt='',sep='\n', encoding='utf8'):
    # asynchronous generator that streams data from standard input.
    # Analogue for `while True: yield await input_async(line_prompt,sep=sep, encoding=encoding)``
    while True:
        yield await input_async(line_prompt,until=sep, encoding=encoding)
