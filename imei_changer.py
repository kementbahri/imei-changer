import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QPushButton, QLineEdit, QLabel, QComboBox, QMessageBox,
                           QTabWidget, QTextEdit, QHBoxLayout)
from PyQt5.QtCore import Qt
import subprocess

class IMEIChanger(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IMEI Değiştirici")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
            QLabel {
                font-size: 14px;
                color: #333;
            }
            QComboBox {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
            QTabWidget::pane {
                border: 1px solid #ddd;
                border-radius: 4px;
                background: white;
            }
            QTabBar::tab {
                background: #f0f0f0;
                padding: 10px 20px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom: 2px solid #4CAF50;
            }
        """)
        
        # Ana widget ve layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Tab widget oluştur
        tabs = QTabWidget()
        main_layout.addWidget(tabs)
        
        # Ana sekme
        main_tab = QWidget()
        main_layout_tab = QVBoxLayout(main_tab)
        
        # Başlık
        title_label = QLabel("IMEI Değiştirici")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333; margin-bottom: 20px;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout_tab.addWidget(title_label)
        
        # Adım 1: Cihaz Seçimi
        step1_group = QWidget()
        step1_layout = QVBoxLayout(step1_group)
        step1_layout.addWidget(QLabel("Adım 1: Cihaz Seçimi"))
        step1_layout.addWidget(QLabel("Bağlı Cihazlar:"))
        self.device_combo = QComboBox()
        step1_layout.addWidget(self.device_combo)
        refresh_button = QPushButton("Cihazları Yenile")
        refresh_button.clicked.connect(self.refresh_devices)
        step1_layout.addWidget(refresh_button)
        main_layout_tab.addWidget(step1_group)
        
        # Adım 2: Mevcut IMEI ve Root Bilgisi
        step2_group = QWidget()
        step2_layout = QVBoxLayout(step2_group)
        step2_layout.addWidget(QLabel("Adım 2: Mevcut IMEI"))
        self.current_imei_label = QLabel("Mevcut IMEI: ")
        step2_layout.addWidget(self.current_imei_label)
        self.root_status_label = QLabel("Root: Bilinmiyor")
        self.root_status_label.setStyleSheet("color: #007700; font-weight: bold;")
        step2_layout.addWidget(self.root_status_label)
        main_layout_tab.addWidget(step2_group)
        
        # Adım 3: Yeni IMEI
        step3_group = QWidget()
        step3_layout = QVBoxLayout(step3_group)
        step3_layout.addWidget(QLabel("Adım 3: Yeni IMEI Girişi"))
        self.new_imei_input = QLineEdit()
        self.new_imei_input.setPlaceholderText("15 haneli IMEI numarası girin")
        step3_layout.addWidget(self.new_imei_input)
        change_button = QPushButton("IMEI Değiştir")
        change_button.clicked.connect(self.change_imei)
        step3_layout.addWidget(change_button)
        main_layout_tab.addWidget(step3_group)
        
        # Durum mesajı
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #666; margin-top: 10px;")
        main_layout_tab.addWidget(self.status_label)
        
        # Yardım sekmesi
        help_tab = QWidget()
        help_layout = QVBoxLayout(help_tab)
        
        help_text = QTextEdit()
        help_text.setReadOnly(True)
        help_text.setHtml("""
        <h2>IMEI Değiştirici Kullanım Kılavuzu</h2>
        
        <h3>Ön Hazırlık:</h3>
        <ol>
            <li>Telefonunuzda "Ayarlar" > "Telefon Hakkında" > "Derleme numarası"na 7 kez tıklayın</li>
            <li>"Geliştirici Seçenekleri"ne girin</li>
            <li>"USB Hata Ayıklama"yı aktif edin</li>
            <li>Telefonu USB kablosu ile bilgisayara bağlayın</li>
            <li>USB bağlantı modunu "Dosya Aktarımı" olarak ayarlayın</li>
        </ol>
        
        <h3>Program Kullanımı:</h3>
        <ol>
            <li><b>Adım 1:</b> "Cihazları Yenile" butonuna tıklayın ve telefonunuzu listeden seçin</li>
            <li><b>Adım 2:</b> Mevcut IMEI numaranızı kontrol edin</li>
            <li><b>Adım 3:</b> Yeni IMEI numarasını girin (15 haneli olmalı)</li>
            <li><b>Adım 4:</b> "IMEI Değiştir" butonuna tıklayın</li>
            <li><b>Adım 5:</b> Telefonunuzu yeniden başlatın</li>
        </ol>
        
        <h3>Önemli Notlar:</h3>
        <ul>
            <li>IMEI numarası 15 haneli olmalıdır</li>
            <li>İşlem sırasında telefonunuzu çıkarmayın</li>
            <li>Hata durumunda telefonunuzu yeniden başlatın</li>
            <li>Bu işlem telefonunuzun garantisini etkileyebilir</li>
        </ul>
        """)
        help_layout.addWidget(help_text)
        
        # Sekmeleri ekle
        tabs.addTab(main_tab, "IMEI Değiştirici")
        tabs.addTab(help_tab, "Yardım")
        
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
                # Root kontrolü
                root_result = subprocess.run(['adb', '-s', device, 'shell', 'su', '-c', 'id'], capture_output=True, text=True)
                if 'uid=0(root)' in root_result.stdout:
                    self.root_status_label.setText("Root: Var")
                    self.root_status_label.setStyleSheet("color: #007700; font-weight: bold;")
                else:
                    self.root_status_label.setText("Root: Yok")
                    self.root_status_label.setStyleSheet("color: #bb0000; font-weight: bold;")
        except Exception as e:
            self.status_label.setText(f"Hata: {str(e)}")
            self.root_status_label.setText("Root: Bilinmiyor")
            self.root_status_label.setStyleSheet("color: #888; font-weight: bold;")

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
            QMessageBox.information(self, "Başarılı", "IMEI başarıyla değiştirildi!\nLütfen telefonunuzu yeniden başlatın.")
            self.show_current_imei()
            
        except Exception as e:
            self.status_label.setText(f"Hata: {str(e)}")
            QMessageBox.critical(self, "Hata", f"IMEI değiştirilirken hata oluştu: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = IMEIChanger()
    window.show()
    sys.exit(app.exec_()) 