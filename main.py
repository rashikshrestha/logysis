import sys
from logysis.logysis import logysis

if len(sys.argv)!=2:
    print("Usage: python main.py logfile.txt")
    sys.exit()

log_data = logysis(sys.argv[1])
print(log_data)