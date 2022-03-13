echo Downloading python and installing it to C:\python39 directory
curl -o python3_9_10.exe https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe
python3_9_10.exe PrependPath=1 TargetDir=c:\python39 /passive
echo Wait until the installation is completed
pause

echo Installing pip packages
\python39\Scripts\pip install pyscreenshot
\python39\Scripts\pip install pyopenssl
\python39\Scripts\pip install Pillow

echo To start server open a new terminal and run in src-directory, and accept the firewall request.
echo   python3 server.py
echo
echo To run client run in src-directory:
echo   python3 application.py 127.0.0.1
