![alt text](https://github.com/viictorjs/Refrapy/blob/master/refrapy_logo.png)

## Introduction

Refrapy is a Python software package with a graphical interface for seismic refraction data analysis. 

It is based on two modules: Refrapick and Refrainv.

The Refrapick program is used for basic waveform processing for first breaks picking. The waveform reading is powered by ObsPy (https://www.obspy.org/).

The Refrainv program is used to run a time-terms and a traveltimes tomography inversion. The latter is powered by pyGIMLi (https://www.pygimli.org/).

All dependencies are listed below:
   ```
   numpy
   matplotlib
   scipy
   obspy
   pygimli
   tkinter
   ```

It is recommended the use of Anaconda (https://www.anaconda.com/), because it simplifies package management.
Once it is installed, open run the following commands on Anaconda prompt:

   ```
   conda create -n refrapy python=3.7.7
   conda activate refrapy
   conda install obspy
   conda install -c gimli -c conda-forge pygimli=1.0.12
   ```
    
Once all the necessarty packages are installed, extract Refrapick.py, Refrainv.py and the images folder to a directory on your computer. 

You can execute the python files by running:

   ```
   python Refrapick.py
   python Refrainv.py
   ```

## Refrapick

**Open waveform files**: the software is aimed to work mainly around SEG2 files, but all waveform formats readable by ObsPy can be used. However, there are a few conditions that need to be considered when reading multichannel waveform data. Waveform **files with missing data traces cannot be used as input**, which can occur with files that have already passed through some other processing software, where one or more traces were removed manually, probably due to being bad noisy data. Thus, **it is recommended the use of original files (i.e., without any editing)**. Also, receivers and source position may not be well defined in the file header or may fail to be properly read. In such cases, instead of obtaining this information automatically (conventional attempt), dialog boxes appear so that the user can enter these required values.

![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/open_waveform.gif)

**Basic waveform processing**: Normalization divides amplitudes by each trace’s maximum amplitude. Scale gain divides (decrease gain) or multiplies (increase gain) the amplitudes of the current section by a fixed factor. High pass/Low pass filters removes unwanted frequency content of the current section, where each consecutive application will assign a new frequency limit following a fixed factor. Traces can be plotted with the filling of the positive/negative side of amplitudes or as simple wiggles (no filling). A trimming mode can be enabled/disabled: clicking on the plotting screen will assign the y value of the clicked position as a limit, where all samples in the current section after that time will be removed. This function is particularly useful when there are data sets with high sampling frequency, where **removing samples might speed up the performance of other functions**.

![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/norm_gain_fill.gif)
![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/filters.gif)
![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/trim_samples.gif)

**Get apparent velocity of layers**: An interaction mode can be enable/disable to obtain the apparent velocity of a layer (Va), that can be estimated by drawing a straight line on the current section, where the inverse of the calculated slope of the line is plotted as Va.

![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/apparent_velocity.gif)

**Picking first breaks**: An interaction mode can be enabled/disabled for first breaks picking. Picks can be made individually with single clicks or several at once. The latter can be done by drawing a straight line through the section, where intersections with traces will be marked as picks. Only one pick can be created per trace, so that a pick already made will be changed to a new y value if a new click occurs. A line connecting all the picks of the current section can be plotted. All picks of the current section can be removed. A preview of the resulting traveltime curves can be checked any time, with an interaction mode to  manually highlight erroneous picks and facilitate its identification between sections. Figure functions (e.g. zoom, pan) are available in the Matplotlib's toolbar.

![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/pick.gif)
![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/pick2.gif)
![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/pick3.gif)

If a new data set is to be analyzed or if it is necessary to open more sections in addition to those already read, this function should be used, it is necessary to reset all memory and plotting screens.

![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/reset.gif)

## Refrainv

Run the time-terms inversion:

![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/timeterms_inv1.gif)
![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/timeterms_inv2.gif)
![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/timeterms_inv3.gif)

Run the traveltimes tomography inversion:

![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/tomography_inv1.gif)
![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/tomography_inv2.gif)
![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/tomography_inv3.gif)


Author: Victor Guedes, e-mail: vjs279@hotmail.com
