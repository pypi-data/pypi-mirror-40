import os
from ..config import get_config
from ..process import run_cmd

markdup_cmd_script ="""
{java} -Djava.io.tmpdir={tmpdir} -Xmx{memory} -jar {picard} MarkDuplicates INPUT={bamfile} OUTPUT={markedbam} METRICS_FILE={markedbam}.metrics
{samtools} index {markedbam}
"""

def run_markdup(bamfile, markedbam, memory, tmpdir, config):
    """
    Run MarkDuplicates of Picard. this function tags duplicate reads with "markduplicate" in BAM file.
    See also MarkDuplicates_ in gatk.

    .. _MarkDuplicates: https://software.broadinstitute.org/gatk/documentation/tooldocs/current/picard_sam_markduplicates_MarkDuplicates.php

    The config file should be provided:
    ::
        [SNV]
        java = /path/to/java
        picard = /path/to/picard.jar
        
    Usage:
    ::
      baseqSNV markdup -b Sample.bam -m Sample.marked.bam -d ./tmp -c config.ini 

    Return:
    metrics file indicates the numbers of duplicates for both single- and paired-end reads
    ::
      Sample.marked.bam
      Sample.marked.bam.bai
      Sample.marked.bam.metrics
    """
    java = get_config("SNV", "java", config)
    picard = get_config("SNV", "picard", config)
    samtools = get_config("SNV", "samtools", config)
    
    if not os.path.exists(tmpdir):
        os.makedirs(tmpdir)

    cmd = markdup_cmd_script.format(java=java, picard=picard, samtools=samtools, 
        markedbam=markedbam, bamfile=bamfile, memory=memory,tmpdir=tmpdir)
    run_cmd("Mark duplicates","".join(cmd))

    return cmd