import sys

"""
to test rf.read()
"""
with open("ICSD_Compounds.txt",'r') as rf1:
    data1=rf1.read()
    #data1=rf1.read().split('\n')[:-1]
    print data1
    #set1=set()
    #for dat in data1:
    #    str1=dat.split('_')[-1]
    #    set1.add(str1)

