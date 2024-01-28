# London Bicycle Hire Data Analysis 🚲📊

This repository is dedicated to the analysis of the Santander London Bicycle Hire data. It includes Python scripts for data retrieval, preprocessing, and analysis to gain insights into bicycle hire patterns.

## Repository Structure 📁

- `src/models/`: Contains predictive models for forecasting bicycle hire demand 📈.
  - `VBaseline.py`: Implements a baseline dummy regressor model that predicts average hourly hire volumes per station 🏙️.
  - `V0.py`: Implements a random forest and hist gbm 🌲
  - `clustering.py`: NOT IMPLEMENTED

- `src/data/`: Includes scripts for data acquisition and transformation 🔄.
  - `ingest.py`: Retrieves bicycle hire and station data from BigQuery and stores it in a local format 💾.
  - `features.py`: Augments the data with temporal features and flags for UK bank holidays 🇬🇧🎉.
  - `transform.py`: Aggregates hire data into hourly intervals and fills gaps to maintain a continuous time series ⏳.



## Usage 🛠️

To utilize the scripts in this repository, please follow these steps:

1. Create a Python (3.11) environment with dependencies listed in `requirements.txt` 🐍.

2. Run the notebooks in order 📒
