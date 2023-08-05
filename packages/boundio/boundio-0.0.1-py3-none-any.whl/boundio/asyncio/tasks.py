import asyncio

task_list = []

def task(*args,**kwargs):
    # Adds an asynchronous function to the task list
    # so that it will be run when run_tasks is called
    global task_list
    def decorator(func):
        # Add function & arguments to the task list
        task_list.append( ( func, args, kwargs.copy() ) )
        return func
    return decorator

# Runs a set of tasks asynchronously. If functions have been decorated with the @task decorator,
# They are automatically included in the task list.
def run_tasks( *tasks ):
    global task_list

    # Create tasks right before running
    tasks = list(tasks) + [func(*args,**kwargs) for func,args,kwargs in task_list]
    try:
        loop = asyncio.get_event_loop() # Let's get/create an event loop
        # tasks = [asyncio.create_task(handler) for handler in task_list]
        loop.run_until_complete(asyncio.gather(*tasks)) # And have it run the IO tasks
    except KeyboardInterrupt as e:
        print(f"Cancelling all tasks due to KeyboardInterrupt:\n\n{e}\n")

        # asyncio.Task.all_tasks() gets a list of all tasks
        # task.done() returns True if the task is done; if it's done, we don't need to cancel it
        # task.cancel() stops the task
        [task.cancel() for task in asyncio.Task.all_tasks()]# if not task.done()]
    finally:
        task_list = []
