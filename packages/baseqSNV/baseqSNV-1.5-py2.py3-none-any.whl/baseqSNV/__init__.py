import click, sys
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    click.echo("Welcome to use baseqSNV...")

from .cmd import *
from .qc.cmd import *
from .vcf.cmd import *
from .gatk import *

__all__ = [
    'quality_enrich', 'quality_enrich_multiple',
    'run_gatkpipe', 'run_multi_gatkpipe',
    'alignment', 'run_markdup', 'bqsr',
    'run_callvar',
    'selectvar', 'mutect2', 'create_pon',
    'run_annovar'
]

#quality control
from .qc.enrich import quality_enrich, quality_enrich_multiple

#gatk
from .gatk.pipe import run_gatkpipe, run_multi_gatkpipe
from .gatk.mutect import mutect2
from .gatk.align import alignment
from .gatk.markdup import run_markdup
from .gatk.callvar import run_callvar
from .gatk.selectvar import selectvar
from .gatk.bqsr import bqsr
from .annovar import run_annovar
from .gatk.createpon import create_pon