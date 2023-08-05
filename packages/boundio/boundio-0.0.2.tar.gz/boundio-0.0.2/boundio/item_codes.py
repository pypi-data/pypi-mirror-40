class ITEM_CODE():
    def __init__( self,name ):
        self.name = name
    def __str__(self):
        return ''

# Go to on_close
class CLOSE_STREAM(ITEM_CODE):
    def __init__(self, frame):
        super(CLOSE_STREAM,self).__init__("boundio.item_codes.CLOSE_SOCKET")
        self.frame = frame

    def __str__(self):
        return str(self.frame)

# Don't yield this item
SKIP_ITEM = ITEM_CODE("boundio.item_codes.SKIP_ITEM")

# Directly return
END_IO = CLOSE_STREAM('')
END_IO.name = "boundio.item_codes.END_IO"
