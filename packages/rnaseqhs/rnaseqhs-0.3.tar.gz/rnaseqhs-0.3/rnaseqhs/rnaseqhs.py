#rnaseqhs - a package for analysis of RNA-seq data.
#
#
#Test of pull

r'''
overview
---------
rnaseqhs can do bioinformatics analysis for RNA_seq data and generate clean BAM/SAM result from HISAT2, GTF result from STRINGTIE and HTseq_count result. This package contains human (hg38) HISAT2 transcriptome index files.

rnaseqhs is available under the terms of the MIT license (see the file ``LICENSE``)

pre-requirements
-----------------
1. 'gzip','fastx_trimmer','fastqc','cutadapt','fastq_quality_filter','HIISAT2','STRINGTIE','samtools (v1.3.1)','bedtools (v2.19.1)' in $PATH.
2.  HIISAT2 built transcriptome index, and gtf & bed file.

Installation
------------
1. tar zxvf rnaseqhs-<version>.tar.gz
2. cd rnaseqhs-<version>
3. python setup.py install --user

Usage
------
1. use it as module in python console ::

    >>>import rnaseqhs

    >>>rnaseqhs.rnaseqhs.main(<Arguments>)

Arguments are ::
    >>>rnaseqhs.rnaseqhs.main(INDIR, OUTDIR, PHRED, QCCHECK, TRIM, LASTKEEP, RMADAPT,
                      LADAPTER, RADAPTER, OVERLAP, MINLEN, REMOVEN, NCUTOFF, 
                      FILTQ, MINQ, PMINQ, QCSTAT, MAPPING, HISAT2INDEX, ORIENTATIONS,RNASTRANDNESS, GTF, DRAWCOVER, GENOMEBED, WINDOWSIZE)

2. use it as command line in bash ::

    <installed-path>/rnaseqhs <options>

Options are ::
usage: rnaseqhs [-h] [-i INDIR] [-o OUTDIR] [-P PHRED] [-Q QCCHECK] [-T TRIM]
                [-l LASTKEEP] [-r RMADAPT] [-L LADAPTER] [-R RADAPTER]
                [-O OVERLAP] [-m MINLEN] [-N REMOVEN] [-c NCUTOFF] [-F FILTQ]
                [--minQ MINQ] [--pminQ PMINQ] [-q QCSTAT] [-M MAPPING]
                [--hisat2index HISAT2INDEX] [--orientations ORIENTATIONS]
                [--rnastrandness RNASTRANDNESS] [--gtf GTF]
                [--drawCover DRAWCOVER] [--genomebed GENOMEBED]
                [--windowsize WINDOWSIZE]

optional arguments:
  -h, --help            show this help message and exit
  -i INDIR, --indir INDIR
                        fastq files path
  -o OUTDIR, --outdir OUTDIR
                        output path
  -P PHRED, --phred PHRED
                        phred score used in platform [33]
  -Q QCCHECK, --qccheck QCCHECK
                        do quality check [true]
  -T TRIM, --trim TRIM  trim given fastq short reads as --lastkeep defined
  -l LASTKEEP, --lastkeep LASTKEEP
                        with "trim" option, last bases to keep
  -r RMADAPT, --rmadapt RMADAPT
                        remove adapter [true]
  -L LADAPTER, --ladapter LADAPTER
                        left adapter [AGATCGGAAGAGC]
  -R RADAPTER, --radapter RADAPTER
                        right adapter [AGATCGGAAGAGC]
  -O OVERLAP, --overlap OVERLAP
                        If the overlap between the read and adapter is shorter
                        than the overlap length, the read will NOT be
                        modified. [6]
  -m MINLEN, --minlen MINLEN
                        Discard trimmed reads that are shorter than "minlen"
                        [75]
  -N REMOVEN, --removeN REMOVEN
                        remove "N" bases [true]
  -c NCUTOFF, --Ncutoff NCUTOFF
                        with "removeN" option, N cutoff [0.1]
  -F FILTQ, --filtQ FILTQ
                        Filters sequences based on quality [true]
  --minQ MINQ           Minimum quality score to keep [20]
  --pminQ PMINQ         Minimum percent of bases [80]
  -q QCSTAT, --qcStat QCSTAT
                        generate QC statistic plot for seq
  -M MAPPING, --mapping MAPPING
                        read mapping [true]
  --hisat2index HISAT2INDEX
                        hisat2 index
  --orientations ORIENTATIONS
                        orientations
  --rnastrandness RNASTRANDNESS
                        rna strandness
  --gtf GTF             gtf file for annotation
  --drawCover DRAWCOVER
                        coverage of genome region [true]
  --genomebed GENOMEBED
                        coverage genome bed file
  --windowsize WINDOWSIZE
                        coverage window size [500000]
'''

#!/usr/bin/env python
import os
import re
import sys
import subprocess
import glob
import pkg_resources
from .__init__  import ncore,__version__,WriteLogin,WriteLoginStart,CheckTools,CountLines,CheckBed,RmN,SortCover,RmUnpaired 
import logging

fastqc='fastqc'
cutadapt='cutadapt'
hisat2='hisat2'
stringtie='stringtie'

removeN=pkg_resources.resource_filename('rnaseqhs','rmN.py')
Q20=pkg_resources.resource_filename('rnaseqhs','Q20_1.py')
ReadMap =pkg_resources.resource_filename('rnaseqhs','ReadMap.R')
sortCover=pkg_resources.resource_filename('rnaseqhs','sortCover2.py')

