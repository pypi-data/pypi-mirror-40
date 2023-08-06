import os, sys
from .align import alignment
from .markdup import run_markdup
from .callvar import run_callvar
from .selectvar import selectvar
from .bqsr import bqsr
from ..annovar import run_annovar
from ..config import get_config
from ..process import run_cmd

def run_gatkpipe(config, dir, fq1, fq2, bamfile, name, genome, memory, step="all"):
    """ Run GATK, including bqsr/callvar/selectvar/annovar
    
    The pipeline contains following steps:
    
    #. Alignment using BWA.
    #. MarkDuplicated Using Picard.
    #. BQSR.
    #. Haplocaller.
    #. SelectVarient.

    A config file should be provided:
    ::
        
    
    Args:
        config: config file;
        dir: outdir path, the result will be dir/name;
        step: all/align/markdup/bqsr/callvar/annovar;
    
    Examples:
    ::
        #In commandline:
        

        #As function...
        from baseqSNV.gatk.pipe import run_gatkpipe
        run_gatkpipe("./config.ini", )
    """

    if config:
        if not os.path.exists(config):
            sys.exit("[error] Config file not exists")
        os.environ["BASEQCFG"] = config

    outdir = os.path.abspath(os.path.join(dir, name))
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    bam_marked = os.path.join(outdir, "{}.marked.bam".format(name))
    bam_bqsr = os.path.join(outdir, "{}.marked.bqsr.bam".format(name))
    vcf_raw = os.path.join(outdir, "{}.raw.snp.indel.vcf".format(name))
    vcf_select = os.path.join(outdir, "{}.raw.snp.vcf".format(name))
    vcf_filter = os.path.join(outdir, "{}.filter.snp.vcf".format(name))
    annovarfile = os.path.join(outdir, "{}.snp.avinput".format(name))

    if fq1 :
        bamfile = os.path.join(outdir, "{}.bam".format(name))
    
    if step in ['all', 'align'] :
        if fq1 :
            alignment(fq1, fq2, name, genome, bamfile)
        else:
            print("[ERROR] Alignment is not apply for bam file.")

    if step in ['all', 'markdup']:
        run_markdup(bamfile, bam_marked, memory, outdir)

    if step in ['all', 'bqsr']:
        bqsr(bam_marked, bam_bqsr, genome)

    if step in ['all', 'callvar']: 
        run_callvar(bam_bqsr, vcf_raw, genome)
        selectvar(vcf_raw, vcf_select, vcf_filter, genome)
    
    # if step in ['all', 'annovar']:  
    #     run_annovar(vcf_filter, annovarfile, name, genome, outdir)

def run_multi_gatkpipe(config, genome, list, dir, thread, memory_size, step="all"):
    """ Run GATK pipeline for multiple fastq or bam file list.
    """
    with open(list, 'r') as file:
          lines = file.readlines()
    lists = [line.strip().split() for line in lines]
    import multiprocessing as mp
    pool = mp.Pool(processes=int(thread))
    results = []
    for list in lists:
        if list[1][-4:] == ".bam":
            results.append(pool.apply_async(run_gatkpipe, (config, dir, "", "", list[1], list[0], genome, memory_size, step)))
        elif list[1][-5:] == "fq.gz" and list[2]:
            results.append(pool.apply_async(run_gatkpipe, (config, dir, list[1], list[2], "", list[0], genome, memory_size, step)))
        else:
            results.append(pool.apply_async(run_gatkpipe, (config, dir, list[1], "", "", list[0], genome, memory_size, step)))
    pool.close()
    pool.join()
    [x.get() for x in results]
    print("[info] Multi-sample GATK analysis complete")

qusb_script_cmd = """
baseq-SNV run_multi_gatkpipe -c {config} -g {genome} -l {part_sample_list} -d {outdir} -t{thread} -M {memory_size}
"""

def samplefile_split(linesize,sample_list):
    filedir,name =  os.path.split(sample_list)
    name,ext = os.path.splitext(name)
    #print(filedir,name,ext)

    stream = []
    partno = 0
    partfile = []
    with open(sample_list,'r') as f:
        for line in f:
            stream.append(line)
            if len(stream) < int(linesize):
                continue
            partfile_name = os.path.join(filedir,name + "_" + str(partno) + ext)
            partfile.append(partfile_name)
            with open(partfile_name,'w') as p:
                p.write(''.join([line for line in stream[:-1]]))
                p.write(stream[-1].strip())
                stream = []
                partno += 1
    if stream:
        partfile_name = os.path.join(filedir,name + "_" + str(partno) + ext)
        partfile.append(partfile_name)
        with open(partfile_name, 'w') as p:
            p.write('\n'.join([line for line in stream[:-1]]))
            p.write(stream[-1].strip())
    with open(os.path.join(filedir, "{name}_split{ext}".format(name=name,ext=ext)),'w') as r:
        r.write('\n'.join([line for line in partfile]))

    return os.path.join(filedir, "{name}_split{ext}".format(name=name,ext=ext))
