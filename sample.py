import random


def locations(f):
    with open(f, "r") as fh:
        for line in fh:
            bits = line.split("\t")
            yield bits

print(",".join([ "ID", "Name", "Lat", "Long" ]))
for b in locations("AU.txt"):
    if random.randint(0, 10000) < 5:
    	print(",".join([b[0], b[1], b[4], b[5]]))