def getFile(path, regex):
    pattern='%s/*%s'%(path,regex)
    files = glob.glob(pattern)
    return files

def mkDir(path):
    if not os.path.exists(path):
        os.mkdir(path)

#---------------QC check--------------------#
def QC(fqlist,phred,out_dir):
    '''do quality check for fastq list under 33 or 64 phred score'''
    outQC = out_dir + '/01.QC/'
    mkDir(outQC)
    phred=int(phred)
    qc_shell = ''
    if len(fqlist) == 2:
        fq_1 = fqlist[0]
        fq_2 = fqlist[1]
        qc_shell = '%s  %s %s -o %s\n' %(fastqc,fq_1, fq_2, outQC)
        qc_shell+='python3.6 %s %s %s %s \n'%(Q20,fq_1,outQC,phred)
        qc_shell+='python3.6 %s %s %s %s \n'%(Q20,fq_2,outQC,phred)
    elif len(fqlist) == 1:
        fq_1 = fqlist[0]
        qc_shell = '%s %s -o %s\n' %(fastqc,fq_1, outQC)
        qc_shell+='python3.6 %s %s %s %s \n'%(Q20,fq_1,outQC,phred)
    else:
        #print >>sys.stderr, 'There must be one or two paired-end fastq files!!!'
        print ('There must be one or two paired-end fastq files!!!',sys.stderr)
        sys.exit(0)
    return qc_shell

#---------------trim short reads--------------------#
def Trim(fqlist,phred,lastkeep,out_dir):
    '''trim kept length for fastq list given phred score'''
    out_clean=out_dir+'/02.DataCleaning'
    print ('-'*60+'\n')
    print ('Cleaning fastq is in:',out_clean)
    mkDir(out_clean)
    trim_shell=''
    phred=int(phred)
    fqlist=sorted(fqlist)
    if len(fqlist)==2:
        fq_1=fqlist[0]
        fq_2=fqlist[1]
        trim_1=out_clean+'/trimmed_'+os.path.basename(fq_1)
        trim_2=out_clean+'/trimmed_'+os.path.basename(fq_2)
        trim_shell='fastx_trimmer -v -f 1 -l %s -i %s -o %s -Q %s \n'%(lastkeep,fq_1,trim_1,phred)
        trim_shell+='fastx_trimmer -v -f 1 -l %s -i %s -o %s -Q %s \n'%(lastkeep,fq_2,trim_2,phred)
    elif len(fqlist)==1:
        fq_1=fqlist[0]
        trim_1=out_clean+'/trimmed_'+os.path.basename(fq_1)
        trim_shell='fastx_trimmer -v -f 1 -l %s -i %s -o %s -Q %s \n'%(lastkeep,fq_1,trim_1,phred)
    else:
        #print >>sys.stderr,"'There must be one or two fastq files!!!'"
        print ('There must be one or two paired-end fastq files!!!',sys.stderr)
        sys.exit(0)
    return trim_shell

#--------------cut adapter-------------------#
def rmAdapt(fqlist,adapter,overlap,min_len,out_dir):
    ''' remove adaptor sequence for fastq list given overlap and minimum length'''
    out_clean=out_dir+'/02.DataCleaning'
    mkDir(out_clean)
    if len(fqlist)==2:
        fqlist=sorted(fqlist)
        outfq0=out_clean+'/rmadapter_'+os.path.basename(fqlist[0])
        outfq1=out_clean+'/rmadapter_'+os.path.basename(fqlist[1])
        rmadapt_log=out_clean+'/run.adapter.'+'log'
        rmadapt_shell='%s -a %s -A %s -O %s -m %s -o %s -p %s %s %s 2>>%s\n '%(cutadapt,adapter[0],adapter[1],overlap,min_len,outfq0,outfq1,fqlist[0],fqlist[1],rmadapt_log)
    elif len(fqlist)==1:
        outfq0=out_clean+'/rmadapter_'+os.path.basename(fqlist[0])
        rmadapt_log=out_clean+'/run.adapter.'+'log'
        rmadapt_shell='%s -a %s -O %s -m %s -o %s %s 2>>%s\n '%(cutadapt,adapter[0],overlap,min_len,outfq0,fqlist[0],rmadapt_log)
    else:
        #print >>sys.stderr,r"'There must be one or two fastq files!!!'"
        print ('There must be one or two paired-end fastq files!!!',sys.stderr)
        sys.exit(0)
    return rmadapt_shell

def rmN(fqlist,N_cutoff,out_dir):
    ''' remove N nucleotide for fastq list given cutoff para'''
    out_clean=out_dir+'/02.DataCleaning'
    mkDir(out_clean)
    if len(fqlist)==2:
        fq_1=fqlist[0]
        fq_2=fqlist[1]
        rmN_shell=''
        rmN_shell='python3.6 %s\t%s\t%s\t%s \n'%(removeN,fq_1,N_cutoff,out_clean) 
        rmN_shell+='python3.6 %s\t%s\t%s\t%s \n'%(removeN,fq_2,N_cutoff,out_clean) 
    elif len(fqlist)==1:
        fq_1=fqlist[0]
        rmN_shell=''
        rmN_shell='python3.6 %s\t%s\t%s\t%s \n'%(removeN,fq_1,N_cutoff,out_clean)
    else:
        #print >>sys.stderr,"'There must be one or two fastq files!!!'"
        print ('There must be one or two paired-end fastq files!!!',sys.stderr)
        sys.exit(0)
    return rmN_shell

