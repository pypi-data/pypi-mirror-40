import click
from . import cli
from .Table.cmd import *
from .GTF.cmd import *

@cli.command(short_help="salmon quatification")
@click.option('--sample_file', '-m', default='', help="Tab seprated file: name, fq1, fq2")
@click.option('--genome', '-g', default='hg38', help="Species hg19 or mm10/mm38")
@click.option('--name', '-n', default='RNA', help="Name of The Process (RNA)")
@click.option('--config', '-c', default='', help="Path to the config file")
@click.option('--parallel', '-p', default='6', help="How many runs at the same time...")
@click.option('--fq1', '-1', default='', help="Fastq 1")
@click.option('--fq2', '-2', default='', help="Fastq 2")
def run_salmon(sample_file, fq1, fq2, genome, name, parallel, config):
    from .salmon import run_salmon, run_multiple_salmons
    if sample_file:
        run_multiple_salmons(sample_file, genome, name, parallel, config)
    else:
        run_salmon(fq1, fq2, genome, name, config)

#run hisat, samtools and cufflinks
@cli.command(short_help="hisat alignment and cufflinks quatification")
@click.option('--name', '-n', default='sample', help="Name of Sample/Samples (For fq1/fq2)")
@click.option('--fq1', '-1', default='', help="Fastq 1")
@click.option('--fq2', '-2', default='', help="Fastq 2")
@click.option('--sample_file', '-m', default='', help="Tab seprated file: name, fq1, fq2")
@click.option('--genome', '-g', default='hg38', help="Species hg19 or mm10/mm38")
@click.option('--aligner', '-a', default='hisat', help="hisat/star/none")
@click.option('--quantify', '-q', default='cufflinks', help="Cufflinks/Featurecounts/none")
@click.option('--parallel', '-p', default='4', help="How many samples in the same time?")
def run_hisat(sample_file, fq1, fq2, name, genome, quantify, aligner, parallel):
    from .pipeline import align_quantify
    align_quantify(name, fq1, fq2, sample_file, genome, aligner, quantify, int(parallel))

@cli.command(short_help="Aggregate TPM and Counts and QC Tables for multiple samples")
@click.option('--sample_file', '-m', default='', help="Tab seprated file: name, fq1, fq2")
@click.option('--processdir', '-d', default='./', help="Combine all the TPMs under the folder")
@click.option('--name', '-n', default='sample', help="Name of Analysis")
def aggr_TPM_QC(processdir, sample_file, name):
    from .salmon import build_TPM_table
    build_TPM_table(processdir, sample_file, name)

@cli.command(short_help="Aggregate TPM and Counts and QC Tables for multiple samples")
@click.option('--sample_file', '-m', default='', help="Tab seprated file: name, fq1, fq2")
@click.option('--processdir', '-d', default='./', help="Combine all the TPMs under the folder")
@click.option('--outpath', '-o', default='./', help="Prefix of the TPM and Count file")
def aggr_FPKM_QC(processdir, sample_file, outpath):
    from .pipeline import build_FPKM_table
    print("[info] Aggregate FPKM into {}".format(outpath))
    build_FPKM_table(processdir, sample_file, outpath)

@cli.command(short_help="plot tpm correlation figure between samples")
@click.option('--name1', '-1', default='', help="sample name")
@click.option('--name2', '-2', default='', help="sample name")
@click.option('--table', '-t', default='', help="Table path")
@click.option('--figname', '-n', default='scatter', help="The scripts and output path")
def plot_corelation_scatter(name1, name2, table, figname):
    from .QC.scatterplot import plot_corelation_fig
    plot_corelation_fig(name1, name2, table, figname)

@cli.command(short_help="Correlation Heatmap")
@click.option('--table', '-t', default='', help="Table path")
@click.option('--name', '-n', default='heatmap', help="The scripts and output path")
def corr_heatmap(table, name):
    from .QC.corrheatmap import correlation_heatmap
    correlation_heatmap(table, name)

@cli.command(short_help="Correlation Heatmap")
@click.option('--table', '-t', default='', help="Table path")
@click.option('--group', '-g', default='', help="Group file")
@click.option('--name', '-n', default='pca_analysis', help="The scripts and output path")
def pca_analysis(table, group, name):
    from .QC.pca import pca_analysis
    pca_analysis(table, group)

@cli.command(short_help="Correlation Heatmap")
@click.option('--table', '-t', default='', help="Table path")
@click.option('--group', '-g', default='', help="Group file")
@click.option('--comparefile', '-p', default='', help="Tab seprated file: group1, group2")
@click.option('--qcfile', '-q', default='', help="QC files")
@click.option('--name', '-n', default='pca_analysis', help="The scripts and output path")
def diff_power_analysis(table, group, comparefile, qcfile, name):
    from .QC.pca import pca_score_power
    pca_score_power(table, group, comparefile, qcfile)


@cli.command(short_help="test for listfobam")
@click.option('--sample_file', '-m', default='', help="Tab seprated file: name, fq1, fq2")
@click.option('--bampath', '-b', default='', help="Directory of bam file")
def listofbam(sample_file, bampath):
    from .quantify import listofbam
    listofbam(sample_file, bampath)

@cli.command(short_help="FeatureCounts quantify")
@click.option('--sample_file', '-m', default='', help="Tab seprated file: name, fq1, fq2")
@click.option('--bampath', '-b', default='', help="Directory of bam file")
@click.option('--genome', '-g', default='hg38', help="Species hg19 or mm10/mm38,or the GTF/GFF file you provide in config")
@click.option('--feature', '-f', default='exon', help="feature of provided annotation(e.g. exon, gene, transcript")
@click.option('--id', '-d', default='', help="the gene_id attribute available in the GTF format annotation (or the GeneID column in the SAF format annotation)")
@click.option('--countsfile', '-o', default='', help="table of counts")
@click.option('--seqtype', '-t', default='', help="single- or paired-end read dataset")
def featurecounts(genome, feature, id, countsfile, bampath, seqtype, sample_file):
    from .quantify import featureCounts
    featureCounts(genome, feature, id, countsfile, bampath, seqtype, sample_file)

#######################
##### DESeq2 commands
#######################
@cli.command(short_help="Run DESeq2")
@click.option('--config', default='', help="The Config Excel ...")
@click.option('--groupfile', '-g', default='', help="Tab seprated file: samplename, groups")
@click.option('--comparefile', '-p', default='', help="Tab seprated file: group1, group2")
@click.option('--tpmfile', '-t', default='./', help="TPM filepath")
@click.option('--countfile', '-c', default='./', help="Read Count filepath")
@click.option('--outpath', '-o', default='./diff_exp', help="Folder for exportation...")
def diff_deseq2(config, tpmfile, countfile, groupfile, comparefile, outpath):
    from .DiffExp.deseq2 import deseq2
    print("[info] DESeq2 {}".format(outpath))
    deseq2(config, tpmfile, countfile, groupfile, comparefile, outpath)

@cli.command(short_help="Run DESeq2")
@click.option('--groupfile', '-g', default='', help="Tab seprated file: samplename, groups")
@click.option('--comparefile', '-p', default='', help="Tab seprated file: group1, group2")
@click.option('--outdir', '-o', default='./diff_exp', help="Folder for exportation...")
def diff_deseq2_result(groupfile, comparefile, outdir):
    from .DiffExp.deseq2 import DESeq2_to_Excel
    print("[info] DESeq2 {}".format(outdir))
    DESeq2_to_Excel(groupfile, comparefile, outdir)


