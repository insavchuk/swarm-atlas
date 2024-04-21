import os
import scanpy as sc
import scvi
import torch

scvi.settings.seed = 0
print("Last run with scvi-tools version:", scvi.__version__)
torch.set_float32_matmul_precision("high")

# Define file names and paths for reading/writing
in_data_dir = "/local/home/savchuki/projects/swarm-atlas/data"
out_model_dir = "/local/home/savchuki/projects/swarm-atlas/results/scvi"
in_filename = "lung-atlas-public-processed.h5ad"
out_model_name = "scvi-lung.pt"
adata_path = os.path.join(in_data_dir, in_filename) # path to processed adata
model_result_path = os.path.join(out_model_dir, out_model_name) # path to trained scvi model

adata = sc.read(adata_path)

scvi.model.SCVI.setup_anndata(adata, layer="counts", batch_key="batch")

model = scvi.model.SCVI(adata, n_layers=2, n_latent=30, gene_likelihood="nb")

print("-----TRAINING SCVI MODEL-----")
model.train()

model.save(out_model_dir, overwrite=True)
print("-----SAVED SCVI MODEL-----")