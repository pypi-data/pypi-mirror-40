import asyncio

# QUEUE FUNCTIONS

# Takes input from an async generator and adds it to an async queue
async def producer_queue(queue, generator):
    async for item in generator:
        await queue.put(item)

# Yields information from an async queue
async def yield_queue(queue):
    while True:
        item = await queue.get()
        if item is END_IO:
            break
        yield item

# Process data in an async queue as an async coroutine
async def process_queue(queue, process):
    async for item in yield_queue(queue):
        yield process(item)
