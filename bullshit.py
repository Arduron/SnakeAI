from random import randint
import json

x = []
y = []
for _ in range(0,1000):
    x.append(randint(1,15) * 21)
    y.append(randint(1,15) * 21)

filename = "y.json"
with open(filename, "w") as fp:
    json.dump(y, fp)


