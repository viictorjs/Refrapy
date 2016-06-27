# Geosis
Geosis is a Python application with a graphic interface for seismic refraction data processing tested on Windows and Linux. It is based on 3 modules: Sispick, Sisref and Sisconv.

Author: Victor Guedes, e-mail: vjs279@hotmail.com

- Sispick is a module to process seismic sections. It offers a wide set of tools for trace processing, such as: normalize traces against each traces maximum for a better view on lower amplitudes, apply a gain factor on amplitudes, cut superposition of amplitudes, shade positive/negative sides of amplitudes, low pass/high pass filters, first break pricking and others.

- Sisref is the interpretation module. It offers the application of the time-terms method to create a velocity model of the refractor layer.
  
- Sisconv is an individual module which convert SEG2 files into SEGY (header info might be lost).
 
Running the program on Windows:

 - Download and install a Python 3 interpreter from the official website (https://www.python.org/).
    - Recommended: Python 3.4.3
    - Note: check for system compatibility (32 or 64 bits).
    
 - The developer offers a Python 3 program to make it easier and faster to install all the necessary packages on the following website: https://github.com/viictorjs/Geosis-easy-packages-installer-Windows-. By using this method you will not be getting the lastest versions of each package. If you wish to have those you need to install the packages manually (requires internet connection).
 
 - The fastest way to install the necessary packages yourself is by using the Python Package Index. On your command prompt run:
   ```
   C:\Python34\Scripts\pip.exe install numpy
   C:\Python34\Scripts\pip.exe install matplotlib
   C:\Python34\Scripts\pip.exe install scipy
   C:\Python34\Scripts\pip.exe install obspy
   ```
    
- Once you have all the necessarty packages installed, extract the Geosis.py file and the 'imagens' folder to a directory on your computer then double-click Geosis.py to run the program.
