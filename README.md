![alt text](https://github.com/viictorjs/Refrapy/blob/master/refrapy_logo.png)

## Introduction

Refrapy is a Python software with a graphical interface for seismic refraction data analysis. 

It is based on two modules: Refrapick and Refrainv.

The Refrapick program is used to deal with seismic sections and to pick first breaks. The waveform reading is powered by ObsPy (https://www.obspy.org/).

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

I recommend installing Anaconda (https://www.anaconda.com/), because it simplifies package management.
Once you have it installed, open the Anaconda prompt and run the following commands:

   ```
   conda create -n refrapy python=3.7.7
   conda activate refrapy
   conda install obspy
   conda install -c gimli -c conda-forge pygimli=1.0.12
   ```
    
Once you have all the necessarty packages installed, extract Refrapick.py, Refrainv.py and the 'images' folder to a directory on your computer. 

You can execute the python files by running:

   ```
   python Refrapick.py
   python Refrainv.py
   ```

## Refrapick

Opening waveform files:

![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/open_waveform.gif)

Normalization, gain, fill and clip amplitudes:

![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/norm_gain_fill.gif)

Filters:

![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/filters.gif)

Trimming samples:

![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/trim_samples.gif)

Get apparent velocity of layers:

![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/apparent_velocity.gif)

Picking first breaks:

![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/pick.gif)
![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/pick2.gif)
![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/pick3.gif)

Analyze new data:

![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/reset.gif)

## Refrainv

Run time-terms inversion:

![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/timeterms_inv1.gif)
![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/timeterms_inv2.gif)
![alt text](https://github.com/viictorjs/Refrapy/blob/master/gifs/timeterms_inv3.gif)


Author: Victor Guedes, e-mail: vjs279@hotmail.com
