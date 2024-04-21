import os
import scanpy as sc
import scvi
import torch

in_data_dir = "/local/home/savchuki/projects/swarm-atlas/data"
out_data_dir = "/local/home/savchuki/projects/swarm-atlas/data"
in_filename = "lung-atlas-public.h5ad"
out_filename = "lung-atlas-public-processed.h5ad"

torch.set_float32_matmul_precision("high")

# Load the raw adata
adata_path = os.path.join(in_data_dir, in_filename)
adata = sc.read(adata_path)

adata.raw = adata  # keep full dimension safe
sc.pp.highly_variable_genes(
    adata,
    flavor="seurat_v3",
    n_top_genes=2000,
    layer="counts",
    batch_key="batch",
    subset=True,
)

# Write processed adata
adata_processed_path = os.path.join(out_data_dir, out_filename)
adata.write_h5ad(adata_processed_path)