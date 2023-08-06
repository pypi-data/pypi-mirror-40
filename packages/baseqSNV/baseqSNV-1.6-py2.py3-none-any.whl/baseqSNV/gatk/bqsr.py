import os
from ..config import get_config
from ..process import run_cmd

bqsr_cmd_script = """
export PATH=$PATH:{java}
{gatk} BaseRecalibrator -R {index} -L {interval} -I {markedbam} --known-sites {dbsnp} --known-sites {snp} --known-sites {indel} -O {markedbam}.table
{gatk} ApplyBQSR -R {index} -L {interval} -I {markedbam} -bqsr {markedbam}.table -O {bqsrbam}
"""

bqsr_cmd_script_DRF = """
export PATH=$PATH:{java}
{gatk} BaseRecalibrator -R {index} -L {interval} -I {markedbam} --known-sites {dbsnp} --known-sites {snp} --known-sites {indel} --disable-read-filter NotDuplicateReadFilter -O {markedbam}.table
{gatk} ApplyBQSR -R {index} -L {interval} -I {markedbam} -bqsr {markedbam}.table --disable-read-filter NotDuplicateReadFilter -O {bqsrbam}
"""

def bqsr(markedbam, bqsrbam, genome, config, interval, disable_dup_filter=False):
    """
    Run BQSR_. This function performs the two-steps process called base quality score recalibration. the first
    ster generates a recalibration table based on various covariates which is recruited to the second step to
    correct the systematic bias in input BAM file. More details about BaseRecalibrator_ and ApplyBQSR_ .

    .. _BQSR: https://gatkforums.broadinstitute.org/gatk/discussion/44/base-quality-score-recalibration-bqsr
    .. _BaseRecalibrator: https://software.broadinstitute.org/gatk/documentation/tooldocs/current/org_broadinstitute_hellbender_tools_walkers_bqsr_BaseRecalibrator.php
    .. _ApplyBQSR: https://software.broadinstitute.org/gatk/documentation/tooldocs/current/org_broadinstitute_hellbender_tools_walkers_bqsr_ApplyBQSR.php

    Usage:
    
    * Default mode filters duplicate reads (reads with "markduplicate" tags) before applying BQSR
      ::
        baseqSNV bqsr -m Sample.marked.bam -g hg38 -q Sample.marked.bqsr.bam -i interval.bed -c config.ini

    * Disable reads filter before analysis (to keep all duplicated reads for further analysis).
      ::
        baseqSNV bqsr -m Sample.marked.bam -g hg38 -q Sample.marked.bqsr.bam -i interval -f Yes

    The following files will be generated:
    ::
      Sample.marked.bam.table
      Sample.marked.bqsr.bai
      Sample.marked.bqsr.bam
    """

    gatk = get_config("SNV", "GATK", config)
    java = get_config("SNV", "java", config)
    index = get_config("SNV_ref_"+genome, "bwa_index", config)
    DBSNP = get_config("SNV_ref_"+genome, "dbSNP", config)
    SNP = get_config("SNV_ref_"+genome, "SNP", config)
    INDEL = get_config("SNV_ref_"+genome,"INDEL", config)

    java_dir = os.path.dirname(java)
  
    #Default, we use the read filter...
    if not disable_dup_filter:
        bqsr_cmd = bqsr_cmd_script.format(gatk=gatk, index=index, interval=interval, markedbam=markedbam,
                                          bqsrbam=bqsrbam, dbsnp=DBSNP, snp=SNP, indel=INDEL, java=java_dir)
    #We can also disable the read filter...
    else:
        bqsr_cmd = bqsr_cmd_script_DRF.format(gatk=gatk, index=index, interval=interval, markedbam=markedbam,
                                          bqsrbam=bqsrbam, dbsnp=DBSNP, snp=SNP, indel=INDEL, java=java_dir)
    run_cmd("BaseRecalibrator","".join(bqsr_cmd))