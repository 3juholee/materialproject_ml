import argparse
import json
from urllib import urlopen, URLopener
import time
from scipy import *
import sys
import os

"""
Fetch files in 
http://aflowlib.duke.edu/AFLOWDATA/ICSD_WEB/
"""
    
prefix='http://aflowlib.duke.edu/AFLOWDATA/ICSD_WEB/'
tags=[
    'BCC', 
    'BCT', 
    'CUB', 
    'FCC', 
    'HEX', 
    'MCL', 
    'MCLC', 
    'ORC',
    'ORCC', 
    'ORCF', 
    'ORCI', 
    'RHL', 
    'TET', 
    'TRI'
    ] 

def surl(url): #simplified version of openurl
    return json.loads(urlopen(url+'/?format=json').read().decode('utf-8'))

def getlistall():
    """
    Make the list of all tenaries
    OUTPUT -> ./Compounds.txt
    """
    List=[]
    for tg in tags:
        URL=prefix+tg
        print(URL)
        t1=time.time()
        entry=surl(URL)
        t2=time.time()
        print "time for the %s = %2.2f sec" %(tg,t2-t1) 
        
        CompList=entry['aflowlib_entries']
        for comp in CompList.values():
            str1 = comp.split('_')[0]
            nonumber=''
            for s in str1:
                if s.isdigit() or s=='.':
                    nonumber=nonumber+' '
                else:
                    nonumber=nonumber+s

            if len(nonumber.split())==3:
                List.append(comp)
    
    print "number of ternary= %d" %len(List)
    with open("ICSD_Compounds.txt",'w') as f:
        for comp in List:
            if ':' in comp: continue #skip compounds name having ':'
            print >>f, comp



def getICSD(comp):
    res=[]
    ptypes=surl(prefix+comp)['aflowlib_entries']
    for s in ptypes:
        if 'ICSD' in s:
            res.append(s)
    return res

def PrintUrl(url,outputfile):
    with open(outputfile,'w') as f:
        fhand=urlopen(url+'/?format=json')
        #print url
        for line in fhand:
            print >>f, line.strip()


def getData(start,end,timecut=1e100):
    t1=time.time()
    i=0
    i_icsd=0
    for comp in CompList[start:end]:
        i=i+1
        tryICSD=getICSD(comp)
        if tryICSD:
            for icsd_id in tryICSD:
                i_icsd=i_icsd+1
                outputfile=comp+'_'+icsd_id
                url=prefix+''+comp+'/'+icsd_id
                PrintUrl(url,outputfile)
        t2=time.time()
        if t2-t1>timecut:
            print "number of materials searched= %d" %i
            print "time's up!, t=%2.3f sec" %(t2-t1)
            break
    print 'Total time= %2.2f sec' %(t2-t1)
    print 'Number of ICSD= %d ' %i_icsd



def getlist_class(output,nopymatgen=True):
    """
    categorize the compounds in terms of tag list
    """
    matgenIDs=getMatgenIDs()
    with open(output,'w') as f:
        for tg in tags:
            print >>f, '# '+tg
            URL=prefix+tg
            print(URL)
            t1=time.time()
            entry=surl(URL)
            t2=time.time()
            print "time for the %s = %2.2f sec" %(tg,t2-t1) 
            
            CompList=entry['aflowlib_entries']
            for comp in CompList.values():
                if not isTernary(comp):
                    continue
                if nopymatgen:#skip compounds in pymatgen
                    ind=getID(comp)
                    if ind in matgenIDs:
                        continue
                print >>f, '\t'+comp
        


def getcif(target):
    """
    Get all ICSD cif files listed in target file.
    The target file should contain tag like '# BCC'.
    """
    matgenIDs=getMatgenIDs()

    if not os.path.isdir('./ciffiles'):
        os.makedirs('./ciffiles')

    with open(target,'r') as f:
        st=f.readline()
        t1=time.time()
        while st:
            if st[0]=='#':
                tg=st.split()[-1]
                st=f.readline()
                t2=time.time()
                print "time for the %s = %2.2f sec" %(tg,t2-t1) 
                t1=time.time()
                continue
            st=st.strip()
            ind=getID(st)
            if ind in matgenIDs:
                continue #skip matgen compounds
            URL=prefix+tg+'/'+st+'/'+st+'.cif' 
            testfile=URLopener()
            try:
                testfile.retrieve(URL,'ciffiles/'+st)
            except:
                print "Error: ",URL

            st=f.readline()

def getID(string):
    """
    get ICSD id from strings like "Al1H3O3_ICSD_26830"
    """
    return string.split('_')[-1]

def getMatgenIDs():
    """
    get all strings of ICSD-IDs-matproj.txt file
    """
    return set(loadtxt('ICSD-IDs-matproj.txt',comments='#',dtype=str))

def checkMultiplicity():
    comps=loadtxt("tagged_list.txt",comments="#", dtype=str)
    print "total N=", len(comps)
    check=set([])
    for comp in comps:
        check.add(comp)
    print "N without multiplicity=", len(check)
        
def isTernary(string):
    """
    check if given compound is a ternary
    """
    str1 = string.split('_')[0]
    nonumber=''
    for s in str1:
        if s=='.':
            return False
        if s.isdigit():
            nonumber=nonumber+' '
        else:
            nonumber=nonumber+s

    if len(nonumber.split())==3:
        return True
    return False


    
if __name__=="__main__":
    #s=getID('Al1H3O3_ICSD_26830')
    #getlistall()
    #getlist_class('nomatgen_list')
    
    getcif('nomatgen_list')
    #checkMultiplicity()
