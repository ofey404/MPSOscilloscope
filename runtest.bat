pyuic5.exe .\src\ui\mainwindow.ui -o .\src\ui\mainwindow.py
pyuic5.exe .\src\plugin\builtin\basicAnalysis\ui\basicAnalysis.ui -o .\src\plugin\builtin\basicAnalysis\ui\basicAnalysis.py
pyuic5.exe .\src\plugin\builtin\fastFourierTranformation\ui\fft.ui -o .\src\plugin\builtin\fastFourierTranformation\ui\fft.py

python src/
