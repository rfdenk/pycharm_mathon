
import sys

def pr(s, end='\n', flush=False):
    sys.stdout.write(s)
    sys.stdout.write(end)
    if flush: sys.stdout.flush()

