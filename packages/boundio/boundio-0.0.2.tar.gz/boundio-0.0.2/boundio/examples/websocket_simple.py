from boundio.examples.utils import get_example_code
source = get_example_code(__file__)

from boundio.sockets import run_socket

def on_open(socket):
    return '['

def on_message(socket, message):
    return message.strip().replace('\n','')+',\n'

def on_close(socket):
    return ']'

url = '' # Websocket URL to connect to
output_path = ''

if __name__ == '__main__':
    run_socket(url, output_path, on_open=on_open, on_message=on_message, on_close=on_close, time_limit=10)
