import click
from . import cli

@cli.command(short_help="Check the enrichment quality, input: bam, interval and outpath")
@click.argument("bampath")
@click.argument("interval")
@click.argument("outpath")
def enrich_saturation(bampath, interval, outpath):
    pass

@cli.command(short_help="Align to genome Using BWA")
@click.option('--fq1', '-1', default='', help='fastq1 path')
@click.option('--fq2', '-2', default='', help='fastq2 path (optional)')
@click.option('--name', '-n', default='SNV', help='sample name(ID)')
@click.option('--thread', '-t', default='8', help='thread for BWA')
@click.option('--genome','-g', default='hg19', help='species genome version: hg19/mm10/mm38')
@click.option('--config', '-c', default = '', help = 'path of config file (./config.ini)')
def align(fq1, fq2, name, genome, thread, config):
    from .gatk.align import alignment
    alignment(fq1, fq2, name, genome, thread, config)
    print("[info] Alignment Completed")

@cli.command(short_help="mark duplicates")
@click.option('--bamfile', '-b', default='', help='bamfile for gatk analysis')
@click.option('--markedbam', '-m', default='', help='marked bamfile')
@click.option('--memory_size', '-M', default='2G', help='memory size,such as 2G,1024M')
@click.option('--tmpdir', '-d', default='./', help='directory for temporary data output ')
@click.option('--config', '-c', default = '', help = 'path of config file (./config.ini)')
def markdup(bamfile, markedbam, memory_size, tmpdir, config):
    from .gatk.markdup import run_markdup
    run_markdup(bamfile, markedbam, memory_size, tmpdir, config)
    print("[info] Mark duplicates complete")

@cli.command(short_help="Base Recalibrator")
@click.option('--markedbam', '-m',default='', help='bam file with mark duplicates')
@click.option('--genome', '-g', default='', help='Species hg38/hg19 or mm10/mm38')
@click.option('--interval', '-i', default='./interval.bed', help='interval bed file of the sample')
@click.option('--keepdup', '-f', default='', help='Set Yes to keep duplicate reads')
@click.option('--bqsrbam', '-q',default='', help='output bam file after base recalibrator')
@click.option('--config', '-c', default = '', help = 'path of config file (./config.ini)')
def bqsr(markedbam, bqsrbam, genome, interval, keepdup, config):
    from .gatk.bqsr import bqsr
    if keepdup:
        bqsr(markedbam, bqsrbam, genome, config, interval, disable_dup_filter=True)
    else:
        bqsr(markedbam, bqsrbam, genome, config, interval)
    print("[info] Base recalibrator complete")

@cli.command(short_help="call variants")
@click.option('--bqsrbam', '-q',default='', help='bam from BQSR processing')
@click.option('--genome', '-g',default='', help='genome version: hg19/mm10/mm38')
@click.option('--rawvcf', '-r', default='baseqSNV.vcf', help='output vcf file include snp and indel')
@click.option('--interval', '-i', default='./interval.bed', help='interval bed file of the sample')
@click.option('--config', '-c', default = 'config.ini', help = 'path of config file (./config.ini)')
def callvar(bqsrbam, rawvcf, genome, interval, config):
    from .gatk.callvar import run_callvar
    run_callvar(bqsrbam, rawvcf, genome, config, interval)
    print("[INFO] Calling variants complete")

@cli.command(short_help="select variants ")
@click.option('--rawvcf', '-r', default='', help='vcf file include snp and indel')
@click.option('--selectvcf', '-s', default='', help='output file include snp only')
@click.option('--filtervcf', '-f', default='', help='output vcf file after filtering low quality snp')
@click.option('--genome', '-g', default='', help='Species hg19 or mm10/mm38')
def selectvar(rawvcf, selectvcf, filtervcf, genome):
    from .gatk.selectvar import selectvar
    selectvar(rawvcf, selectvcf, filtervcf, genome)
    print("[info] Select variants complete")

@cli.command(short_help="annovar annotation")
@click.option('--filtervcf', '-f', default='', help='vcf file after filtering low quality snp')
@click.option('--genome','-g', default='', help='Species hg19 or mm10/mm38')
@click.option('--dir', '-d', default='', help='folder for output files')
@click.option('--name', '-n', default='', help='prefix of annovar annotation file')
def run_annovar(filtervcf,dir,name,genome):
    from .annovar import run_annovar
    annovarfile = os.path.join(dir, "{}.avinput".format(name))
    run_annovar(filtervcf,annovarfile,name,genome,dir)
    print("[info] Annovar annotation complete")

@cli.command(short_help="run gatk pipeline")
@click.option('--config', '-c', default = '', help = 'config file path')
@click.option('--genome', '-g', default = '', help = 'Species hg19/hg38')
@click.option('--name', '-n', default = '', help = 'sample name')
@click.option('--step', default = 'all', help = 'Run all pipelines or the substeps')
@click.option('--fq1', '-1', default = '', help = 'fastq1 path')
@click.option('--fq2', '-2', default = '', help = 'fastq2 path(optional)')
@click.option('--bamfile', '-b', default = '', help = 'bamfile for gatk analysis(When fq1,fq2 not set)')
@click.option('--dir', '-d', default = './', help = 'folder for output files')
@click.option('--memory_size', '-M', default='', help='memory size,such as 2G,1024M')
def run_gatkpipe(config, dir, fq1, fq2, bamfile, name, genome, memory_size, step):
    from .gatk.pipe import run_gatkpipe
    run_gatkpipe(config, dir, fq1, fq2, bamfile, name, genome, memory_size, step)

