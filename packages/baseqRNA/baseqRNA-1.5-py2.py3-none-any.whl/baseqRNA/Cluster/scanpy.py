"""
Scanpy_ is a scalable toolkit for analyzing single-cell gene expression data. It includes preprocessing, visualization, clustering, pseudotime and trajectory inference, differential expression testing and simulation of gene regulatory networks. The Python-based implementation efficiently deals with datasets of more than one million cells.

Read the documentation_ . If Scanpy is useful for your research, consider citing Genome Biology (2018).

http://anndata.readthedocs.io/en/latest/

.. _Scanpy: https://github.com/theislab/scanpy
.. _documentation: http://scanpy.readthedocs.io/en/latest/

Usage:
::
    import scanpy.api as sc

    # cluster cells using Louvain clustering
    sc.tl.louvain(adata, **tool_params)

    import pandas as pd
    anno = pd.read_csv(filename_sample_annotation)
    adata.obs['cell_groups'] = anno['cell_groups']  # categorical annotation of type pandas.Categorical
    adata.obs['time'] = anno['time']                # numerical annotation of type float
    # alternatively, you could also set the whole dataframe
    # adata.obs = anno
"""

def sranpy(dataset):
    """

    """
    pass