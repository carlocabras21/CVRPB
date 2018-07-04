import os
# File Handler

def read_instance(filename):
    if os.path.isfile("data/Instances/" + filename + ".txt"):
        fp = open("data/Instances/" + filename + ".txt")
        for line in fp:
            print(line.split())
