@echo off
echo IMEI Changer Kurulum Basladi...
echo.

:: Python kurulumu kontrol et
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python bulunamadi. Yukleniyor...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe' -OutFile 'python-installer.exe'"
    python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python-installer.exe
) else (
    echo Python zaten yuklu.
)

:: ADB klasörü oluştur
if not exist "C:\Android\platform-tools" (
    echo ADB yukleniyor...
    powershell -Command "Invoke-WebRequest -Uri 'https://dl.google.com/android/repository/platform-tools-latest-windows.zip' -OutFile 'platform-tools.zip'"
    powershell -Command "Expand-Archive -Path 'platform-tools.zip' -DestinationPath 'C:\Android' -Force"
    del platform-tools.zip
    
    :: PATH'e ADB'yi ekle
    setx PATH "%PATH%;C:\Android\platform-tools" /M
) else (
    echo ADB zaten yuklu.
)

:: Gerekli kütüphaneleri yükle
echo Gerekli kutuphaneler yukleniyor...
pip install PyQt5==5.15.9
pip install pure-python-adb==0.3.0

:: Programı çalıştır
echo.
echo Kurulum tamamlandi!
echo Program baslatiliyor...
python imei_changer.py

pause 