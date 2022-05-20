pyuic5.exe .\ui\mainwindow.ui -o .\ui\mainwindow.py
pyuic5.exe .\plugin\builtin\basicAnalysis\ui\basicAnalysis.ui -o .\plugin\builtin\basicAnalysis\ui\basicAnalysis.py
pyuic5.exe .\plugin\builtin\fastFourierTranformation\ui\fft.ui -o .\plugin\builtin\fastFourierTranformation\ui\fft.py

python __main__.py