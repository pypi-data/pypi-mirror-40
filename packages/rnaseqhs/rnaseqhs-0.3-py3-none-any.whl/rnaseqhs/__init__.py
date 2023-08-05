#This is rnaseqhs package for analysis of RNA_seq data.
r'''
This is rnaseqhs package for analysis of RNA_seq data. Written by Zhi Zhang.

For help in python console,type:
>>>import rnaseqhs
>>>help(rnaseqhs.rnaseqhs)

For help in command line,type:
$ <installed path>/rnaseqhs -h
'''

#import commands

import subprocess
import os
import re
import gzip
import sys
import multiprocessing
from operator import itemgetter, attrgetter
from . import rnaseqhs

__version__ = "0.3"
ncore=1
oar=subprocess.run(['if [ -z "$OAR_NODEFILE"];then echo "";else echo "oar";fi'],shell=True,stdout=subprocess.PIPE).stdout
if oar!=b'\n':
    ncore=int(subprocess.run(['cat "$OAR_NODEFILE"|wc -l'],shell=True,stdout=subprocess.PIPE).stdout)
else:
    ncore=multiprocessing.cpu_count()

class WriteLogin(object):
    def __init__(self,logfile,step,shell,status):
        self.logfile=logfile
        self.step=step
        self.shell=shell
        self.status=status
    def writefile(self):
        fh=open(self.logfile,'a')
        if self.status == 0:
            shell='-'*60+'\n'+self.shell+'\n'+'-'*60+'\n'+'%s finished at %s \n'%(self.step,subprocess.check_output('date "+%Y-%m-%d%:%H:%M:%S"',shell=True))+'-'*60+'\n'
            fh.write(shell)
            print ('-'*60+'\n')
            print (shell)
            print ('-'*60+'\n')
        else:
            shell='-'*60+'\n'+self.shell+'-'*60+'\n'+'%s Error!!!\n%s\n' %(self.step,subprocess.check_output('date "+%Y-%m-%d%:%H:%M:%S"',shell=True))+'-'*60+'\n'
            fh.write(shell)
            print ('-'*60+'\n')
            print (shell)
            print ('-'*60+'\n')
        fh.close()
        
class WriteLoginStart(object):
    def __init__(self,logfile,step):
        self.logfile=logfile
        self.step=step
    def writefile(self):
        fh=open(self.logfile,'a')
        fh.write('-'*60+'\n')
        fh.write('%s starting at %s\n' % (self.step,subprocess.check_output('date "+%Y-%m-%d%:%H:%M:%S"',shell=True)))
        fh.write('-'*60+'\n')
        fh.close()

class CheckTools(object):
    def __init__(self,command):
        self.command=command
    def checkit(self):
        status=subprocess.run(["which %s"%self.command],shell=True).returncode
        return status
            
class CountLines(object):
    def __init__(self,filename):
        self.filename=filename
    def countfile(self):
        n=0
        fh=open( self.filename,'r')
        while True: 
            if not fh.readline():
                break
            else:
                n=n+1
        fh.close()
        return n

class CheckBed(object):
    def __init__(self,bedfile):
        self.bedfile=bedfile
    def getchrs(self):
        chrs={}
        fh=open(self.bedfile,'r')
        while True:
            line=fh.readline().rstrip()
            if not line:
                break
            else:
                features=line.split('\t')
                chrs[str(features[0])]=features[2]
        fh.close()
        return chrs

class RmN(object):
    def __init__(self,infile,ratio,outdir):
        self.infile=infile
        self.ratio=float(ratio)
        self.outdir=outdir
    def removeN(self):
        if re.search('gz$|gzip$', self.infile):
            infilefh = gzip.open(self.infile, 'rb')
        else: 
            infilefh = open(self.infile, 'r')
        fqname = os.path.basename(self.infile).replace('.gz', '')
        fqname = fqname.replace(fqname.split('.')[-1], 'fastq')
        remain = open(self.outdir + '/remained_' + fqname, 'w')
        remove_log  = open(self.outdir + '/removed_N_' + fqname + '.log', 'w')
        remove_reads = 0
        total_reads = 0
        while True:
                readid = infilefh.readline().rstrip()
                if len(readid) == 0:
                        break
                seq = infilefh.readline().rstrip()
                mark = infilefh.readline().rstrip()
                qual = infilefh.readline().rstrip()
                seqlen = len(seq)
                total_reads += 1
                N_count = seq.count('N')
                N_ratio = float(N_count) / seqlen
                if N_ratio <= self.ratio:
                    remain.write('%s\n%s\n%s\n%s\n' %(readid, seq, mark, qual))
                else:
                    remove_reads += 1
        remove_rate = float(remove_reads) / total_reads * 100
        remove_log.write('Total Reads\tRemained Reads\t%Removed N Rate\n')
        remove_log.write('%s\t%s\t%.2f\n' %(total_reads, total_reads - remove_reads, remove_rate))
        infilefh.close()
        remain.close()
        remove_log.close()

