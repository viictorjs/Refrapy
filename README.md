![alt text](https://github.com/viictorjs/Refrapy/blob/master/refrapy_logo.png)

## Summary

[Introduction to the software and installation of dependencies](#introduction)

[Using Refrapick for first-break picking](#refrapick)

[Using Refrainv to calculate velocity models](#refrainv)

[Have a question or found a problem?](#reporting-errors-and-asking-questions)

[Citing Refrapy](#citation)

## Introduction

Refrapy is a Python software package with a graphical interface for seismic refraction data analysis.

It is based on two modules: Refrapick and Refrainv.

All main dependencies are listed below:
   ```
   obspy=1.3.0
   pygimli=1.2.6
   numpy=1.19.5
   scipy=1.8.0
   matplotlib=3.5.1
   ```

It is recommended the use of Anaconda (https://www.anaconda.com/), because it simplifies package management.
Once it is installed, run the following commands on the Anaconda prompt (**tested on Windows 10 system, with Python 3.8.13**):

   ```
   conda create -n refrapy python=3.8
   conda activate refrapy
   conda install obspy
   conda install -c gimli -c conda-forge pygimli
   pip install pmw
   ```
    
Once all the necessary packages are installed, extract Refrapick.py, Refrainv.py and the images folder to a directory on your computer. Sample data are also available for download.

### Instalation through Environment and Miniconda

You can install a bare minimum conda version by installing miniconda from (https://docs.conda.io/en/latest/miniconda.html) 
In the Anaconda console you can then clone the working conda environment for this version of Refrapy by executing 

   ```
   conda env create -f refrapy_environment.yml
   ```
   
You can execute the Python files by running:

   ```
   python Refrapick.py
   python Refrainv.py
   ```

## Refrapick

The Refrapick program is used for basic waveform processing and for first breaks picking. The software is aimed to work mainly around SEG2 files, but all waveform formats readable by ObsPy (https://www.obspy.org/) can be used. However, there are a few conditions that need to be considered when reading multichannel waveform data. Waveform **files with missing data traces cannot be used as input**, which can occur with files that have already passed through some other processing software, where one or more traces were removed manually, probably due to being bad noisy data. Thus, **it is recommended the use of original files (i.e., without any editing)**. Also, receivers and source position may not be well defined in the file header or may fail to be properly read. **In such cases, instead of obtaining this information automatically (conventional attempt), dialog boxes appear so that the user can enter these required values**.

### Video tutorial - Basic waveform processing and first-break picking
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/3a9eZW4WKjI/0.jpg)](https://www.youtube.com/watch?v=3a9eZW4WKjI)


## Refrainv

The Refrainv program is used to run a time-terms and a traveltimes tomography inversion. The latter is powered by pyGIMLi (https://www.pygimli.org/). The program presents an individual frame for each inversion method, where each frame has three main panels: the traveltime plotting panel (upper left), used to view and interact with the observed data; the fit and editing panel (upper right), used to edit traveltimes, by clicking on data points and dragging them up or down, and to view the graphical fit between the observed and calculated traveltimes; and the velocity model plotting panel (bottom). 

### Video tutorial - Calculate velocity models from data inversion
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/rOJjxoc2cbU/0.jpg)](https://www.youtube.com/watch?v=rOJjxoc2cbU)

## Reporting errors and asking questions

We encourage users to open an issue in this repository when encountering an error or when in doubt about a functionality or any other subject regarding the use of the software. Please keep in mind that, in its current state, Refrapy is mantained by few active contributors that are not always available for development, so bug fixing might take some time to be properly adressed.

## Citation

If you use Refrapy in your work, please consider citing the following paper:

*Guedes, V.J.C.B., Maciel, S.T.R., Rocha, M.P., 2022. Refrapy: A Python program for seismic refraction data analysis, Computers and Geosciences. https://doi.org/10.1016/j.cageo.2021.105020.*
