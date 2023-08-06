from ..io import FileOutput, FileInput

try:
    import pandas as pd
    import scipy.sparse as sp
    from anndata import AnnData
except ImportError:
    raise ImportError(
        "This module requires anndata (https://github.com/theislab/anndata)."
    )


def get_path(file, content_type, input=False, output=False):
    """Returns a path iff the file is of requested type and """
    if input and type(file) is not FileInput:
        raise TypeError(
            f'File "{file.name}" has to be an input file.'
        )
    if output and type(file) is not FileOutput:
        raise TypeError(
            f'File "{file.name}" has to be an output file.'
        )
    if file.type != content_type:
        raise TypeError(
            f'File "{file.name}" is of type "{file.type}" but expected "{content_type}".'
        )
    return file.path


def read_data(
    fgprocess,
    expr="expression_matrix",
    cell_meta="cell_metadata",
    gene_meta="gene_metadata",
):
    expr_path = get_path(
        fgprocess.files[expr],
        content_type="expression_matrix",
        input=True,
    )
    cell_path = get_path(
        fgprocess.files[cell_meta],
        content_type="cell_metadata",
        input=True,
    )
    gene_path = get_path(
        fgprocess.files[gene_meta],
        content_type="gene_metadata",
        input=True,
    )

    obs = pd.read_csv(cell_path, index_col="cell_id")
    var = pd.read_csv(gene_path, index_col="entrez_id")
    expr = pd.read_csv(expr_path, sep=",")

    counts = sp.coo_matrix(
        (expr.expression, (expr.cell_id, expr.entrez_id)),
        shape=(obs.shape[0], var.shape[0]),
        dtype="float32",
    ).tocsr()

    adata = AnnData(counts, obs=obs, var=var)
    return adata


# Writing
def write_exprs_csv(adata, csv_file):
    mat = adata.X.tocoo()
    df = pd.DataFrame.from_dict(
        dict(cell_id=mat.row, entrez_id=mat.col, expression=mat.data)
    )
    df.to_csv(csv_file)


def write_data(
    fgprocess, adata, expr=None, cell_meta=None, gene_meta=None
):
    if expr is not None:
        exprs_path = get_path(
            fgprocess.files[expr],
            content_type="expression_matrix",
            output=True,
        )
        write_exprs_csv(adata, exprs_path)
    if cell_meta is not None:
        cell_path = get_path(
            fgprocess.files[cell_meta],
            content_type="cell_metadata",
            output=True,
        )
        adata.obs.to_csv(cell_path)
    if gene_meta is not None:
        gene_path = get_path(
            fgprocess.files[gene_meta],
            content_type="gene_metadata",
            output=True,
        )
        adata.obs.to_csv(gene_path)
