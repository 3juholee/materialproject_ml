import argparse
import json
from urllib import urlopen
import time
from scipy import *
import sys
#import __future__
#from urllib.request import urlopen # preamble

def surl(url): #simplified version of openurl
    return json.loads(urlopen(url+'/?format=json').read().decode('utf-8'))


def getlist():
    """
    Make the list of all tenaries
    OUTPUT -> ./Compounds.txt
    """
    URL=SERVER+'/'+PROJECT # project-layer
    print(URL)
    t1=time.time()
    entry=json.loads(urlopen(surl(URL)).read().decode('utf-8')) # load
    t2=time.time()
    print "time for the compound list= %2.2f sec"%(t2-t1)
    
    CompList=entry['aflowlib_entries']
    print "number of ternary= %d" %len(CompList)
    with open("Compounds.txt",'w') as f:
        for comp in CompList:
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
    
SERVER='http://aflowlib.duke.edu' # server name
PROJECT='AFLOWDATA/LIB3_RAW/' # project name: ternary
prefix=SERVER+'/'+PROJECT 

if __name__=="__main__":
    
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--start', action='store', dest='start',type=int)
    parser.add_argument('--end', action='store', dest='end',type=int)
    
    results = parser.parse_args()
    start = results.start
    end = results.end

    with open('Compounds.txt','r') as rf:
        readall=rf.read()
        CompList=readall.split('\n')[:-1]
        #print len(CompList)
    
    if not start:
        start=0
    if not end:
        end=len(CompList)

    print "From %d to %d" %(start,end)
    getData(start,end)
