![alt text](https://github.com/viictorjs/Refrapy/blob/master/refrapy_logo.png)

Refrapy is a Python software with a graphical interface for seismic refraction data analysis. 

It is based on two modules: Refrapick and Refrainv.

The Refrapick program is used to deal with seismic sections and pick first breaks. The waveform reading is powered by ObsPy (https://www.obspy.org/).

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
Once you have Anaconda installed, open the Anaconda prompt and run the following commands:

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

Author: Victor Guedes, e-mail: vjs279@hotmail.com
