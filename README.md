# Geosis
Geosis is a Python 3 based program for seismic refraction data processing tested on Windows.
Current content: visualize waveform data (supported: seg2, segy and mseed), basic trace processing (normalize, gain, clip, shading) and first-break picking (current output is a Seisimager .vs traveltime file).

Running the program on Windows:

 - Step 1: download and install a Python 3 interpreter from the official website (https://www.python.org/).
    - Recommended: Python 3.4.3
    - Note: check for system compatibility (32 or 64 bits).
    
 - Step 2: download and install the necessary Python packages listed bellow:
    - NumPy
    - Future
    - SciPy
    - Six
    - Dateutil
    - Pytz
    - Pyparsing
    - Setuptools
    - Matplotlib
    - Lxml
    - SqlAlchemy
    - ObsPy
    
- Step 3: Extract the Geosis.py script and the 'imagens' folder to a directory on your computer then double-click Geosis.py to run the program.
    
Installing the necessary packages:

- The developer offers a program to make it easier and faster to install all the necessary packages on the following website: https://github.com/viictorjs/Geosis-easy-packages-installer-Windows-. 
- If you choose to install the packages yourself, a simple way to do it is to download the Python Wheels (.whl files) of the listed packages at http://www.lfd.uci.edu/~gohlke/pythonlibs then use pip command lines to install them.
    
  - Installing a package: Go to run > type cmd > type pip install file-name.whl
    - Note 1: you should install the packages following the order in 'Step 2' (some packages are necessary for the installation of other packages). 
    
    - Note 2: in case of error 'pip' is not recognized as an internal or external command, you can try typing the pip.exe location instead of only 'pip' (i.e. C:\Python34\Scripts\pip.exe install file-name.whl).
      
    - Note 3: when typing the pip command line make sure that you are locatted on the folder where the .whl file is. You can use the 'cd folder-name' command line to move around directories or you can tell the exact location of the downloaded Python Wheel (i.e. pip install C:\User\Downloads\file-name.whl).
    



