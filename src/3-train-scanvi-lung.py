import os
import scanpy as sc
import scvi
import torch

scvi.settings.seed = 0
print("Last run with scvi-tools version:", scvi.__version__)
torch.set_float32_matmul_precision("high")

# Define file names and paths for reading/writing
in_data_dir = "/local/home/savchuki/projects/swarm-atlas/data"
in_model_dir = "/local/home/savchuki/projects/swarm-atlas/results/scvi"
in_model_prefix = "scvi-transplant-"
out_model_dir = "/local/home/savchuki/projects/swarm-atlas/results/scanvi"
in_filename = "lung-atlas-public-transplant-hvgs.h5ad" # Use the same adata as for the scvi model!
out_model_prefix = "scanvi-transplant-"
in_data_path = os.path.join(in_data_dir, in_filename) # path to processed adata

adata = sc.read(in_data_path)

# load trained scvi model
scvi_model = scvi.model.SCVI.load(in_model_dir, prefix=in_model_prefix, adata=adata)

# instantiate scanvi model using scvi model
scanvi_model = scvi.model.SCANVI.from_scvi_model(
    scvi_model,
    adata=adata,
    labels_key = "cell_type",
    unlabeled_category="unknown"
)

# train the model
print("-----TRAINING SCANVI MODEL-----")
scanvi_model.train(max_epochs=20, n_samples_per_label=100)

scanvi_model.save(out_model_dir, prefix=out_model_prefix, overwrite=True)
print("-----SAVED SCANVI MODEL-----")