#--------------filterQ-------------------#
def filterQ(fqlist,phred, minQ,pminQ,out_dir):
    '''filter fastq list with 33 or 64 phred score given minimum quality score and percentage of nucleotide with minimum quality score'''
    out_clean=out_dir+'/02.DataCleaning'
    mkDir(out_clean)
    phred=int(phred)
    if len(fqlist)==2:
        fq_1=fqlist[0]
        fq_2=fqlist[1]
        fq_1_basename=os.path.basename(fq_1)
        fq_2_basename=os.path.basename(fq_2)
        filtQ_1 = out_clean + '/filtQ_' + fq_1_basename
        filtQ_2 = out_clean + '/filtQ_' + fq_2_basename
        filtQ_1_log=out_clean+'/filtlogQ_1'+'.log'
        filtQ_2_log=out_clean+'/filtlogQ_2'+'.log'
        filterQ_shell=''
        filterQ_shell = 'fastq_quality_filter -v -q %s -p %s -i %s -o %s -Q %s >%s \n' %(minQ, pminQ, fq_1, filtQ_1,phred, filtQ_1_log)
        filterQ_shell += 'fastq_quality_filter -v -q %s -p %s -i %s -o %s -Q %s  >%s\n' %(minQ, pminQ, fq_2, filtQ_2,phred, filtQ_2_log)
    elif len(fqlist)==1:
        fq_1=fqlist[0]
        fq_1_basename=os.path.basename(fq_1)
        filtQ_1 = out_clean + '/filtQ_' + fq_1_basename
        filtQ_1_log=out_clean+'/filtlogQ_1'+'.log'
        filterQ_shell=''
        filterQ_shell = 'fastq_quality_filter -v -q %s -p %s -i %s -o %s -Q %s >%s \n' %(minQ, pminQ, fq_1, filtQ_1,phred, filtQ_1_log)
    else:
        #print >>sys.stderr,"'There must be one or two fastq files!!!'"
        print ('There must be one or two paired-end fastq files!!!',sys.stderr)
        sys.exit(0)
    return filterQ_shell

#----------------QC statistics------------------#
def qcStatsh(fqlist,out_dir):
    '''draw bar graph compared with raw fastq and filtered fastq'''
    out_clean=out_dir+'/02.DataCleaning'
    Rstrip=open(out_clean+'/qcStat.R','w')
    if len(fqlist)==2:
        n_fq_rmUnpairedfiltQ_left=n_fq_rmUnpairedfiltQ_right=n_fq_trimmed_left=n_fq_trimmed_right=n_fq_rmadapter_left=n_fq_rmadapter_right=n_fq_remained_left=n_fq_remained_right=n_fq_filtQ_left=n_fq_filtQ_right=0
        fq_trimmed=getFile(out_clean,'trimmed*.fastq') or getFile(out_clean,'trimmed*.fq')
        if not fq_trimmed:
            n_fq_trimmed_left=n_fq_trimmed_right=0
        else:
            n_fq_trimmed_left=CountLines(fq_trimmed[0]).countfile()
            n_fq_trimmed_right=CountLines(fq_trimmed[1]).countfile()
        
        fq_rmadapter=getFile(out_clean,'rmadapter*.fastq') or getFile(out_clean,'rmadapter*.fq')
        if not fq_rmadapter:
            n_fq_rmadapter_left=n_fq_rmadapter_right=0
        else:
            n_fq_rmadapter_left=CountLines(fq_rmadapter[0]).countfile()
            n_fq_rmadapter_right=CountLines(fq_rmadapter[1]).countfile()

        fq_remained=getFile(out_clean,'remained*.fastq') or getFile(out_clean,'remained*.fq')
        if not fq_remained:
            n_fq_remained_left=n_fq_remained_right=0
        else:
            n_fq_remained_left=CountLines(fq_remained[0]).countfile()
            n_fq_remained_right=CountLines(fq_remained[1]).countfile()

        fq_filtQ=getFile(out_clean,'filtQ*.fastq') or getFile(out_clean,'filtQ*.fq')
        if not fq_filtQ:
            n_fq_filtQ_left=n_fq_filtQ_right=0
        else:
            n_fq_filtQ_left=CountLines(fq_filtQ[0]).countfile()
            n_fq_filtQ_right=CountLines(fq_filtQ[1]).countfile()
        
        fq_rmUnpairedfiltQ=getFile(out_clean,'rm2Unpaired*.fastq') or getFile(out_clean,'rm2Unpaired*.fq')
        if not fq_rmUnpairedfiltQ:
            n_fq_rmUnpairedfiltQ_left=n_fq_rmUnpairedfiltQ_right=0
        else:
            n_fq_rmUnpairedfiltQ_left=CountLines(fq_rmUnpairedfiltQ[0]).countfile()
            n_fq_rmUnpairedfiltQ_right=CountLines(fq_rmUnpairedfiltQ[1]).countfile()
        script='library(ggplot2);pdf(file="%s/qcStatistics.pdf")\n'% out_clean
        script+='df <- data.frame(category=c("trimmed_left","rmadapter_left","remained_left","filtQ_left","rm2UnpairedfiltQ_left","trimmed_right","rmadapter_right","remained_right","filtQ_right","rm2UnpairedfiltQ_right"),counts=c(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s));df$category<-as.character(df$category);df$category <- factor(df$category, levels=unique(df$category))\n'%(int(n_fq_trimmed_left),int(n_fq_rmadapter_left),int(n_fq_remained_left),int(n_fq_filtQ_left),int(n_fq_rmUnpairedfiltQ_left),int(n_fq_trimmed_right),int(n_fq_rmadapter_right),int(n_fq_remained_right),int(n_fq_filtQ_right),int(n_fq_rmUnpairedfiltQ_right))
        script+='ggplot(data=df, aes(x=category, y=counts)) +geom_bar(stat="identity", fill="steelblue")+geom_text(aes(label=counts), vjust=1.6, color="white", size=3.5)+ theme(axis.text.x = element_text(angle = 45, hjust = 1))\n'
