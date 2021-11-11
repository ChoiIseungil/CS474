# Written by Seungil Lee, Nov 11, 2021

import json
import os
import glob

files = []
for file in glob.glob("./raw_data/*.json"): files.append(file)


with open('./data.txt','w') as f:
    for file in files:
        j = open(file,'r')
        data = json.load(j)
        for key in data: print(key)
        titles = data["title"]
        bodies = data["bodies"]
        for key in titles:
            f.write(titles[key] + ' ' + bodies[key] + '\n')

# f = open()