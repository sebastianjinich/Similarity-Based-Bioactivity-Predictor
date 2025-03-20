# Similarity-Based Bioactivity Predictor (Dockerized)

## Overview
This script predicts the bioactivity of chemical compounds based on similarity measures. It utilizes molecular fingerprints, similarity functions, and different scoring methods to estimate the activity of unknown compounds relative to a known dataset.


## Data Used in the Predictor

The **Similarity-Based Bioactivity Predictor** is designed to estimate the bioactivity of chemical compounds by comparing them to a reference dataset of known bioactive and inactive molecules. This predictor is particularly useful in **early-stage drug discovery and virtual screening**, where identifying potentially active compounds is crucial.

### Problem Context
Drug discovery is a costly and time-consuming process. Traditionally, experimental screening is used to test thousands of compounds against biological targets to identify potential drug candidates. Computational methods, such as **similarity-based virtual screening**, provide an alternative by leveraging known structure-activity relationships to predict the bioactivity of new compounds. The predictor implemented here is based on the assumption that **chemically similar compounds tend to exhibit similar bioactivity**.

### Data Requirements
The predictor requires two main datasets:

1. **Known Bioactivity Dataset (`--known_dataset_csv`)**
   - Contains chemical compounds with experimentally validated bioactivity against specific biological targets.
   - Each compound is represented using **SMILES (Simplified Molecular Input Line Entry System)** notation.
   - The dataset is labeled with bioactivity as **active (1) or inactive (0)**.
   - Typically sourced from publicly available databases like **ChEMBL**, which compiles bioactivity data from experimental assays.

   **Example Format:**
   ```
   comp_id,smiles,bioactivity
   CHEMBL101747,CCN1CCC(CC(=O)Nc2n...,1
   CHEMBL101804,O=C(Nc1n[nH]c2nc(-...,1
   CHEMBL102714,Cn1cc(C2=C(c3ccc(C...,0
   ```

2. **Prediction Dataset (`--predict_csv`)**
   - Contains the chemical structures of compounds for which bioactivity predictions are needed.
   - The dataset includes only compound identifiers and their **SMILES representation**, without bioactivity labels.

   **Example Format:**
   ```
   comp_id,smiles
   CHEMBL1078178,N#CCNC(=O)c1ccc(-c...
   CHEMBL1079175,NC1(c2ccc(-c3nc4cc...
   ```

### How the Data is Used

The **Similarity-Based Bioactivity Predictor** operates by evaluating the chemical similarity between a set of known bioactive and inactive compounds and a set of new, unclassified compounds. The algorithm implemented in this predictor follows the baseline similarity-based approach described in the thesis.

- The predictor **computes molecular fingerprints** from the SMILES representation of each compound.
- It then applies **similarity metrics (e.g., Tanimoto, Cosine, Braun-Blanquet)** to compare unknown compounds to the reference dataset.
- Finally, a scoring function (e.g., **max similarity, mean similarity, upper quartile**) determines a **prediction score**, indicating how likely a given compound is to be bioactive.

#### Algorithm Overview

The predictive model is based on the assumption that **chemically similar compounds tend to exhibit similar bioactivity**. To quantify similarity, the algorithm:

1. **Computes Molecular Fingerprints**: Each compound is transformed into a molecular fingerprint representation. The fingerprinting method used by default is ASP (All-Shortest Path), which captures structural information about the molecule. Fingerprints are generated using jCompoundMapper [1] and its Python wrapper [2].
   
2. **Calculates Similarity Scores**: For each query compound, the similarity to every compound in the known bioactivity dataset is computed using the Braun-Blanquet similarity coefficient.
   
3. **Determines the Maximum Similarity per Class**: The algorithm extracts the maximum similarity score of the query compound with active compounds and the maximum similarity with inactive compounds.
   
4. **Applies a Softmax Function**: The two maximum similarity scores (one from the active compounds and one from the inactive compounds) are normalized using a softmax function to obtain a probability-like score for bioactivity prediction.
   
This process results in a final score that represents the likelihood of the compound being bioactive based on its structural similarity to known active and inactive compounds.

## Usage of the container

## What is Docker?
Docker is a platform that allows applications to run inside isolated environments called containers. A container includes everything needed to execute an application, such as libraries, dependencies, and system configurations, ensuring consistency across different computing environments.

This predictor runs inside a Docker container, meaning that all its dependencies are pre-installed and configured within a self-contained environment. This ensures reproducibility and eliminates compatibility issues.

Docker containers are ephemeral, meaning that any data stored inside them will be lost once the container stops or is removed. To persist data, bind mounts are used to link directories from the host machine to the container. This ensures that:
- Input files can be accessed by the container.
- Generated predictions are stored outside the container and persist after execution.

