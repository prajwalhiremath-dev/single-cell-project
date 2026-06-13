from pathlib import Path


def summarize_h5ad(path: str) -> dict:
    """Return a lightweight summary for an AnnData `.h5ad` file.

    This import is intentionally inside the function because Scanpy/AnnData can be
    heavy and should not slow down normal API startup.
    """
    import scanpy as sc

    dataset_path = Path(path)
    adata = sc.read_h5ad(dataset_path)

    return {
        "cells": int(adata.n_obs),
        "genes": int(adata.n_vars),
        "obs_columns": list(map(str, adata.obs.columns.tolist())),
        "var_columns": list(map(str, adata.var.columns.tolist())),
        "has_raw": adata.raw is not None,
        "layers": list(map(str, adata.layers.keys())),
    }


def validate_supported_format(filename: str) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix != ".h5ad":
        raise ValueError("Only .h5ad is supported in the first MVP version")
    return "h5ad"
