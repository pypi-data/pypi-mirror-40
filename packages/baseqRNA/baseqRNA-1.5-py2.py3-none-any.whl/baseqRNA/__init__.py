# Copyright 2018- by Xiannian Zhang. 
# All rights reserved.

__version__ = "1.0.0"

CONTEXT_SETTINGS = dict(
	help_option_names=['-h', '--help']
	)

import click

@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    click.echo("Welcome to Use baseqRNA ...")

from .cmd import *

#gene quantification
from .salmon import run_salmon, run_multiple_salmons, build_TPM_table
from .aligner import HISAT2, STAR
from .quantify import cufflinks,featureCounts
from .pipeline import align_quantify, build_FPKM_table

#Differential Expression
from .DiffExp.deseq2 import deseq2, DESeq2_to_Excel