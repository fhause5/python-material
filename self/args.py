import sys

x = len(sys.argv)

if x > 1:
    print("Here is: " + str(sys.argv[1:]))
else:
    print("[Error not args]")
