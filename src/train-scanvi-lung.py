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
out_model_dir = "/local/home/savchuki/projects/swarm-atlas/results/scanvi"
in_filename = "lung-atlas-public-processed.h5ad"
out_model_name = "scanvi-lung.pt"
in_data_path = os.path.join(in_data_dir, in_filename) # path to processed adata
model_result_path = os.path.join(out_model_dir, out_model_name) # path to trained scanvi model

adata = sc.read(in_data_path)

# load trained scvi model
scvi_model = scvi.model.SCVI.load(in_model_dir, adata=adata)

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

scanvi_model.save(out_model_dir, overwrite=True)
print("-----SAVED SCANVI MODEL-----")