@cli.command(short_help="run multi-samples' gatk pipeline")
@click.option('--config', '-c', default = '', help = 'config file path')
@click.option('--genome', '-g', default = '', help = 'Species hg19/hg38')
@click.option('--list', '-l', default = '', help = 'list of name and BAMfile path or list of names and Fastq files path')
@click.option('--dir', '-d', default = './', help = 'folder for output files')
@click.option('--step', default = 'all', help = 'Run all pipelines or the substeps')
@click.option('--thread', '-t', default='8', help='Thread(int) for samples analysed at the same time')
@click.option('--memory_size', '-M', default='', help='memory size,such as 2G,1024M')
def run_multi_gatkpipe(config,genome,list,dir,thread, memory_size, step):
    from .gatk.pipe import run_multi_gatkpipe
    run_multi_gatkpipe(config, genome, list, dir, thread, memory_size, step)

@cli.command(short_help="mutect2 analysis")
@click.option('--genome', '-g', default = '', help = 'Species hg19/hg38')
@click.option('--normalbam', '-N', default = '', help = 'bam file of normal sample')
@click.option('--tumorbam', '-T', default = '', help = 'bam file of tumor sample')
@click.option('--normalname', '-n', default = 'normal', help = 'name of normal sample')
@click.option('--tumorname', '-t', default = 'tumor', help = 'name of tumor sample')
@click.option('--path', '-o', default = '', help = 'path of output files')
@click.option('--pon', '-p', default = '', help = 'panel of normal samples')
@click.option('--list', '-l', default = '', help = 'list of normal bamfile and tumor bamfile,normalname,normalbam,tumorname,tumorbam')
@click.option('--germline', '-G', default = '', help = 'population gnomAD')

def run_mutect2(genome, normalbam, normalname, tumorbam, tumorname, list, path, pon, germline):
    from .gatk.mutect import mutect2
    if list:
        with open(list, 'r') as file:
            lines = file.readlines()
        lists = [line.strip().split() for line in lines]

    else:
        lists = [[normalname,normalbam,tumorname,tumorbam]]
    import multiprocessing as mp
    pool = mp.Pool(processes=10)
    results = []
    for list in lists:
        vcffile = os.path.join(path,"{}_{}.vcf.gz".format(list[0],list[2]))
        results.append(pool.apply_async(mutect2, (genome, list[0], list[1], list[2], list[3], vcffile, pon, germline)))
    pool.close()
    pool.join()
    [x.get() for x in results]
    print("[info] mutect2 analysis complete")

@cli.command(short_help="mutect2 analysis")
@click.option('--resource', '-r', default = '', help = 'common biallelic vcf files')
@click.option('--tumorbam', '-T', default = '', help = 'bam file of tumor sample')
@click.option('--somaticvcf', '-s', default = '', help = 'mutect call')
@click.option('--path', '-o', default = '', help = 'path of output files')
@click.option('--tumorname', '-t', default = '', help = 'tumor sample name')
def filter_mutect_call(tumorname, tumorbam, somaticvcf, resource, path):
    from .gatk.selectvar import get_filter_table,filter_mutect_vcf
    gps_table = os.path.join(path,"{}_gps.table".format(tumorname))
    calcontam_table = os.path.join(path, "{}_calcontam.table".format(tumorname))
    filter_call = os.path.join(path, "{}_filter.vcf.gz".format(tumorname))

    get_filter_table(tumorbam, resource, gps_table, calcontam_table)
    filter_mutect_vcf(somaticvcf, calcontam_table, filter_call)

@cli.command(short_help="test for filter_mutect_vcf")
@click.option('--calcontam_table', '-c', default = '', help = 'table')
@click.option('--somaticvcf', '-s', default = '', help = 'mutect call')
@click.option('--path', '-o', default = '', help = 'path of output files')
def filter_mutect_vcf(somaticvcf, calcontam_table, path):
    from .gatk.selectvar import filter_mutect_vcf
    filter_call = os.path.join(path, "somatic_filter.vcf.gz")
    filter_mutect_vcf(somaticvcf, calcontam_table, filter_call)


@cli.command(short_help="create PoN")
@click.option('--path', '-p', default = '', help = 'path of the output files')
@click.option('--genome', '-g', default = '', help = 'Species hg19/hg38')
@click.option('--list', '-l', default = '', help = 'list of normal bamfile and tumor bamfile,normalname,normalbam,tumorname,tumorbam')
@click.option('--interval', '-L', default = '', help = 'interval list')
def create_pon(genome, list, path, interval):
    from .gatk.createpon import create_pon
    create_pon(genome, list, path, interval)

@cli.command(short_help="creat args file for PoN")
@click.option('--path', '-p', default = '', help = 'path of all normal-call vcf files')
def listofvcf(path):
    from .gatk.createpon import listofvcf
    listofvcf(path)

@cli.command(short_help="create panel of normals")
@click.option('--outpath', '-o', default = '', help = 'path of output file')
@click.option('--ponpath', '-p', default = '', help = 'path of all normal-call vcf files')
def run_createsomatic_pon(ponpath,outpath):
    from .gatk.createpon import run_createsomatic_pon
    run_createsomatic_pon(ponpath,outpath)

@cli.command(short_help = "test for split file")
@click.option('--list', '-l', default = '', help = 'list of name and BAMfile path or list of names and Fastq files path')
@click.option('--line_size', '-S', default = '3', help = 'number of lines in each split file')
def split_file(line_size,list):
    from .gatk.pipe import samplefile_split
    samplefile_split(line_size,list)
