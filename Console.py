
import sys

# shim for 3.6.2 print() function
# version 3.2 doesn't support the 'flush' parameter,
# but I like to use it!


def pr(s, end='\n', flush=False):
    sys.stdout.write(s)
    sys.stdout.write(end)
    if flush:
        sys.stdout.flush()
