import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QPushButton, QLineEdit, QLabel, QComboBox, QMessageBox)
from PyQt5.QtCore import Qt
import subprocess

class IMEIChanger(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IMEI Değiştirici")
        self.setGeometry(100, 100, 500, 400)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
            QLabel {
                font-size: 14px;
                color: #333;
            }
            QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
        """)
        
        # Ana widget ve layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Başlık
        title_label = QLabel("IMEI Değiştirici")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333; margin-bottom: 20px;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Cihaz seçimi
        layout.addWidget(QLabel("Bağlı Cihazlar:"))
        self.device_combo = QComboBox()
        layout.addWidget(self.device_combo)
        
        # Yenile butonu
        refresh_button = QPushButton("Cihazları Yenile")
        refresh_button.clicked.connect(self.refresh_devices)
        layout.addWidget(refresh_button)
        
        # Mevcut IMEI gösterimi
        self.current_imei_label = QLabel("Mevcut IMEI: ")
        layout.addWidget(self.current_imei_label)
        
        # Yeni IMEI girişi
        layout.addWidget(QLabel("Yeni IMEI Numarası:"))
        self.new_imei_input = QLineEdit()
        self.new_imei_input.setPlaceholderText("15 haneli IMEI numarası girin")
        layout.addWidget(self.new_imei_input)
        
        # IMEI değiştirme butonu
        change_button = QPushButton("IMEI Değiştir")
        change_button.clicked.connect(self.change_imei)
        layout.addWidget(change_button)
        
        # Durum mesajı
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #666; margin-top: 10px;")
        layout.addWidget(self.status_label)
        
        # İlk cihazları yükle
        self.refresh_devices()

    def refresh_devices(self):
        try:
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
            devices = result.stdout.strip().split('\n')[1:]
            self.device_combo.clear()
            
            for device in devices:
                if device.strip():
                    self.device_combo.addItem(device.split('\t')[0])
            
            if self.device_combo.count() > 0:
                self.show_current_imei()
                self.status_label.setText("Cihazlar başarıyla yüklendi")
            else:
                self.status_label.setText("Bağlı cihaz bulunamadı")
                
        except Exception as e:
            self.status_label.setText(f"Hata: {str(e)}")
            QMessageBox.critical(self, "Hata", f"Cihazlar yüklenirken hata oluştu: {str(e)}")

    def show_current_imei(self):
        try:
            device = self.device_combo.currentText()
            if device:
                result = subprocess.run(['adb', '-s', device, 'shell', 'service', 'call', 'iphonesubinfo', '1'], 
                                     capture_output=True, text=True)
                imei = result.stdout.strip()
                self.current_imei_label.setText(f"Mevcut IMEI: {imei}")
        except Exception as e:
            self.status_label.setText(f"Hata: {str(e)}")

    def change_imei(self):
        try:
            device = self.device_combo.currentText()
            new_imei = self.new_imei_input.text()
            
            if not device:
                QMessageBox.warning(self, "Uyarı", "Lütfen bir cihaz seçin!")
                return
                
            if not new_imei or len(new_imei) != 15:
                QMessageBox.warning(self, "Uyarı", "Geçerli bir IMEI numarası girin (15 haneli)")
                return
            
            # IMEI değiştirme komutu
            command = f'adb -s {device} shell "service call iphonesubinfo 1 i32 1 s16 {new_imei}"'
            subprocess.run(command, shell=True)
            
            self.status_label.setText("IMEI başarıyla değiştirildi!")
            QMessageBox.information(self, "Başarılı", "IMEI başarıyla değiştirildi!")
            self.show_current_imei()
            
        except Exception as e:
            self.status_label.setText(f"Hata: {str(e)}")
            QMessageBox.critical(self, "Hata", f"IMEI değiştirilirken hata oluştu: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = IMEIChanger()
    window.show()
    sys.exit(app.exec_()) 