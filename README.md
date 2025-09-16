# PWA-hydro-conditioning-main
Author: Idil Yaktubay, iyaktubay@iisd-ela.org (IISD-ELA)

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
4) and have ```GDAL``` installed using the ```conda install -c conda-forge gdal``` on command line. You can verify the install with ```gdalinfo --version```.

## Setup Instructions
### 1. Clone this repository and the pwa-tools repository
1.1 Open the Visual Studio Code app on your desktop.
1.2 Open a new Powershell terminal by using the toolbar on the top left corner.

<img width="604" height="146" alt="image" src="https://github.com/user-attachments/assets/d3960591-8bfb-49e4-8c2c-9ad2cfa8a521" />

Your terminal should look something like this:

<img width="774" height="159" alt="image" src="https://github.com/user-attachments/assets/6c2e96e4-fb07-4790-b710-70f393fbacd4" />

1.3 Clone this repository to your workspace by running the following command:
```bash
git clone https://github.com/IISD-ELA/PWA-hydro-conditioning-main.git
```
1.4 In the same workspace, clone the [pwa-tools repository](https://github.com/IISD-ELA/PWA-hydro-conditioning-tools) by running the following command:
```bash
git clone https://github.com/IISD-ELA/PWA-hydro-conditioning-tools.git
```

### 2. Install the pwa-tools package
2.1 Make sure you are working in an active conda environment. For example, in my case, the ```pwa_dev``` environment is active:

<img width="731" height="59" alt="image" src="https://github.com/user-attachments/assets/9c70f1bd-080a-4ab3-a03e-f12206abf1db" />

2.2 cd into the cloned ```PWA-hydro-conditioning-tools``` folder by running the following command:
```bash
cd PWA-hydro-conditioning-tools
```
Your terminal should now look like this:

<img width="772" height="32" alt="image" src="https://github.com/user-attachments/assets/5548fec5-ae87-46fb-92e6-ed6d1065a997" />

2.3 Install the custom ```pwa-tools``` package in editable mode by running the following command. You must install it in editable mode for the pipeline to work correctly.
```bash
pip install -e .
```
2.4 After installation, if the ```pwa-tools``` package was updated in the remote repository, you can locally update the package by uninstalling the package and re-installing it in editing mode:
```bash
pip uninstall pwa-tools
```
```bash
pip install -e .
```
### 3. Prepare the input data
Create a ```Data/``` folder inside the ```PWA-hydro-conditioning-main``` folder and download and extract the following zip files into it:
- Watershed of interest based on outlet point from the [CLRH Hydrofabrics website](https://hydrology.uwaterloo.ca/CLRH/Hydrofabric.html) (e.g., ID: 05OE006 for Manning Canal)
- Streams dataset of interest from [NHN streams website](https://ftp.maps.canada.ca/pub/nrcan_rncan/vector/geobase_nhn_rhn/shp_en/) (e.g., ngn_rhn_05oe000_shp_en.zip for Manning Canal)
- Raster DEM(s) of interest from [LiDAR DEMs](https://mli.gov.mb.ca/dems/index_external_lidar.html) (e.g., Seine & Rat 2016 for Manning Canal)

Your local workspace should now have the following structure:
```bash
your-working-directory/
├── PWA-hydro-conditioning-main/
    ├── hydro_condition.py
    ├── README.md
    ├── .gitignore
    └── Data
        └──  ...data files you downloaded...
└── PWA-hydro-conditioning-tools/
    └──  ...repository contents...
```

### 4. Run the hydroconditioning script
4.1 On Visual Studio Code's welcome page, open the ```PWA-hydro-conditioning-main``` folder by clicking "Open folder...":

<img width="450" height="339" alt="image" src="https://github.com/user-attachments/assets/a307cdca-e5ce-4f85-8038-73004327e639" />

4.2 Open up terminal on Visual Studio Code once again if it's not already open and cd into the ```PWA-hydro-conditioning-main``` folder if it's not already there.
4.3 Run the following command to execute the hydro conditioning script. The script will ask you to input your watershed name as well as some file names.
```bash
python hydro_condition.py
```
4.4 Once the script has fully run, you will see the output files under the ```Data\<watershed name you entered when prompted>\HydroConditioning\Processed``` folder:

<img width="396" height="268" alt="image" src="https://github.com/user-attachments/assets/c48b59a7-3551-45eb-99a9-38567594141d" />

You can also see any intermediate files in the ```...\Interim``` folder:

<img width="404" height="304" alt="image" src="https://github.com/user-attachments/assets/37a4b00b-21c6-4825-9036-143331cf4745" />

The output files include a depression depths raster .tif, depression depths shapefile, and a zonal statistics file for your watershed by default, as well as a wetland polygons shapefile with statistics (area, total storage, and median depth) if the user chooses to generate it.




