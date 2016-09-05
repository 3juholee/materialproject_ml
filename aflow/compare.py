import sys

"""
ICSD_WEB(ICSD_Compounds.txt)
vs
LIB3 with ICSD tag (collect/ICSDlist.txt)
"""
with open("ICSD_Compounds.txt",'r') as rf1:
    data1=rf1.read().split('\n')[:-1]
    set1=set()
    for dat in data1:
        str1=dat.split('_')[-1]
        set1.add(str1)

with open("collect/ICSDlist.txt",'r') as rf2:
    data2=rf2.read().split('\n')[:-1]
    for dat in data2:
        st=dat.split('ICSD')[-1]
        str2=st.split('.')[0][1:]

        if str2 not in set1:
            print str2


