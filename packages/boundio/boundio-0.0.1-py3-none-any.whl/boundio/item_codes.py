class ITEM_CODE():
    def __init__( self,name ):
        self.name = name
    def __str__(self):
        return ''

class CLOSE_STREAM(ITEM_CODE):
    def __init(self, frame):
        super(CLOSE_STREAM,self).__init__("boundio._lib.item_codes.CLOSE_SOCKET")
        self.frame = frame
    def __str__(self):
        return str(self.frame)

SKIP_ITEM = ITEM_CODE("boundio._lib.item_codes.SKIP_ITEM")
# END_IO = ITEM_CODE("boundio._lib.item_codes.END_IO")
