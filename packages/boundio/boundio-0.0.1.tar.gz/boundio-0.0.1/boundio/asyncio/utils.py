# Execute a function as if it's an asynchronous function
# but return the result if not
async def execute_async(func,*args,**kwargs):
    obj = func(*args,**kwargs)
    try:
        return await obj
    except TypeError:
        return obj
