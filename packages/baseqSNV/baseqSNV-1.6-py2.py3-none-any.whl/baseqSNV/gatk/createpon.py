import os
from ..config import get_config
from ..process import run_cmd

def listofvcf(path):
    normalargs=open(os.path.join(path,"normalvcf_for_pon.args"),"w")
    filelist=[]
    filename = os.listdir(path)
    for fn in filename:
        if fn[-6:] == "vcf.gz":
           fullfilename = os.path.join(path,fn)
           filelist.append(fullfilename)
    normalargs.write("\n".join([list for list in filelist]) + "\n")
    return os.path.join(path,"normalvcf_for_pon.args")

normalvcf_cmd_script="""
{gatk} Mutect2 -R {index} -I {normalbam} -tumor {samplename} --disable-read-filter MateOnSameContigOrNoMappedMateReadFilter -L {interval} -O {normalvcf}
"""
normalvcf_cmd_script1="""
{gatk} Mutect2 -R {index} -I {normalbam} -tumor {samplename} --disable-read-filter MateOnSameContigOrNoMappedMateReadFilter -O {normalvcf}
"""
pon_cmd_script="""
{gatk} CreateSomaticPanelOfNormals -vcfs {normalvcfs} -O {ponvcf}
"""
def create_pon(genome,list,path,interval):
    """
    Create_pon function helps you create PoN(panel of normals) file necessary for mutect2 calling. The PoN captures
    common artifactual and germline variant sites. Mutect2 then uses the PoN to filter variants at the site-level.

    Example of samples list (tab delimited):

    * Content of columns are normal sample name, normal BAM file, tumor sample name, tumor BAM file(order cannot be distruped).
      Absoulte path of all BAM files should be added if directory of BAM files and analysis directory are different.
      ::
        N504    N504_marked_bqsr.bam   T504    T504_marked_bqsr.bam
        N505    N505_marked_bqsr.bam   T505    T505_marked_bqsr.bam
        N506    N506_marked_bqsr.bam   T506    T506_marked_bqsr.bam
        N509    N509_marked_bqsr.bam   T509    T509_marked_bqsr.bam
        N510    N510_marked_bqsr.bam   T510    T510_marked_bqsr.bam

    Usage:

    * Interval list defines genomic regions where analysis is restricted. Introduction of interval list format and its function can be found this page_.
      ::
        # designated a intervals.list
        baseq-SNV create_pon -g hg37 -l sample_list.txt -p ./ -L interval.list
        # Using the dafalut intervals.list
        baseq-SNV create_pon -g hg37 -l sample_list.txt -p ./

    .. _page: https://software.broadinstitute.org/gatk/documentation/article?id=11009
    """
    index = get_config("SNV_ref_" + genome, "bwa_index")
    gatk = get_config("SNV", "GATK")
    if not os.path.exists(path):
        print("[ERROR] No such file or directory")
    else:
        path_pon = os.path.join(path, "pon")
        if not os.path.exists(path_pon):
            os.mkdir(path_pon)

    with open(list, "r") as file:
        lines = file.readlines()
    sample_info = [line.strip().split() for line in lines]
    import multiprocessing as mp
    pool = mp.Pool(processes=6)
    results = []
    for sample in sample_info:
        normalvcf = os.path.join(path_pon, "{}_tumor-only.vcf.gz".format(sample[0]))
        if interval:
            normalvcf_cmd = normalvcf_cmd_script.format(gatk=gatk, index=index, normalbam=sample[1],
                                                        samplename=sample[0],
                                                        normalvcf=normalvcf, interval=interval)
        else:
            normalvcf_cmd = normalvcf_cmd_script1.format(gatk=gatk, index=index, normalbam=sample[1],
                                                         samplename=sample[0],
                                                         normalvcf=normalvcf)
        results.append(pool.apply_async(run_cmd, ("creat normal vcf file", "".join(normalvcf_cmd,))))
    pool.close()
    pool.join()
    [x.get() for x in results]
    normalargs = listofvcf(path_pon)
    ponvcf = os.path.join(path, "pon.vcf.gz")
    pon_cmd = pon_cmd_script.format(gatk=gatk, normalvcfs=normalargs, ponvcf=ponvcf)
    run_cmd("create panel of normals", "".join(pon_cmd))

def run_createsomatic_pon(path_pon,path):
    gatk = get_config("SNV", "GATK")
    normalargs = listofvcf(path_pon)
    ponvcf = os.path.join(path,"pon.vcf.gz")
    pon_cmd = pon_cmd_script.format(gatk=gatk, normalvcfs=normalargs, ponvcf=ponvcf)
    run_cmd("create panel of normals", "".join(pon_cmd))
