from boundio.examples.utils import get_example_code
source = get_example_code(__file__)

from boundio.stdin import stdin_stream
import boundio as bio

@bio.task() # Add task to task list
async def basic_echo():
    async for line in stdin_stream():
        line = line[:-1]
        if line == 'quit': break
        print(line)

if __name__ == '__main__':
    bio.run_tasks()
else:
    bio.clear_tasks()
