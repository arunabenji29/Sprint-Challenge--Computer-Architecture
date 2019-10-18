import sys
from cpu import *

cpu = CPU()
# print(sys.argv)

if len(sys.argv) != 2:
    print("usage: ls.py <filename>", file = sys.stderr)
    sys.exit(1)

else:
    cpu.load(sys.argv[1])
    cpu.run()