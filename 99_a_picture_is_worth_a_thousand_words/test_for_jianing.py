# import re
#
# str = "thisthisdahuainformaiondahua"
#
# a = re.search("dahua",str)
# print str
# print(a)


# list = ["aa","bb", "cc", "aa", "bb"]
#
# a = set(list)
# print(a)
#
# b = set('abracadabra')
#
# print(b)

# import math
#
# for x in range(1, 10):
#     print(x)
#     for y in range(10):
#         print(y)
#         for z in range(10):
#             #print(z)
#             sum = x * 100 + y * 10 + z
#             sum1 = x ** 3 + y ** 3 + z ** 3
#             print("%d,%d%d%d" %(sum1,x,y,z))
#             if sum == x ** 3 + y ** 3 + z ** 3:
#                 print(sum)
# a ="vostm"
# #vos only 1  m>=1 a>=m
# v=0
# o=RTSP Session 0 0 IN IP4 0.0.0.0
# s=Media Server
# c=In IP4 0.0.0.0
# t=0 0
# a=control:*
# a=packetization-rupported:DH
#
#
# m=video 0 RTP/AVP 96
# a=control:trackID
# a=framerate:25 000000

import re
import os

f = open("info.txt","r")
data = f.readlines()
patten1 = re.compile("(.*)=")
patten2 = re.compile("=(.*)")
str = re.findall(patten1,data[0])

li1 = []
v_count = 0
o_count=0
s_count=0
c_count=0
t_count=0
m_count=0
a_count=0
other_count =0 #we can use optimize with dict
for line in data:
    if line.split():
        m_bf = re.findall(patten1, line)
        m_af = re.findall(patten2, line)
        # ******handle m_af*****************#
        if m_af[0].startswith(" "):
            print("ERROR0: has a space after =")
            print("ERR line: ", line.encode("utf-8"))
        # ******handle m_bf*****************#
        if len(m_bf[0]) != 1: # only a char before =.
            print("ERROR1: not only a character before =")
            print("ERR line: ", line.encode("utf-8"))
        else:
            if m_bf[0] == "v":
                v_count += 1
            elif m_bf[0] == "o":
                o_count += 1
            elif m_bf[0] == "s":
                s_count += 1
            elif m_bf[0] == "t":
                t_count += 1
            elif m_bf[0] == "m":
                m_count += 1
            elif m_bf[0] == "a":
                a_count += 1
            elif m_bf[0] == "c":
                c_count += 1
            else:
                other_count += 1

if v_count !=1 or o_count != 1 or s_count != 1:
    print("ERROR2: 'vos' not only one in stream!")

if m_count < 1:
    print("ERROR3: m_count less than 1")

if a_count <1:
    print("ERROR4: a_count less than 1")
elif a_count < m_count:
    print("ERROR5: a_count < m_count")

print("v_count= ", v_count)
print("o_count= ", o_count)
print("s_count= ", s_count)
print("t_count= ", t_count)
print("m_count= ", m_count)
print("a_count= ", a_count)
print("c_count= ", c_count)
print("other_count= ", other_count)