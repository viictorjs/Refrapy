![plot](C:\Users\Victor\Desktop\Refrapy\Refrapy)

Refrapy is a Python software with a graphical interface for seismic refraction data analysis. It is based on two modules: Refrapick and Refrainv.

Dependencies:
   ```
   numpy
   matplotlib
   scipy
   obspy
   pygimli
   tkinter
   ```

I recommend installing Anaconda (https://www.anaconda.com/), because it simplifies package management.
Once you have Anaconda installed, open the Anaconda promtp and run the following commands:

   ```
   conda create -n refrapy python=3.7.7
   conda activate refrapy
   conda install obspy
   conda install -c gimli -c conda-forge pygimli=1.0.12
   ```
    
Once you have all the necessarty packages installed, extract Refrapick.py, Refrainv.py and the 'images' folder to a directory on your computer. You can run the python files by running:

   ```
   python Refrapick.py
   python Refrainv.py
   ```

Author: Victor Guedes, e-mail: vjs279@hotmail.com
