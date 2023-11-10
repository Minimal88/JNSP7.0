# JNSP 7.0 GNSS Academy Certification

This repository contains code and documentation for the software deliverables of the JNSP 7.0 GNSS Academy Certification program. 

## Overview

The certification covers topics like:

- GNSS fundamentals and architecture
- GNSS signals and measurements
- GNSS receivers and antennas  
- GNSS applications and services

The code is written in Python using Anaconda on Linux. The Jupyter notebooks contain the main analysis and results.

## Getting Started

To use this repository:

1. Clone the repository: `git clone https://github.com/Minimal88/JNSP7.0.git`
2. Install Anaconda for Python 3.x
3. Create a conda environment: `conda create --name gnss-env python=3.8`
4. Activate the environment: `conda activate gnss-env` 
5. Install required packages: `pip install -r requirements.txt`
6. Launch Jupyter notebook: `jupyter notebook`
7. Open and run the Jupyter notebooks in the `notebooks/` folder

## Running Commands

Here are some example commands to run the code:

- Process GNSS data: `python WP0_RCVR_ANALYSIS/SRC/receiver_analysis.py ../SCEN/SCEN_TLSA00615-GPSL1-SPP` 


## Repository Structure

    .
    ├── data/               # Example input data
    ├── notebooks/          # Jupyter notebooks for course modules 
    ├── results/            # Output from notebooks
    ├── src/                # Python source code
    ├── requirements.txt    # Required Python packages
    └── README.md           # This README file
    
## Credits

This repository was created by Esteban Martinez as a certification candidate for the GNSS Academy Certification Program offered by [GNSS Academy](https://gnssacademy.com/).
