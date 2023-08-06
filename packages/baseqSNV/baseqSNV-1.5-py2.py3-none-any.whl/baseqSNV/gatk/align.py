import os
from ..config import get_config
from ..process import run_cmd

bwa_cmd_script_p = r"""{bwa} mem -t {thread} -M -R "@RG\tID:{sample}\tSM:{sample}\tLB:WES\tPL:Illumina" {genome} {fq1} {fq2}  1>{samfile}"""
bwa_cmd_script_s = r"""{bwa} mem -t {thread} -M -R "@RG\tID:{sample}\tSM:{sample}\tLB:WES\tPL:Illumina" {genome} {fq1} 1>{samfile}"""

sort_index_cmd_script = """
{samtools} view -bS {samfile} > {viewedbam}
{samtools} sort -@ 8 {viewedbam} -o {sample}.bam
{samtools} index {sample}.bam
rm {samfile} {viewedbam}
"""

def alignment(fq1, fq2, sample, genome, thread=8, config=""):
    """
    Map FASTQ files to genome using BWA aligner. 
    
    Add ReadGroup_ to bamfile using the input sample name.
    Outfile is in BAM format and indexed for the downstream analysis.

    A bam file and its index will be genrated:
    ::
      <sample>.bam
      <sample>.bam.bai

    .. _ReadGroup: https://software.broadinstitute.org/gatk/documentation/article.php?id=6472

    Usage:
    ::
      A config file should be provided:
      [SNV]
      bwa = /home/soft/bin/bwa
      samtools = /home/soft/bin/samtools

      [SNV_ref_hg19]
      bwa_index = /home/ref/hg19.fa

      #Run using the command line:
      baseqSNV align -1 test.1.fq.gz -2 test.2.fq.gz -n Sample -c config.ini -g hg38
      
      #Call as function:
      from baseqSNV import alignment
      alignment("sample.1.fq.gz", "sample.2.fq.gz", "Sample", "hg19", "config.ini")

    """
    bwa = get_config("SNV", "bwa", config)
    samtools = get_config("SNV", "samtools", config)
    genome = get_config("SNV_ref_"+genome, "bwa_index", config)
    viewedbam = sample + ".view.bam"
    samfile = sample + ".sam"
    
    if fq1 and fq2 and os.path.exists(fq1) and os.path.exists(fq2):
        bwa_cmd = bwa_cmd_script_p.format(bwa=bwa, sample=sample, genome=genome, fq1=fq1, fq2=fq2, samfile=samfile, thread=thread)
    elif fq1 and os.path.exists(fq1):
        bwa_cmd = bwa_cmd_script_s.format(bwa=bwa, sample=sample, genome=genome, fq1=fq1, samfile=samfile, thread=thread)
    sort_index_cmd=sort_index_cmd_script.format(samtools=samtools, sample=sample, samfile=samfile,viewedbam=viewedbam)
    run_cmd("bwa alignment", "".join(bwa_cmd))
    run_cmd("samtools sort", "".join(sort_index_cmd))
    return bwa_cmd+"\n"+sort_index_cmd