import datetime
import sys

def log(message, out=sys.stdout):
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    out.write('[' + current_time + '] ' + message)
    out.flush()
