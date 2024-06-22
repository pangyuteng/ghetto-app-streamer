import sys
from vncdotool import api

if __name__ == "__main__":
    keyargs = sys.argv[1]
    client = api.connect('localhost:5901', password=None)
    client.keyPress(keyargs)
