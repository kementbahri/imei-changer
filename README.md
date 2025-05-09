# IMEI Changer Tool

Android cihazların IMEI numarasını değiştirmek için kullanılan basit bir araç.

## Özellikler
- Bağlı cihazları otomatik tespit
- Mevcut IMEI görüntüleme
- IMEI değiştirme
- Kullanıcı dostu arayüz

## Kurulum

1. Python'u yükleyin (https://www.python.org/downloads/)
2. ADB'yi yükleyin (https://developer.android.com/studio/releases/platform-tools)
3. Gerekli kütüphaneleri yükleyin:
   ```
   pip install -r requirements.txt
   ```

## Kullanım

1. Telefonu USB ile bilgisayara bağlayın
2. USB hata ayıklamayı açın
3. Programı çalıştırın:
   ```
   python imei_changer.py
   ```
4. Cihazı seçin ve yeni IMEI'yi girin

## Gereksinimler
- Python 3.7+
- ADB (Android Debug Bridge)
- USB hata ayıklama aktif cihaz 