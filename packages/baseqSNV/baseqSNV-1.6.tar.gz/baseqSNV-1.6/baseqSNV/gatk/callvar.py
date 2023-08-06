import os
from ..config import get_config
from ..process import run_cmd

callvar_cmd_script = """
export PATH=$PATH:{java}
{gatk} --java-options "-Xmx4g" HaplotypeCaller -R {index} -L {interval} -I {bqsrbam} -O {rawvcf} -bamout bamout.bam --native-pair-hmm-threads 20 {extrainfos}
"""

def run_callvar(bqsrbam, rawvcf, genome, config, interval, disable_dup_filter = False):
    """
    Call germline SNPs and indels via local re-assembly of haplotypes. "bqsrbam" file recalbrated by BQSR do recommand as
    input BAM file and this functin only run the single sample genotypeVCF calling. More details see also
    HaplotypeCaller_

    .. _HaplotypeCaller: https://software.broadinstitute.org/gatk/documentation/tooldocs/current/org_broadinstitute_hellbender_tools_walkers_haplotypecaller_HaplotypeCaller.php

    Usage:
    ::
      baseqSNV callvar -q Sample.marked.bqsr.bam -r Sample.raw.indel.snp.vcf -g hg38 -c config.ini -i interval.bed

    Return:
    ::
      Test.raw.indel.snp.vcf

    """
    GATK = get_config("SNV", "GATK", config)
    index = get_config("SNV_ref_" + genome, "bwa_index", config)
    java = get_config("SNV", "java", config)
    java_dir = os.path.dirname(java)

    extra = ""

    if disable_dup_filter:
        extra = "--disable-read-filter NotDuplicateReadFilter"
    
    callvar_cmd = callvar_cmd_script.format(gatk=GATK, index=index, 
        interval=interval, bqsrbam=bqsrbam, rawvcf=rawvcf, extrainfos=extra, java=java_dir)
    run_cmd("call variants","".join(callvar_cmd))
    print("[INFO] The VCF is generated in:" + rawvcf)
    return callvar_cmd