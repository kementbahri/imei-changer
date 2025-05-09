# Yönetici izni kontrol et
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Warning "Yonetici izni gerekli. Yeniden baslatiliyor..."
    Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

Write-Host "IMEI Changer Kurulum Basladi..." -ForegroundColor Green
Write-Host ""

# Python kurulumu kontrol et
try {
    $pythonVersion = python --version
    Write-Host "Python zaten yuklu: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Python bulunamadi. Yukleniyor..." -ForegroundColor Yellow
    $pythonUrl = "https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe"
    $pythonInstaller = "$env:TEMP\python-installer.exe"
    Invoke-WebRequest -Uri $pythonUrl -OutFile $pythonInstaller
    Start-Process -FilePath $pythonInstaller -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1" -Wait
    Remove-Item $pythonInstaller
}

# ADB klasörü oluştur
if (-not (Test-Path "C:\Android\platform-tools")) {
    Write-Host "ADB yukleniyor..." -ForegroundColor Yellow
    $adbUrl = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
    $adbZip = "$env:TEMP\platform-tools.zip"
    Invoke-WebRequest -Uri $adbUrl -OutFile $adbZip
    
    # ZIP'i çıkart
    Expand-Archive -Path $adbZip -DestinationPath "C:\Android" -Force
    Remove-Item $adbZip
    
    # PATH'e ADB'yi ekle
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
    if (-not $currentPath.Contains("C:\Android\platform-tools")) {
        [Environment]::SetEnvironmentVariable("Path", "$currentPath;C:\Android\platform-tools", "Machine")
    }
}

# Gerekli kütüphaneleri yükle
Write-Host "Gerekli kutuphaneler yukleniyor..." -ForegroundColor Yellow
pip install PyQt5==5.15.9
pip install pure-python-adb==0.3.0

# Programı çalıştır
Write-Host "`nKurulum tamamlandi!" -ForegroundColor Green
Write-Host "Program baslatiliyor..." -ForegroundColor Green
python imei_changer.py

Write-Host "`nCikmak icin bir tusa basin..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 