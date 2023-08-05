from unittest import TestCase
from ..rnaseqhs import main

class TestConsole(TestCase):
    def test_paired_end(self):
        main('./rnaseqhs/tests/test_data/in2','./rnaseqhs/tests/test_data/out2',33,'true','true',77,'true','AGATCGGAAGAGC','AGATCGGAAGAGC',6,40,'true',0.1,'true',20,80,'true','true','./rnaseqhs/genome/refrence/HISAT2Index/chrX_tran','fr','unstranded','./rnaseqhs/genome/refrence/HISAT2Index/chrX.gtf','true','./rnaseqhs/genome/genome.bed',50000)
    def test_single_end(self):
        main('./rnaseqhs/tests/test_data/in','./rnaseqhs/tests/test_data/out',33,'true','true',77,'true','AGATCGGAAGAGC','AGATCGGAAGAGC',6,40,'true',0.1,'true',20,80,'true','true','./rnaseqhs/genome/refrence/HISAT2Index/chrX_tran','fr','unstranded','./rnaseqhs/genome/refrence/HISAT2Index/chrX.gtf','true','./rnaseqhs/genome/genome.bed',50000)
