#!/usr/bin/python

#find_sender from email doc

import fileinput, re

print("start")
pat = re.compile(r'[a-z][0-9a-z\-_\.]+@[a-z.]+', re.IGNORECASE)
Emailpath = "D:\\test_zhou\\testmail.txt"
print(pat)
addresses = set() # 使用集合为了剔除重复名字
print(addresses)

try:
    f = open(Emailpath, 'r')
    for line in f.readlines():
        for address in pat.findall(line):
            addresses.add(address)

finally:
    f.close()

print(addresses)
for address in sorted(addresses):
    print(address)

print("end")