#        script+='barplot(c(%s,%s,%s,%s,%s,%s,%s,%s),names.arg=c("trimmed_left","rmadapter_left","remained_left","filtQ_left","trimmed_right","rmadapter_right","remained_right","filtQ_right"),las=2)\n'%(int(n_fq_trimmed_left),int(n_fq_rmadapter_left),int(n_fq_remained_left),int(n_fq_filtQ_left),int(n_fq_trimmed_right),int(n_fq_rmadapter_right),int(n_fq_remained_right),int(n_fq_filtQ_right))
        script+='dev.off()\n'
        Rstrip.write('%s\n'%script)
        Rstrip.close()
        Rplot=out_clean+'/qcStat.R'
        qcStat_shell='module load lang/R/3.0.2-goolf-1.4.10 ;Rscript %s\n'% Rplot
    elif len(fqlist)==1:
        n_fq_trimmed=n_fq_rmadapter=n_fq_remained=n_fq_filtQ=0
        fq_trimmed=getFile(out_clean,'trimmed*.fastq') or getFile(out_clean,'trimmed*.fq')
        if not fq_trimmed:
            n_fq_trimmed=0
        else:
            n_fq_trimmed=CountLines(fq_trimmed[0]).countfile()
        
        fq_rmadapter=getFile(out_clean,'rmadapter*.fastq') or getFile(out_clean,'rmadapter*.fq')
        if not fq_rmadapter:
            n_fq_rmadapter=0
        else:
            n_fq_rmadapter=CountLines(fq_rmadapter[0]).countfile()
 
        fq_remained=getFile(out_clean,'remained*.fastq') or getFile(out_clean,'remained*.fq')
        if not fq_remained:
            n_fq_remained=0
        else:
            n_fq_remained=CountLines(fq_remained[0]).countfile()

        fq_filtQ=getFile(out_clean,'filtQ*.fastq') or getFile(out_clean,'filtQ*.fq')
        if not fq_filtQ:
            n_fq_filtQ=0
        else:
            n_fq_filtQ=CountLines(fq_filtQ[0]).countfile()
        script='library(ggplot2);pdf(file="%s/qcStatistics.pdf")\n'% out_clean
        script+='df <- data.frame(category=c("trimmed","rmadapter","remained","filtQ"),counts=c(%s,%s,%s,%s));df$category<-as.character(df$category);df$category <- factor(df$category, levels=unique(df$category))\n'%(int(n_fq_trimmed),int(n_fq_rmadapter),int(n_fq_remained),int(n_fq_filtQ))
        script+='ggplot(data=df, aes(x=category, y=counts)) +geom_bar(stat="identity", fill="steelblue")+geom_text(aes(label=counts), vjust=1.6, color="white", size=3.5)+ theme(axis.text.x = element_text(angle = 45, hjust = 1))\n'
#        script+='barplot(c(%s,%s,%s,%s),names.arg=c("trimmed_left","rmadapter_left","remained_left","filtQ_left"),las=2)\n'%(int(n_fq_trimmed_left),int(n_fq_rmadapter_left),int(n_fq_remained_left),int(n_fq_filtQ_left))
        script+='dev.off()\n'
        Rstrip.write('%s\n'%script)
        Rstrip.close()
        Rplot=out_clean+'/qcStat.R'
        qcStat_shell='module load lang/R/3.0.2-goolf-1.4.10 ;Rscript %s\n'% Rplot
    else:
        #print >>sys.stderr,"'There must be one or two fastq files!!!'"
        print ('There must be one or two paired-end fastq files!!!',sys.stderr)
        sys.exit(0)
    return qcStat_shell

#----------------mapping------------------#
def mappingSeq(fqlist,gtf,hisat2index,orientations,rnastrandness,out_dir):
    '''map fastq with reference genome and create cufflink GTF and HTseq_count txt result'''
    out_aln=out_dir+'/03.Alignment'
    mkDir(out_aln)
    mapping_shell=''
    if len(fqlist)==2:
        fq_1=fqlist[0]
        fq_2=fqlist[1]
        sam=out_aln+'/alignment.sam'
        bam=out_aln+'/alignment.bam'
        samplegtf=out_aln+'/alignment.gtf'
        samlogin=out_aln+'/alignment.alnstats'
