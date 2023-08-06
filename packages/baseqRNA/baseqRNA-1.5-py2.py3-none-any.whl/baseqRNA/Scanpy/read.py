
def get_hvg_genes(h5files, names):
    """
    Get highly variable genes from list of 10X h5 files

    Usage:
    ::
        get_hvg_intersects(["filtered_gene_bc_matrices_h5.h5", "filtered_gene_bc_matrices_2_h5.h5"],
        ["sample1", "sample2"])
    """

    import scanpy.api as sc

    adata1 = sc.read_10x_h5("3-11-filtered_gene_bc_matrices_h5.h5", "GRCh38")
    adata2 = sc.read_10x_h5("3-43-filtered_gene_bc_matrices_h5.h5", "GRCh38")
    adata3 = sc.read_10x_h5("5-1-filtered_gene_bc_matrices_h5.h5", "GRCh38")
    adata4 = sc.read_10x_h5("5-2-filtered_gene_bc_matrices_h5.h5", "GRCh38")

    datas = [adata1, adata2, adata3, adata4]
    datas_norm = [1, 1, 1, 1]
    var_genes = []
    for index, adata in enumerate(datas):
        adata.var_names_make_unique()
        sc.pp.filter_cells(adata, min_genes=1000)
        sc.pp.filter_genes(adata, min_cells=300)

        # freezes the state of the AnnData object
        adata.raw = sc.pp.log1p(adata, copy=True)
        sc.pp.normalize_per_cell(adata, counts_per_cell_after=1e4)
        filter_result = sc.pp.filter_genes_dispersion(adata.X, min_mean=0.25, max_mean=3, min_disp=0.5)
        sc.pl.filter_genes_dispersion(filter_result)

        # do the filtering
        adata = adata[:, filter_result.gene_subset]
        sc.pp.log1p(adata)

        datas_norm[index] = adata
        var_genes.append(list(adata.var_names))
        print(adata)

    import itertools
    merged = list(itertools.chain(*var_genes))
    vargenes = list(set(merged))
    print(len(vargenes))


def slice_raw(cells, genes):
    """
    Sampling the number of cells with the given gene list...
    """
    pass