from .config import get_config
from .command import run_cmd
from .fastqfiles import check
import sys, os, re, json
import multiprocessing as mp

def run_salmon(fq1, fq2, genome, outdir, config=""):
    """
    salmon- is a tool for quantifying the expression of transcripts using RNA-seq data.

    .. _Salmon: http://combine-lab.github.io/salmon/

    Usage:
    ::
       baseqRNA run_salmon -g hg38 -1 Sample01.1.fa.gz -2 Sample01.2.fa.gz -n Test

    Return:
    ::
        Test
        |---aux_info
             |---ambig_info.tsv
             |---expected_bias.gz
             |---fld.gz
             |---meta_info.json
             |---observed_bias_3p.gz
             |---observed_bias.gz
        |---cmd_info.json
        |---lib_format_counts.json
        |---libParams
            |---flenDist.txt
        |---logs
            |---salmon_quant.log
        |---quant.genes.sf
        |---quant.sf
    """
    
    salmon = get_config("RNA", "salmon", config)
    salmon_ref = get_config("RNA_ref_"+genome, "salmon_index", config)
    gene_map = get_config("RNA_ref_"+genome, "gene_map", config)
    if fq1 and fq2 and os.path.exists(fq1) and os.path.exists(fq2):
        salmon_cmd = [salmon, 'quant', '-i', salmon_ref, '-l A', '-1', fq1, '-2', fq2, '-p 8', '-g', gene_map, '-o', outdir]
    elif fq1 and os.path.exists(fq1):
        salmon_cmd = [salmon, 'quant', '-i', salmon_ref, '-l A', '-r', fq1, '-p 8', '-g', gene_map, '-o', outdir]
    else:
        sys.exit("[error]")
    run_cmd("Salmon Quantification", " ".join(salmon_cmd))
    return salmon_cmd

# Build TPM and QC ...
def build_TPM_table(processdir, samplefile, name):
    """
    Bulid tpm table using results of run_multi_salmon.
    The standard output of this function also include QC summary for all samples.

    This function requires a sample list(tab delimited, see align_quantify)
    ::
        #in python
        build_TPM_table("./results/of/run_multi_salmon", "samplefile", "Test")

        #in command line
        baseq-RNA aggr_TPM_QC -d /results/of/run_multi_salmon -m sample_list.txt -n Test

    Return:
    ::
        |---Test_TPM.txt
        |---Test_Count.txt
        |---Test_QC.txt

    """
    samples = check(samplefile)
    sample_names = [sample[0] for sample in samples]
    tpm_file_path = "{}_TPM.txt".format(name)
    count_file_path = "{}_Count.txt".format(name)
    qc_file_path = "{}_QC.txt".format(name)
    print("[info] The files will write to : {}".format(tpm_file_path, count_file_path, qc_file_path))
    tpm = {}
    count = {}
    qc = ["\t".join(['sample', 'reads', 'mapped', 'ratio', 'genecounts'])]
    for sample in sample_names:
        #build TPM table
        sample_TPM = []
        salmon_gene_path = os.path.join(processdir, sample, 'quant.genes.sf')
        with open(salmon_gene_path, 'r') as infile:
            infile.readline()
            for line in infile:
                infos = re.split("\t", line)
                gene = infos[0]
                sample_TPM.append(float(infos[3]))
                if not gene in tpm:
                    tpm[gene] = [float(infos[3])]
                    count[gene] = [float(infos[4])]
                else:
                    tpm[gene].append(float(infos[3]))
                    count[gene].append(float(infos[4]))

        #Genes Detected
        genes_TPM_1 = sum([1 for x in sample_TPM if x>=1])

        #build QC data
        metainfo = os.path.join(processdir, sample, 'aux_info', 'meta_info.json')
        with open(metainfo, "r") as file:
            qc_info = json.load(file)
            qc_sample = [sample, qc_info["num_processed"], qc_info["num_mapped"], qc_info["percent_mapped"], genes_TPM_1]
            qc.append("\t".join([str(x) for x in qc_sample]))

    #Write TPM
    tpm_file = open(tpm_file_path, "w")
    tpm_file.write("\t".join(["gene"] + sample_names) + "\n")
    for gene in tpm:
        sum_tpm_genes = sum(tpm[gene])
        if sum_tpm_genes > 0:
            tpm_file.write("\t".join([gene] + [str(x) for x in tpm[gene]]) + "\n")
    tpm_file.close()

    #Write Counts
    count_file = open(count_file_path, "w")
    count_file.write("\t".join(["gene"] + sample_names) + "\n")
    for gene in count:
        sum_tpm_genes = sum(count[gene])
        if sum_tpm_genes > 0:
            count_file.write("\t".join([gene] + [str(x) for x in count[gene]]) + "\n")
    count_file.close()

    #Write QC Table
    qc_file = open(qc_file_path, "w")
    qc_file.writelines("\n".join(qc))
    qc_file.close()

def run_multiple_salmons(samplefile, genome, processname, parallel, config=""):
    """
    This function enables you align and quantify all samples using Salmon in one comand line. Return of this function also include
    TPM table and QC summary.

    This function requires a sample list(tab delimited, see align_quantify). Threads number(int) should be set.
    ::
        #in python
        from baseq.rna import run_multiple_salmons
        run_multiple_salmons(samplefile, "hg38", "TestRNASeq", 8)

        #In command line
        baseq-RNA run_multi_salmon -g hg38 -m sample_list.txt -n Test -p 8

    Return:
    ::
       Test
       |---sample01
           |---...
       |---sample02
           |---...
       |---sample03
           |---...
       |---Test_TPM.txt
       |---Test_Count.txt
       |---Test_QC.txt
    """
    samples = check(samplefile)
    if not os.path.exists(processname):
        os.mkdir(processname)
    pool = mp.Pool(processes = int(parallel))
    for sample in samples:
        name = sample[0]
        path = os.path.join(processname, name)
        if not os.path.exists(path):
            os.mkdir(path)
        if sample[2]:
            script = "baseqRNA run_salmon -1 {} -2 {} -g {} -n {} -c {}".format(sample[1], sample[2], genome, path, config)
        else:
            script = "baseqRNA run_salmon -1 {} -g {} -n {} -c {}".format(sample[1], genome, path, config)
        pool.apply_async(run_cmd, ("Salmon", script))
    pool.close()
    pool.join()
    print("[info] The All samples Are Processed.... Start Aggregating...")
    build_TPM_table(processname, samplefile, processname)