#        mapping_shell='%s -o %s --no-coverage-search --transcriptome-index=%s --library-type %s -p 8 %s %s %s \n'%(tophat2,out_aln,transcriptindex,library,ref,fq_1,fq_2)
        if rnastrandness=='unstranded':
            mapping_shell='hisat2 -p %s --dta --%s  -x %s -1 %s -2 %s -S %s 2>%s\n' %(ncore,orientations,hisat2index,fq_1,fq_2,sam,samlogin)
        else:
            mapping_shell='hisat2 -p %s --dta --%s --rna-strandness %s -x %s -1 %s -2 %s -S %s 2>%s\n' %(ncore,orientations,rnastrandness,hisat2index,fq_1,fq_2,sam,samlogin)
        shell_sort='samtools view -S -b %s | samtools sort -@ %s -o %s -\n'%(sam,ncore,bam)
        shell_gtf='stringtie -p %s -G %s -o %s   %s\n'%(ncore, gtf ,samplegtf,bam)
#         features_count=bam.replace('bam','features_count.txt')
#         shell_features_count="featureCounts -a %s -o %s %s \n"%(gtf,features_count,bam)
#         shell_samtools = shell_sort + shell_gtf + shell_features_count
        shell_samtools = shell_sort + shell_gtf
    elif len(fqlist)==1:
        fq_1=fqlist[0]
        sam=out_aln+'/alignment.sam'
        bam=out_aln+'/alignment.bam'
        samplegtf=out_aln+'/alignment.gtf'
        samlogin=out_aln+'/alignment.alnstats'
#        mapping_shell='%s -o %s --no-coverage-search --transcriptome-index=%s --library-type %s -p 8 %s %s %s \n'%(tophat2,out_aln,transcriptindex,library,ref,fq_1,fq_2)
        if rnastrandness=='unstranded':
            mapping_shell='hisat2 -p %s --dta   -x %s -U %s  -S %s 2>%s\n' %(ncore,hisat2index,fq_1,sam,samlogin)
        else:
            mapping_shell='hisat2 -p %s --dta --rna-strandness %s -x %s -U %s  -S %s 2>%s\n' %(ncore,rnastrandness,hisat2index,fq_1,sam,samlogin)
        shell_sort='samtools view -S -b %s | samtools sort -@ %s -o %s -\n'%(sam,ncore,bam)
        shell_gtf='stringtie -p %s -G %s -o %s  %s\n'%(ncore, gtf ,samplegtf,bam)
#         features_count=bam.replace('bam','features_count.txt')
#         shell_features_count="featureCounts -a %s -o %s %s \n"%(gtf,features_count,bam)
#         shell_samtools = shell_sort + shell_gtf + shell_features_count
        shell_samtools = shell_sort + shell_gtf
    else:
        #print >>sys.stderr,"'There must be one or two fastq files!!!'"
        print ('There must be one or two paired-end fastq files!!!',sys.stderr)
        sys.exit(0)
    return mapping_shell+shell_samtools

#----------------Coverage------------------#
def coverGenome(bam, genomebed,windowsize,out_dir):
    '''draw coverage overview graph for alignment file (BAM/SAM)'''
    out_cover=out_dir+'/04.Coverage'
    cover_shell = ''
    mkDir(out_cover)
    cover_genome =out_cover + '/' + os.path.basename(bam).replace('bam', 'cover.genome')
    cover_window=out_cover+'/'+os.path.basename(bam).replace('bam','cover.window')
    window_bed=out_cover+'/'+os.path.basename(bam).replace('bam','window.bed')
    make_window_shell='bedtools makewindows -b %s  -w %s  >%s\n'%(genomebed,windowsize,window_bed)
    cover_shell= 'bedtools coverage -abam %s -b %s >%s\n' %(bam, genomebed, cover_genome)
    cover_shell+='bedtools coverage -abam %s -b %s > %s\n' %(bam,window_bed,cover_window)
    sort_cover=out_cover+'/'+os.path.basename(bam).replace('bam','sorted.cover')
    pdf=out_cover+'/'+os.path.basename(bam).replace('bam','cover.pdf')
    sort_shell ='python %s %s %s\n'% (sortCover,cover_window,sort_cover)
    plot_cover_shell = 'Rscript %s --args %s %s\n' %(ReadMap, sort_cover, pdf)
    return make_window_shell+cover_shell+sort_shell+plot_cover_shell

def main(indir,outdir,phred,qccheck,trim,lastkeep,rmadapt,ladapter,radapter,overlap,min_len,removeN,Ncutoff,filtQ,minQ,pminQ,qcStat,mapping,hisat2index,orientations,rnastrandness,gtf,drawCover,genomebed,windowsize):
    '''main function of rnaseqhs for pipeline'''
    mkDir(outdir)
    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(outdir+'/rnaseq_login.log')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    
    if (not outdir):
        logger.error("outdir is needed!!!!")
        print ("outdir is needed!!!!",sys.stderr)
        sys.exit(0)
        
    for comm in ['gzip','fastx_trimmer','fastqc','fastq_quality_filter','hisat2','stringtie','samtools','bedtools']:
        status=CheckTools(comm).checkit()
        if status!=0:
            logger.error(comm+" is not in your $PATH")
            print (comm+" is not in your $PATH",sys.stderr)
            sys.exit(0)
    
    if '1.3.1' not in str(subprocess.check_output(['samtools;exit 0'],stderr=subprocess.STDOUT,shell=True)):
        logger.error('You need samtools v1.3.1 installed!')
        print ('You need samtools v1.3.1 installed!')
        sys.exit(1)
    
    if 'v2.19' not in str(subprocess.check_output(['bedtools --version'],shell=True)):
        logger.error('You need bedtools v2.19 installed!')
        print ('You need bedtools v2.19 installed!')
        sys.exit(1)
    
    for postfix in ['.1.ht2','.2.ht2','.3.ht2','.4.ht2','.5.ht2','.6.ht2','.7.ht2','.8.ht2']:
        if not os.path.isfile(hisat2index+postfix):
            logger.error('You need correct hisat2 index file(s)!')
            print ('You need correct hisat2 index file(s)!')
            sys.exit(1)

    if not os.path.isfile(gtf):
        logger.error('You need correct gtf file!')
        print ('You need correct gtf file!')
        sys.exit(1)

    if not os.path.isfile(genomebed):
        logger.error('You need correct genomebed file!')
        print ('You need correct genomebed file!')
        sys.exit(1)
        
    logger.info('='*len('Starting processing RNAseq!'))    
    logger.info('Starting processing RNAseq!')
    logger.info('='*len('Starting processing RNAseq!'))
    mkDir(outdir)
    run_log=outdir+'/rnaseq_login.sh'
    fqlist=getFile(indir,'fastq') or getFile(indir,'fq') or getFile(indir,'fq.gz') or getFile(indir,'fastq.gz')