## Requirements
- Docker. [Install Docker](https://docs.docker.com/get-started/get-docker/)
- Properly formatted input data

## Docker Setup
### Option A: Pull Pre-built Docker Image (Recommended)
```sh
docker pull sebastianjinich/similarity_activity_predictor:latest
```

### Option B: Build the Docker Image from Scratch
```sh
docker build -t similarity-predictor .
```

## Running the Docker Container
Execute the script within the Docker container using bind mounts to ensure data persistence.

```sh
docker run -it \
    --mount type=bind,src=./data,dst=/root/similarity_activity_predictor/data \
    --mount type=bind,src=./predictions,dst=/root/similarity_activity_predictor/predictions \
    sebastianjinich/similarity_activity_predictor:04 \
        --known_dataset_csv data/train_data_example.csv \
        --predict_csv data/predict_data_example.csv \
        --output_path_csv predictions/prediction_example.csv
```

### Explanation of the Command
- `docker run -it`: Runs the container interactively.
- `--mount type=bind,src=./data,dst=/root/similarity_activity_predictor/data`: Mounts the local `data/` directory to the container's `/root/similarity_activity_predictor/data/` directory.
- `--mount type=bind,src=./predictions,dst=/root/similarity_activity_predictor/predictions`: Mounts the local `predictions/` directory to the container's `/root/similarity_activity_predictor/predictions/` directory.
- `sebastianjinich/similarity_activity_predictor:04`: Specifies the Docker image to use.
- `--known_dataset_csv data/train_data_example.csv`: Specifies the known dataset CSV file inside the container.
- `--predict_csv data/predict_data_example.csv`: Specifies the dataset containing compounds to predict.
- `--output_path_csv predictions/prediction_example.csv`: Specifies where to save the prediction results.

### Arguments
| Argument | Description | Required | Options |
|----------|-------------|----------|---------|
| `--known_dataset_csv` | Path to the known dataset CSV file. | Yes | Must be in `/root/similarity_activity_predictor/data/` |
| `--predict_csv` | Path to the dataset containing compounds to predict. | Yes | Must be in `/root/similarity_activity_predictor/data/` |
| `--output_path_csv` | Path where the output CSV file will be saved. | Yes | Must be in `/root/similarity_activity_predictor/predictions/` |
| `--fingerprint_type` | Type of fingerprint to use for similarity calculations. | No | `RDKIT`, `LSTAR`, `ASP` (default), `RAD2D` |
| `--similarity_function` | Similarity function used to compare molecules. | No | `BraunBlanquet` (default), `Tanimoto`, `Cosine` |
| `--scoring` | Scoring method used to compute the similarity score. | No | `max` (default), `mean`, `upper_cuartile`, `upper_decile` |

## Directory Mapping
When running the container, the following directories are mounted from the host system to the Docker environment:
- `/data/`: Stores input datasets for training or prediction.
- `/predictions/`: Stores the output prediction results.

### Modes of Running Docker
Docker containers can be executed in different modes depending on the use case:

- **Interactive Mode (`-it`)**: Runs the container in an interactive session where commands can be executed manually. Useful for debugging.
  ```sh
  docker run -it similarity-predictor ...
  ```
- **Detached Mode (`-d`)**: Runs the container in the background, useful for long-running processes.
  ```sh
  docker run -d similarity-predictor ...
  ```

To check running containers in detached mode:
```sh
docker ps
```
To stop a running container:
```sh
docker stop <container_id>
```

## Example Scripts
There are example scripts available in the repository:
- `run_prediction_example.sh`: Example script to execute a prediction.

Run it using:
```sh
bash run_prediction_example.sh
```

## Input and Output Examples

### Input Files
The script requires two CSV files as input:

#### 1. Known Dataset (`train_data_example.csv`)
This file contains a list of compounds with known bioactivity.

Example format:
```
comp_id,smiles,bioactivity
CHEMBL101747,CCN1CCC(CC(=O)Nc2n...,1
CHEMBL101804,O=C(Nc1n[nH]c2nc(-...,1
CHEMBL102714,Cn1cc(C2=C(c3ccc(C...,0
```
- `comp_id`: Unique compound identifier.
- `smiles`: SMILES representation of the compound.
- `bioactivity`: Bioactivity label (1 for active, 0 for inactive).

#### 2. Prediction Dataset (`predict_data_example.csv`)
This file contains compounds for which bioactivity predictions will be made.

Example format:
```
comp_id,smiles
CHEMBL1078178,N#CCNC(=O)c1ccc(-c...
CHEMBL1079175,NC1(c2ccc(-c3nc4cc...
```
- `comp_id`: Unique compound identifier.
- `smiles`: SMILES representation of the compound.

### Output File
The output file (`prediction_example.csv`) contains the prediction results.

Example format:
```
comp_id,smiles,prediction_score
CHEMBL1078178,N#CCNC(=O)c1ccc(-c...,0.85
CHEMBL1079175,NC1(c2ccc(-c3nc4cc...,0.23
```
- `comp_id`: Unique compound identifier.
- `smiles`: SMILES representation of the compound.
- `prediction_score`: Predicted bioactivity score (higher values indicate stronger activity predictions).

## Output
The script generates a CSV file containing predictions. The output file retains all columns from the `predict_csv` dataset and appends a new column called `prediction_score`. The results are stored in the `predictions/` directory inside the container.

## Error Handling
- If an invalid fingerprint type, similarity function, or scoring method is provided, the script raises an error listing valid options.
- If any required file is missing or improperly formatted, the script exits with an appropriate error message.

## References

[1] Hinselmann, G., Rosenbaum, L., Jahn, A. et al. jCompoundMapper: An open source Java library and command-line tool for chemical fingerprints. J Cheminform 3, 3 (2011). https://doi.org/10.1186/1758-2946-3-3

[2] jCompoundMapper Python wrapper: https://github.com/OlivierBeq/jCompoundMapper_pywrapper

## License
This script is provided as-is with no warranties. Usage and modifications are permitted under the applicable open-source license.