class Q20(object):
    def __init__(self,infile,outdir,phred):
        self.infile=infile
        self.outdir=outdir
        self.phred=int(phred)
    def calQ20(self):
        infilefh = open(self.infile, 'r')
        outname = 'Q20_Q30_%s' %os.path.basename(self.infile)
        outfilefh = open(self.outdir + '/' + outname + '.txt', 'w')
        Q20 = 0
        Q30 = 0
        Total_base = 0
        read = 0
        GC = 0
        while True:
            seqid = infilefh.readline().rstrip()
            if len(seqid) == 0:
                break
            seq = infilefh.readline().rstrip()
            GC_num = seq.count('G') + seq.count('C')
            GC += GC_num
            mark = infilefh.readline().rstrip()
            qual = infilefh.readline().rstrip()
            Total_base += len(qual)
            read += 1
            for qu in qual:
                qual_score = ord(qu) - self.phred
                if qual_score >= 20:
                    Q20 += 1
                if qual_score >= 30:
                    Q30 += 1
        pGC = GC/float(Total_base) *100
        PQ20 = float(Q20) / Total_base * 100
        PQ30 = float(Q30) / Total_base * 100
        outfilefh.write('Minimum Quality: %s\n' % self.phred)
        outfilefh.write('Total reads\t%s\n' %read)
        outfilefh.write('Total bases\t%s\n' %format(Total_base, ','))
        outfilefh.write('GC%%\t%.2f\n' %pGC)
        outfilefh.write('Q20 bases\t%s\n' %format(Q20,','))
        outfilefh.write('Q20 bases%%\t%.2f\n' %PQ20)
        outfilefh.write('Q30 bases\t%s\n' %format(Q30,','))
        outfilefh.write('Q30 bases%%\t%.2f\n' %PQ30)
        infilefh.close()
        outfilefh.close()

class SortCover(object):
    def __init__(self,infile,outfile):
        self.infile=infile
        self.outfile=outfile
    def sortit(self):
        infilefh=open(self.infile,'r')
        outfilefh=open(self.outfile,'w')
        content_infile=[]
        while True:
            line = infilefh.readline().rstrip()
            if not line:
                break
            line_list=line.split('\t')
            line_list[1]=int(line_list[1])
            content_infile.append(line_list)
        content_infile=sorted (content_infile, key=itemgetter(0,1))
        for content in content_infile:
            content[1]=str(content[1])
            line='\t'.join(content)
            line=line+'\n'
            outfilefh.write(line)
        infilefh.close()
        outfilefh.close()        

class RmUnpaired(object):
    def __init__(self,infile,outfile):
        self.infile=sorted(infile)
        self.outfile=sorted(outfile)
    def rmUnpaired(self):
        infile1 = open(self.infile[0], 'r')
        infile2 = open(self.infile[1], 'r')
        outfile1=open(self.outfile[0], 'w')
        outfile2=open(self.outfile[1], 'w')
        fq1_reads=[]
        fq2_reads=[]
        total_reads1 = 0
        total_reads2 = 0
        while True:
            readid = infile1.readline().rstrip().split(' ')[0]
            if len(readid) == 0:
                break
            seq = infile1.readline().rstrip()
            mark = infile1.readline().rstrip()
            qual = infile1.readline().rstrip()
            fq1_reads.append(readid)
            total_reads1 += 1
        print ('total reads from fq_1 is: ',total_reads1)
        
        while True:
            readid = infile2.readline().rstrip().split(' ')[0]
            if len(readid) == 0:
                break
            seq = infile2.readline().rstrip()
            mark = infile2.readline().rstrip()
            qual = infile2.readline().rstrip()
            fq2_reads.append(readid)
            total_reads2 += 1
        print ('total reads from fq_2 is: ',total_reads2)
        infile1.close()
        infile2.close()
        fq1_reads=set(fq1_reads)
        fq2_reads=set(fq2_reads)
        
        fq_reads=fq1_reads.intersection(fq2_reads)
        print ('after rmUnpaired total reads is: ',len(fq_reads))
        
        infile1 = open(self.infile[0], 'r')
        infile2 = open(self.infile[1], 'r')
        
        n=0
        while True:
            readid = infile1.readline().rstrip()
            if len(readid) == 0:
                break
            readid_all=readid.split(' ')
            readid_1=readid_all[0]
            seq = infile1.readline().rstrip()
            readid_len=str(len(seq))
            mark = infile1.readline().rstrip()
            qual = infile1.readline().rstrip()
                
            if (readid_1 in fq_reads) :
                n=n+1
                readid_new=readid_1+' '+readid_all[1]+' length='+readid_len
                outfile1.write('%s\n%s\n%s\n%s\n' %(readid_new,seq,readid_new.replace('@','+'),qual))
        n=0
        while True:
            readid = infile2.readline().rstrip()
            if len(readid) == 0:
                break
            readid_all=readid.split(' ')
            readid_1=readid_all[0]
            seq = infile2.readline().rstrip()
            readid_len=str(len(seq))
            mark = infile2.readline().rstrip()
            qual = infile2.readline().rstrip()
                
            if (readid_1 in fq_reads) :
                n=n+1
                readid_new=readid_1+' '+readid_all[1]+' length='+readid_len
                outfile2.write('%s\n%s\n%s\n%s\n' %(readid_new,seq,readid_new.replace('@','+'),qual))
        infile1.close()
        infile2.close()
        outfile1.close()
        outfile2.close() 
