import os
from ..config import get_config
from ..process import run_cmd

mutect2_cmd_simplified_script="""
{gatk} Mutect2 -R {index} -I {normalbam} -normal {normalname} -I {tumorbam} -tumor {tumorname} -O {vcffile}
"""
mutect2_cmd_stardand_script="""
{gatk} Mutect2 -R {index} -I {normalbam} -normal {normalname} -I {tumorbam} -tumor {tumorname} \
  --germline-resource {germline} \
  --panel-of-normals {pon} \
  -O {vcffile}
"""
def mutect2(genome, normalname, normalbam, tumorname, tumorbam, vcffile, pon, germline):
    """Mutect2_ is aim to call somatic SNVs and indels via local assembly of haplotypes.
    This function requires both tumor BAM file and its matched normal BAM file. tumorname and normalname should be consistent with the ReadGroup(ID) of tumor
    BAM file and normal BAM file respectively. PoN is refer to panel of normals callset(more infomation about PoN and how to
    create it, please see PoN_ ). Germline resource, also in VCF format, is used to annotate variant alleles. Download germline_ resource.

    .. _mutect2: https://software.broadinstitute.org/gatk/documentation/tooldocs/current/org_broadinstitute_hellbender_tools_walkers_mutect_Mutect2.php
    .. _germline: https://software.broadinstitute.org/gatk/download/bundle
    .. _PoN: https://software.broadinstitute.org/gatk/documentation/tooldocs/current/org_broadinstitute_hellbender_tools_walkers_mutect_CreateSomaticPanelOfNormals.php

    Usage:

    * Simplified Mutect2 command line
      ::
        # single sample
        baseq-SNV run_mutect2 -g hg37 -n normal -N normal_marked_bqsr.bam \\
                                      -t tumor -T tumor_marked_bqsr.bam -o ./
        # multiple samples
        baseq-SNV run_mutect2 -g hg37 -l sample_list.txt -o ./

    * Specify PoN(panels of normals) VCF file and germline VCF file.
      Default germline VCF file comes form gatk resource bundle and is recruited if germline isn't designated.
      ::
        # single sample
        baseq-SNV run_mutect2 -g hg37 -n normal -N normal_marked_bqsr.bam \\
                                      -t tumor -T tumor_marked_bqsr.bam -o ./ \\
                                      -p pon.vcf.gz -G af-only-gnomad.raw.sites.b37.vcf.gz
        # multiple samples
        baseq-SNV run_mutect2 -g hg37 -l sample_list.txt -o ./ \\
                                      -p pon.vcf.gz -G af-only-gnomad.raw.sites.b37.vcf.gz

    """

    gatk = get_config("SNV","GATK")
    index = get_config("SNV_ref_" + genome, "bwa_index")
    if pon :
        if not germline:
            germline = get_config("SNV_ref_" + genome, "germline")
            mutect2_cmd = mutect2_cmd_stardand_script.format(gatk=gatk, index=index, normalbam=normalbam,
                                                             normalname=normalname, tumorbam=tumorbam,
                                                             tumorname=tumorname, vcffile=vcffile, germline=germline,
                                                             pon=pon)
        else:
            mutect2_cmd = mutect2_cmd_stardand_script.format(gatk=gatk, index=index, normalbam=normalbam,
                                                             normalname=normalname, tumorbam=tumorbam,
                                                             tumorname=tumorname, vcffile=vcffile, germline=germline,
                                                             pon=pon)
    else:
        mutect2_cmd = mutect2_cmd_simplified_script.format(gatk=gatk, index=index, normalbam=normalbam,
                                                           normalname=normalname, tumorbam=tumorbam,
                                                           tumorname=tumorname, vcffile=vcffile)


    run_cmd("mutect annlysis", "".join(mutect2_cmd))

