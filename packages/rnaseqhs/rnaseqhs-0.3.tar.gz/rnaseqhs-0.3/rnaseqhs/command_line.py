from . import rnaseqhs
import sys
import argparse

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('-i','--indir',help = 'fastq files path')
    parser.add_argument('-o','--outdir',help = 'output path')
    parser.add_argument('-P','--phred',help = 'phred score used in platform [33]',default=33,type=int) 
    parser.add_argument('-Q','--qccheck',help='do quality check [true]',default='true')
    parser.add_argument('-T','--trim',help = 'trim given fastq short reads as --lastkeep defined')
    parser.add_argument('-l','--lastkeep',help = 'with "trim" option, last bases to keep',default=100,type=int)
    parser.add_argument('-r','--rmadapt',help='remove adapter [true]',default='true')
    parser.add_argument('-L','--ladapter',help='left adapter [AGATCGGAAGAGC]',default='AGATCGGAAGAGC')
    parser.add_argument('-R','--radapter',help='right adapter [AGATCGGAAGAGC]',default='AGATCGGAAGAGC')
    parser.add_argument('-O','--overlap',help='If the overlap between the read and adapter is shorter than the overlap length, the read will NOT be modified. [6]',default=6, type=int)
    parser.add_argument('-m','--minlen', help = 'Discard trimmed reads that are shorter than "minlen" [75]', default = 75,type=int)
    parser.add_argument('-N', '--removeN', help='remove "N" bases [true]', default = 'true')
    parser.add_argument('-c','--Ncutoff', help='with "removeN" option, N cutoff [0.1]', default = "0.1",type=float)
    parser.add_argument('-F', '--filtQ', help = 'Filters sequences based on quality [true]', default = 'true')
    parser.add_argument( '--minQ', help = 'Minimum quality score to keep [20]', default = 20,type=int)
    parser.add_argument( '--pminQ', help = 'Minimum percent of bases [80]', default = 80,type=int)
    parser.add_argument('-q','--qcStat',help='generate QC statistic plot for seq',default='true')
    parser.add_argument('-M', '--mapping', help='read mapping [true]', default = 'true')
    parser.add_argument('--hisat2index', help='hisat2 index')
    parser.add_argument( '--orientations', help = 'orientations',default='fr')
    parser.add_argument( '--rnastrandness', help = 'rna strandness',default='unstranded')
    parser.add_argument( '--gtf', help = 'gtf file for annotation')
    parser.add_argument('--drawCover', help = 'coverage of genome region [true]', default ='true')
    parser.add_argument( '--genomebed', help = 'coverage genome bed file')
    parser.add_argument( '--windowsize', help = 'coverage window size [500000]', default = 500000,type=int)

    args=parser.parse_args()
    indir=args.indir
    outdir=args.outdir
    phred=int(args.phred)
    qccheck=args.qccheck
    trim=args.trim
    lastkeep=int(args.lastkeep)
    rmadapt=args.rmadapt
    ladapter=args.ladapter
    radapter=args.radapter
    overlap=args.overlap
    minlen=args.minlen
    removeN=args.removeN
    Ncutoff=args.Ncutoff
    filtQ=args.filtQ
    minQ=args.minQ
    pminQ=args.pminQ
    qcStat=args.qcStat
    mapping=args.mapping
    hisat2index=args.hisat2index
    orientations=args.orientations
    rnastrandness=args.rnastrandness
    gtf=args.gtf
    drawCover=args.drawCover
    genomebed=args.genomebed
    windowsize=args.windowsize

    if len(sys.argv)>1:
        rnaseqhs.main(indir=indir,outdir=outdir,phred=phred,qccheck=qccheck,trim=trim,lastkeep=lastkeep,rmadapt=rmadapt,ladapter=ladapter,radapter=radapter,overlap=overlap,min_len=minlen,removeN=removeN,Ncutoff=Ncutoff,filtQ=filtQ,minQ=minQ,pminQ=pminQ,qcStat=qcStat,mapping=mapping,hisat2index=hisat2index,orientations=orientations,rnastrandness=rnastrandness,gtf=gtf,drawCover=drawCover,genomebed=genomebed,windowsize=windowsize)
    else:
        print ('version %s'%rnaseqhs.__version__)
        print ('Type "-h" or "--help" for more help')
        sys.exit(0)
