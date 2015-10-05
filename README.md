# Geosis
Geosis is an under development Python 3 application with a graphic interface for seismic refraction data processing tested on Windows and Linux.
Current content: 
 - Visualize seismic sections (supported: seg2 and segy);
 - Processing: normalize, energy gain, clip amplitudes superposition, shade amplitudes and filters (low pass/high pass);
 - Editing: first-break picking with real time travel-time curve observation and aparent velocity observation.
 
Running the program on Windows:

 - Download and install a Python 3 interpreter from the official website (https://www.python.org/).
    - Recommended: Python 3.4.3
    - Note: check for system compatibility (32 or 64 bits).
    
 - The developer offers a Python 3 program to make it easier and faster to install all the necessary packages on the following website: https://github.com/viictorjs/Geosis-easy-packages-installer-Windows-. By using this method you will not be getting the lastest versions of each package. If you wish to have those you need to install the packages manually (requires internet connection).
 
 - The fastest way to install the necessary packages yourself is by using the Python Package Index. On your command promp type:
   ```
   C:\Python34\Scripts\pip.exe install numpy
   C:\Python34\Scripts\pip.exe install matplotlib
   C:\Python34\Scripts\pip.exe install scipy
   C:\Python34\Scripts\pip.exe install obspy
   ```
    
- Once you have all the necessarty packages installed, extract the Geosis.py file and the 'imagens' folder to a directory on your computer then double-click Geosis.py to run the program.
