from ..config import get_config
from ..process import run_cmd

selectvar_cmd_script = """
{gatk} SelectVariants -R {index} -V {rawvcf} --select-type-to-include SNP -O {selectvcf}
{gatk} VariantFiltration -R {index} -V {selectvcf} -O {filtervcf} --filter-expression "QD < 2.0 || FS > 60.0 || MQ < 40.0" --filter-name "my_snp_filter"
"""

def selectvar(rawvcf,selectvcf,filtervcf,genome,run=True):
    """
    This function selects SNPs from a VCF file which is usually the output file of
    HaplotypeCaller. Then, all SNPs are filtered by certain criteria based on INFO and/or FORMAT annotations.
    Criteria used here is "QD < 2.0 || FS > 60.0 || MQ < 40.0".
    More details about SelectVariants_ and VariantFiltration_

    .. _SelectVariants: https://software.broadinstitute.org/gatk/documentation/tooldocs/current/org_broadinstitute_hellbender_tools_walkers_variantutils_SelectVariants.php
    .. _VariantFiltration: https://software.broadinstitute.org/gatk/documentation/tooldocs/current/org_broadinstitute_hellbender_tools_walkers_filters_VariantFiltration.php

    Usage:
    ::
      baseqSNV selectvar -r Test.raw.indel.snp.vcf -s Test.raw.snp.vcf -f Test.filtered.snp.vcf -g hg38

    Return:
    ::
      Test.raw.snp.vcf
      Test.filtered.snp.vcf
    """
    GATK = get_config("SNV", "GATK")
    index = get_config("SNV_ref_" + genome, "bwa_index")
    selectvar_cmd = selectvar_cmd_script.format(gatk=GATK,index=index,rawvcf=rawvcf,selectvcf=selectvcf,filtervcf=filtervcf)
    if run:
        run_cmd("SelectVariants","".join(selectvar_cmd))
    return selectvar_cmd

##filt mutect vcf
filtertable_cmd_script = """
{gatk} GetPileupSummaries -I {tumorbam} -V {resource} -O {gps_table}
{gatk} CalculateContamination -I {gps_table} -O {calcontam_table}
"""
def get_filter_table(tumorbam, resource, gps_table, calcontam_table):
    gatk = get_config("SNV","GATK")
    filtertable_cmd = filtertable_cmd_script.format(gatk=gatk, tumorbam=tumorbam, resource=resource, gps_table=gps_table,
                                                    calcontam_table=calcontam_table)
    run_cmd("obatin filter table for mutect calls","".join(filtertable_cmd))


filtercall_cmd_script = """
{gatk} FilterMutectCalls -V {somaticvcf} --contamination-table {calcontam_table} -O {filter_call}
"""
def filter_mutect_vcf(somaticvcf,calcontam_table,filter_call):
    gatk = get_config("SNV","GATK")
    filtercall_cmd = filtercall_cmd_script.format(gatk=gatk, somaticvcf=somaticvcf, calcontam_table=calcontam_table,
                                                    filter_call=filter_call)
    run_cmd("filter mutect calls using contamination table","".join(filtercall_cmd))