#    sample_name=os.path.basename(indir)
    if not fqlist:
        logger.error("Need .fq .fastq .fq.gz or .fastq.gz file(s)!")
        print ("Need .fq .fastq .fq.gz or .fastq.gz file(s)!",sys.stderr)
        sys.exit(0)

    if len(fqlist)==1 and (re.compile(r'\.fq\.gz$').findall(fqlist[0]) or re.compile(r'\.fastq\.gz$').findall(fqlist[0])):
        fqlist_gz=fqlist[0]
        fqlist[0]=fqlist[0].replace('.gz','')
        logger.info('-'*100)
        logger.info("gzip process start...")
        logger.info("COMMAND: "+('gzip -dc %s >%s\n'%(fqlist_gz,fqlist[0])))
        status=subprocess.call('gzip -dc %s >%s\n'%(fqlist_gz,fqlist[0]),shell=True)
        if status !=0:
            logger.error("gzip can NOT process .fq.gz or .fastq.gz file(s)!")
            print ("gzip can NOT process .fq.gz or .fastq.gz file(s)!",sys.stderr)
            sys.exit(0)
        else:
            logger.info("gzip process .fq.gz or .fastq.gz file(s) successfully!")
            logger.info('-'*100)
            print ("gzip process .fq.gz or .fastq.gz file(s) successfully!" )                   
    elif len(fqlist)==2 and (re.compile(r'\.fq\.gz$').findall(fqlist[0]) or re.compile(r'\.fastq\.gz$').findall(fqlist[0])) and (re.compile(r'\.fq\.gz$').findall(fqlist[1]) or re.compile(r'\.fastq\.gz$').findall(fqlist[1])):
        fqlist_gz=[]
        fqlist_gz.append(fqlist[0])
        fqlist_gz.append(fqlist[1])
        fqlist[0]=fqlist[0].replace('.gz','')
        fqlist[1]=fqlist[1].replace('.gz','')
        logger.info('-'*100)
        logger.info("gzip process start...")
        logger.info("COMMAND: "+('gzip -dc %s >%s\n'%(fqlist_gz[0],fqlist[0]))+('gzip -dc %s >%s\n'%(fqlist_gz[1],fqlist[1])))
        status1=subprocess.call('gzip -dc %s >%s\n'%(fqlist_gz[0],fqlist[0]),shell=True)
        status2=subprocess.call('gzip -dc %s >%s\n'%(fqlist_gz[1],fqlist[1]),shell=True)
        if status1 !=0 or status2!=0:
            logger.error("gzip can NOT process .fq.gz or .fastq.gz file(s)!")
            print ("gzip can NOT process .fq.gz or .fastq.gz file(s)!",sys.stderr)
            sys.exit(0)
        else:
            logger.info("gzip process .fq.gz or .fastq.gz file(s) successfully!")
            logger.info('-'*100)
            print ("gzip process .fq.gz or .fastq.gz file(s) successfully!" )
    else:
        pass
    
    fqlist=sorted(fqlist)
    logger.info('Original fastq list is :'+' '.join(fqlist))
    print ('-'*60)
    print ('Original fastq list is :',fqlist  )      

    if re.search('true',trim,re.I):
        phred=int(phred)
        lastkeep=int(lastkeep)
        shell_trim=Trim(fqlist,phred,lastkeep,outdir)
        WriteLoginStart(run_log,'Trim').writefile()
        logger.info('-'*100)
        logger.info("Trim process start...")
        logger.info("COMMAND: "+shell_trim)
        sp=subprocess.Popen(shell_trim,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        status=sp.wait()
        sp_stdout,sp_stderr= sp.communicate()    
        if status !=0 :
            logger.error(sp_stderr)
            logger.error("Trim can NOT process fastq file(s)!")
            print ("Trim can NOT process fastq file(s)!",sys.stderr)
            sys.exit(0)
        else:
            logger.info(sp_stdout)
            logger.info("Trim process fastq file(s) successfully!")
            logger.info('-'*100)
            print ("Trim process fastq file(s) successfully!"  )  
        WriteLogin(run_log,'Trim',shell_trim,status).writefile()
        out_clean=outdir+'/02.DataCleaning'
        fqlist=getFile(out_clean,'trimmed*fastq') or getFile(out_clean,'trimmed*fq')
        print ('-'*60+'\n')
        fqlist=sorted(fqlist)
        logger.info('Trimmed fastq file is:'+' '.join(fqlist))
        print ('Trimmed fastq file is:',fqlist)

    if re.search('true',qccheck,re.I):
        phred=int(phred)
        qc_shell=QC(fqlist,phred,outdir)
        WriteLoginStart(run_log,'QC').writefile() 
        #status=os.system(qc_shell)
        logger.info('-'*100)
        logger.info("QC process start...")
        logger.info("COMMAND: "+qc_shell)
        sp=subprocess.Popen(qc_shell,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        status=sp.wait()
        sp_stdout,sp_stderr= sp.communicate() 
#        status=subprocess.call(qc_shell,shell=True)
        if status !=0 :
            logger.error(sp_stderr)
            logger.error("QC can NOT process fastq file(s)!")
            print ("QC can NOT process fastq file(s)!",sys.stderr)
            sys.exit(0)
        else:
            logger.info(sp_stdout)
            logger.info("QC process fastq file(s) successfully!")
            logger.info('-'*100)
            print ("QC process fastq file(s) successfully!"  )
        WriteLogin(run_log,'QC',qc_shell,status).writefile()
     
    if re.search('true', rmadapt, re.I):
        out_clean=outdir+'/02.DataCleaning'
        leftadapt=ladapter
        rightadapt=radapter
        min_len=int(min_len)
        overlen=int(overlap)
        if len(fqlist)==2:
            fq_Unpaired=[]
            fq_Unpaired.append(out_clean+'/rmUnpaired_'+os.path.basename(fqlist[0]))
            fq_Unpaired.append(out_clean+'/rmUnpaired_'+os.path.basename(fqlist[1]))
            RmUnpaired(fqlist,fq_Unpaired).rmUnpaired()
            fqlist=fq_Unpaired
        rmadapt_shell=rmAdapt(fqlist,[leftadapt,rightadapt],overlap,min_len,outdir)+'\n'
        WriteLoginStart(run_log,'rmadapt').writefile()
        #status = os.system(rmadapt_shell)
        logger.info('-'*100)
        logger.info("rmadapt process start...")
        logger.info("COMMAND: "+rmadapt_shell)
        sp=subprocess.Popen(rmadapt_shell,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        status=sp.wait()
        sp_stdout,sp_stderr= sp.communicate() 
        if status !=0 :
            logger.error(sp_stderr)
            logger.error("rmadapt can NOT process fastq file(s)!")
            print("rmadapt can NOT process fastq file(s)!",sys.stderr)
            sys.exit(0)
        else:
            logger.info(sp_stdout)
            logger.info("rmadapt process fastq file(s) successfully!")
            logger.info('-'*100)
            print ("rmadapt process fastq file(s) successfully!" ) 
        WriteLogin(run_log,'rmadapt',rmadapt_shell,status).writefile()
        fqlist=getFile(out_clean,'rmadapter*fastq') or getFile(out_clean,'rmadapter*fq')
        print ('-'*60+'\n')
        fqlist=sorted(fqlist)
        logger.info('rmadapter fastq file is:'+' '.join(fqlist))
        print ('rmadapter fastq file is:',fqlist)
            
    if re.search('true', removeN, re.I):
        N_cutoff=Ncutoff
        removeN_shell=rmN(fqlist,N_cutoff,outdir)
        WriteLoginStart(run_log,'removeN').writefile()
        #status = os.system(removeN_shell)
        logger.info('-'*100)
        logger.info("removeN process start...")
        logger.info("COMMAND: "+removeN_shell)
        sp=subprocess.Popen(removeN_shell,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        status=sp.wait()
        sp_stdout,sp_stderr= sp.communicate() 
#        status=subprocess.call(removeN_shell,shell=True)
        if status !=0 :
            logger.error(sp_stderr)
            logger.error("removeN can NOT process fastq file(s)!")
            print ("removeN can NOT process fastq file(s)!",sys.stderr)
            sys.exit(0)
        else:
            logger.info(sp_stdout)
            logger.info("removeN process fastq file(s) successfully!")
            logger.info('-'*100)
            print ("removeN process fastq file(s) successfully!" )
        WriteLogin(run_log,'removeN',removeN_shell,status).writefile()
        out_qc = outdir + '/02.DataCleaning'
        fqlist = getFile(out_qc, 'remained*fastq') or getFile(out_clean,'remained*fq')
        print ('-'*60)
        fqlist=sorted(fqlist)
        logger.info('removeN remained fq file is: '+' '.join(fqlist))
        print ('removeN remained fq file is: ',fqlist)

    if re.search('true', filtQ, re.I):
        phred=int(phred)
        minQ=int(minQ)
        pminQ=int(pminQ)
        filterQ_shell=filterQ(fqlist,phred,minQ,pminQ,outdir)
        WriteLoginStart(run_log,'filtQ').writefile()
        #status = os.system(filterQ_shell)
        logger.info('-'*100)
        logger.info("filtQ process start...")
        logger.info("COMMAND: "+filterQ_shell)
        sp=subprocess.Popen(filterQ_shell,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        status=sp.wait()
        sp_stdout,sp_stderr= sp.communicate() 
#        status=subprocess.call(filterQ_shell,shell=True)
        if status !=0 :
            logger.error(sp_stderr)
            logger.error("filterQ can NOT process fastq file(s)!")
            print ("filterQ can NOT process fastq file(s)!",sys.stderr)
            sys.exit(0)
        else:
            logger.info(sp_stdout)
            logger.info("filterQ process fastq file(s) successfully!")
            logger.info('-'*100)
            print ("filterQ process fastq file(s) successfully!" )
        WriteLogin(run_log,'filtQ',filterQ_shell,status).writefile()
        out_qc = outdir + '/02.DataCleaning'
        fqlist = getFile(out_qc, 'filtQ*fastq') or getFile(out_clean,'filtQ*fq')
        print ('-'*60)
        fqlist=sorted(fqlist)
        logger.info('filterQ fqlist is: '+' '.join(fqlist))
        print ('filterQ fqlist is: ',fqlist)
        if len(fqlist)==2:
            fq_Unpaired=[]
            fq_Unpaired.append(out_clean+'/rm2Unpaired_'+os.path.basename(fqlist[0]))
            fq_Unpaired.append(out_clean+'/rm2Unpaired_'+os.path.basename(fqlist[1]))
            RmUnpaired(fqlist,fq_Unpaired).rmUnpaired()
            fqlist=fq_Unpaired
            WriteLogin(run_log,'PairedfiltQ','RmUnpaired(%s,%s).rmUnpaired()'%(fqlist,fq_Unpaired),status).writefile()
            print ('-'*60)
            fqlist=sorted(fqlist)
            logger.info('PairedfilterQ fqlist is: '+' '.join(fqlist))
            print ('PairedfilterQ fqlist is: ',fqlist)

    if re.search('true', qcStat, re.I):
        qcStat_shell=qcStatsh(fqlist,outdir)
        phred=int(phred)
        qc_shell=QC(fqlist,phred,outdir)
        qcStat_shell=qcStat_shell+"\n"+qc_shell+"\n"
        WriteLoginStart(run_log,'qcStat').writefile()
        #status = os.system(qcStat_shell)
        logger.info('-'*100)
        logger.info("qcStat process start...")
        logger.info("COMMAND: "+qcStat_shell)
        sp=subprocess.Popen(qcStat_shell,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        status=sp.wait()
        sp_stdout,sp_stderr= sp.communicate() 
#        status=subprocess.call(qcStat_shell,shell=True)        
        if status !=0 :
            logger.error(sp_stderr)
            logger.error("qcStat can NOT process fastq file(s)!")
            print ("qcStat can NOT process fastq file(s)!",sys.stderr)
            sys.exit(0)
        else:
            logger.info(sp_stdout)
            logger.info("qcStat process fastq file(s) successfully!")
            logger.info('-'*100)
            print ("qcStat process fastq file(s) successfully!" )
        WriteLogin(run_log,'qcStat',qcStat_shell,status).writefile()

    if re.search('true', mapping, re.I):
        mapping_shell = mappingSeq(fqlist,gtf,hisat2index,orientations,rnastrandness,outdir)
        WriteLoginStart(run_log,'mapping').writefile()
        #status = os.system(mapping_shell)
        logger.info('-'*100)
        logger.info("mapping process start...")
        logger.info("COMMAND: "+mapping_shell)
        sp=subprocess.Popen(mapping_shell,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        status=sp.wait()
        sp_stdout,sp_stderr= sp.communicate() 
#        status=subprocess.call(mapping_shell,shell=True)
        if status !=0 :
            logger.error(sp_stderr)
            logger.error("mapping can NOT process fastq file(s)!")
            print ("mapping can NOT process fastq file(s)!",sys.stderr)
            sys.exit(0)
        else:
            logger.info(sp_stdout)
            logger.info("mapping process fastq file(s) successfully!")
            logger.info('-'*100)
            print ("mapping process fastq file(s) successfully!" )
        WriteLogin(run_log,'mapping',mapping_shell,status).writefile()
        out_aln = outdir + '/03.Alignment'
        bam_file = getFile(out_aln, '.bam')[0]
        print ('-'*60)
        logger.error('clean bam file is: '+bam_file)
        print ('clean bam file is: ',bam_file)

    if re.search('true', drawCover,re.I):
        genome_bed = genomebed
        window_size=windowsize
        bam = getFile(out_aln, '.bam')[0]
        if not genome_bed:
            print ('The genomebed file is needed for genome option!!!')
            sys.exit(0)
        coverGenome_shell = coverGenome(bam,  genome_bed,window_size,outdir)
        WriteLoginStart(run_log,'drawCover').writefile()
        #status = os.system(coverGenome_shell)
        logger.info('-'*100)
        logger.info("drawCover process start...")
        logger.info("COMMAND: "+coverGenome_shell)
        sp=subprocess.Popen(coverGenome_shell,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        status=sp.wait()
        sp_stdout,sp_stderr= sp.communicate() 
#        status=subprocess.call(coverGenome_shell,shell=True)
        if status !=0 :
            logger.error(sp_stderr)
            logger.error("drawCover can NOT process fastq file(s)!")
            print ("drawCover can NOT process fastq file(s)!",sys.stderr)
            sys.exit(0)
        else:
            logger.info(sp_stdout)
            logger.info("drawCover process fastq file(s) successfully!")
            logger.info('-'*100)
            print ("drawCover process fastq file(s) successfully!" )
        WriteLogin(run_log,'drawCover',coverGenome_shell,status).writefile()
        print ('-'*100)
#        logger.info('drawCover is done.')
        print ('drawCover is done.')
        logger.info('='*len('Finishing processing RNAseq!'))
        logger.info('Finishing processing RNAseq!')
        logger.info('='*len('Finishing processing RNAseq!'))
