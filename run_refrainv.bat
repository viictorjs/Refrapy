set venv=pg126
set anaconda_folder=C:\ProgramData\Anaconda3

:: INSERT YOUR ANACONDA INSTALL FOLDERE ABOVE.


set refrapy_folder=C:\Users\Riedel\Projekte\Seismic_test_data\refrapy\Refrapy
:: INSERT TTHE FOLDER WHERE REFRAPY IS SITTING ABOVE. The folder needs to contain the refrainv.py file


call %anaconda_folder%\Scripts\activate.bat %anaconda_folder%
call activate %venv%

:: Change directory to the relative path that's needed for script
cd %refrapy_folder%

:: Run script at this location
call python "%refrapy_folder%\Refrainv.py"
PAUSE