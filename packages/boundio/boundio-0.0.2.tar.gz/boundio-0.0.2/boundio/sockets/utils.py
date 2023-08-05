import websockets

# Put each frame in its own line for easier processing
def process_frame(socket,frame):
    return "{}\n".format( frame.strip().replace( '\n','' ) )
