# PWA-hydro-conditioning-main

This repository provides a workflow to hydro-condition Prairie watersheds using the ```hydro_condition.py``` script. It is designed for use with the custom [PWA-hydro-conditioning-tools](https://github.com/IISD-ELA/PWA-hydro-conditioning-tools) Python package, and requires certain datasets as input.

## Repository Structure
```bash
PWA-hydro-conditioning-main/                  
├── hydro_condition_py.py       # Main script to run the hydro-conditioning pipeline
├── README.md                   # This documentation
└── .gitignore                  # File that tells Git to ignore the "Data" folder created by the user

```

## Prerequisites
To be able to run this pipeline, the user must have: 
1) installed Anaconda,
2) configured Git and GitHub SSH access linked to their GitHub account and enabled Python extension on Visual Studio code,
3) have familiarity using Windows command line,
4) and have installed ```GDAL``` using the ```conda install -c conda-forge gdal``` conda command.

## Setup Instructions

