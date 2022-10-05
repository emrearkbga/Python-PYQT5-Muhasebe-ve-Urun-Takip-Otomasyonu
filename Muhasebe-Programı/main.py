from Anasayfa import *
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QHeaderView
from Muhasebe import Ui_muhasebe


# --------------------------------------------------Uygulama oluşturma ------------------------------------

# Uygulama nesnesi oluşturma
Uygulama = QApplication(sys.argv)  # forumda oluşan argumanları q apllicationa verme
penAna = QMainWindow()  # pencere oluşturma
ui = Ui_MainWindow()  # oluşturulan forma ui classi ile ulaşmak için türetilen nesne
ui.setupUi(penAna)  # oluşturulan pencere ile tasarımdaki form birleştirme


# uygulama2 = QApplication(sys.argv)
penAna2 = QMainWindow()  # pencere oluşturma
ui2 = Ui_muhasebe()  # oluşturulan forma ui classi ile ulaşmak için türetilen nesne
ui2.setupUi(penAna2)  # oluşturulan pencere ile tasarımdaki form birleştirme


penAna.showMaximized()  # pencereyi gösterme

# -----------------------------------------------veritabanı oluşturma --------------------------------------
import sqlite3

global curs  # diğer fonksiyonlarlar değişkenler çalıştırılsın diye global tanımlama yapıldı
global conn


conn = sqlite3.connect('veritabani.db')  # veritabanı diye bir veritabanı oluşturur
curs = conn.cursor()  # cursor veritabanı ile iletişim kurmamızı sağlar

sorguCreTblStok = ("CREATE TABLE IF NOT EXISTS UrunStok(                      \
                 SiparisNum TEXT NOT NULL UNIQUE,                             \
                 Renk TEXT NOT NULL,                                          \
                 Model TEXT NOT NULL,                                         \
                 Beden TEXT NOT NULL,                                         \
                 Komisyon INTEGER NOT NULL,                                      \
                 AlisFiyati INTEGER NOT NULL,                                      \
                 Kargo INTEGER NOT NULL,                                      \
                 SatisFiyati INTEGER NOT NULL,                                 \
                 Kar INTEGER NOT NULL,                                  \
                 SiparisTarihi TEXT NOT NULL)")

curs.execute(sorguCreTblStok)  # veritabanına bu sorgunun çalıştırılacağını iletir
conn.commit()


#--------------------------------veritabanı2--------------------------#

global curs1
global conn1

conn1 = sqlite3.connect('muhasebe.db')  # muhasebe diye bir veritabanı oluşturur
curs1 = conn1.cursor()  # cursor1 veritabanı ile iletişim kurmamızı sağlar

sorguCreTblMhsb = ("CREATE TABLE IF NOT EXISTS Muhasebe(                      \
                 Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,                \
                 Tarih TEXT NOT NULL,                                           \
                 HarcamaYapan TEXT NOT NULL,                                     \
                 Urun TEXT NOT NULL,                                              \
                 Miktar INTEGER NOT NULL)")

curs1.execute(sorguCreTblMhsb)  #veritabanına bu sorgunun çalıştırılacağını iletir
conn1.commit()

#--------------------------------------------Muhasebe Veri Ekle------------------------------#
def mhsbEkle():

    _tarih1 = ui2.mhsb_trh.selectedDate().toString(QtCore.Qt.ISODate)
    _harcama_yapan = ui2.harcama_line.text()
    _urun_adi = ui2.urun_line.text()
    _miktar = ui2.miktar_line.text()

    if (len(_miktar) + len(_harcama_yapan)) > 4:
        curs1.execute("INSERT OR IGNORE INTO Muhasebe(Tarih,HarcamaYapan,Urun,Miktar) VALUES (?,?,?,?)", (_tarih1, _harcama_yapan, _urun_adi, _miktar))
        conn1.commit()
        mhsb_listele()
        ui2.statusbar.showMessage("Ekleme Yapıldı", 500)
    else:
        ui2.statusbar.showMessage("Lütfen boş alanlarını Giriniz",500)


def mhsb_listele():
    ui2.mhsb_widget.clear()
    ui2.mhsb_widget.setHorizontalHeaderLabels(
        ('ID','Tarih','HarcamaYapan','Urun','Miktar'))

    ui2.mhsb_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    curs1.execute("SELECT * FROM Muhasebe")
    for satirIndeks1, satirVeri1 in enumerate(curs1):
        for sutunIndeks1, sutunVeri1 in enumerate(satirVeri1):
            ui2.mhsb_widget.setItem(satirIndeks1, sutunIndeks1, QTableWidgetItem(str(sutunVeri1)))

    ui2.harcama_line.clear()
    ui2.urun_line.clear()
    ui2.miktar_line.clear()

    curs1.execute("SELECT COUNT(*)FROM Muhasebe")
    tpl_kayit1 = curs1.fetchone()
    ui2.gider_label.setText(str(tpl_kayit1[0]))

    curs1.execute("SELECT SUM(Miktar) FROM Muhasebe")
    tpl_kar1 = curs1.fetchall()
    ui2.gider_miktar.setText(str(tpl_kar1))


mhsb_listele()
# -----------------------------------------------Stok ekle--------------------------------------

# Form üzerindeki tüm veriler alınıp bir değişkene aktarılır, sonra bu değişkenler veri tabanına aktarılır

def ekle():
    _siparis_no = ui.siparis_no.text()  # text fonksiyonu ile lineedit içerisindeki texti alıyoruz
    _renk = ui.renk.currentText()  # current text ile comboboxtaki verileri alıyoruz
    _model = ui.model.currentText()
    _beden = ui.beden.currentText()
    _komisyon = ui.komisyon.currentText()
    _kdv = ui.kdv.currentText()
    _alis_fiyati = ui.alis_fiyati.currentText()
    _kargo = ui.kargo.currentText()
    _satis_fiyati = ui.satis_fiyati.text()
    _tarih = ui.tarih.selectedDate().toString(QtCore.Qt.ISODate)
    if (len(_satis_fiyati) + len(_siparis_no)) > 2:
        kdv_orani = ((int(_satis_fiyati) * int(_kdv)) / 100)
        komisyon_ = ((int(_satis_fiyati) * int(_komisyon)) / 100)
        _kar = int(_satis_fiyati) - (int(kdv_orani) + int(_alis_fiyati) + int(komisyon_) + int(_kargo))
        curs.execute("INSERT OR IGNORE INTO UrunStok(SiparisNum,Renk,Model,Beden,Komisyon,AlisFiyati,Kargo,SatisFiyati,Kar,SiparisTarihi) VALUES (?,?,?,?,?,?,?,?,?,?)", (_siparis_no, _renk, _model, _beden, komisyon_ , _alis_fiyati, _kargo, _satis_fiyati, _kar, _tarih))
        conn.commit()  # sorgunun veritabanına gideceğini belirtir
        listele()
    else:
        ui.statusbar.showMessage("Lütfen Sipariş No ve Satış Fiyatı alanlarını Giriniz")


# -----------------------------------------------Table widget listeleme--------------------------------------
def listele():
    ui.tableWidget.clear()
    ui.tableWidget.setHorizontalHeaderLabels(
        ('SiparisNum', 'Renk', 'Model', 'Beden', 'Komisyon', 'AlisFiyati','Kargo','SatisFiyati','Kar','SiparisTarihi'))
    ui.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    curs.execute("SELECT * FROM UrunStok")
    for satirIndeks, satirVeri in enumerate(curs):
        for sutunIndeks, sutunVeri in enumerate(satirVeri):
            ui.tableWidget.setItem(satirIndeks, sutunIndeks, QTableWidgetItem(str(sutunVeri)))

    ui.siparis_no.clear()
    ui.satis_fiyati.clear()

    curs.execute("SELECT COUNT(*)FROM UrunStok")
    tpl_kayit = curs.fetchone()
    ui.urun_tpl.setText(str(tpl_kayit[0]))

    curs.execute("SELECT SUM(SatisFiyati) FROM UrunStok")
    tpl_ciro = curs.fetchall()
    ui.ciro_label.setText(str(tpl_ciro))

    curs.execute("SELECT SUM(Kar) FROM UrunStok")
    tpl_kar = curs.fetchall()
    ui.kar_label.setText(str(tpl_kar))


listele()
#----------------------İADE-------------------------

def iade():
    iade_secme = ui.tableWidget.selectedItems()
    if len(iade_secme) > 0:
        iade_olacak = iade_secme[0].text()
        try:
            curs.execute("UPDATE UrunStok SET Kar=-40, SatisFiyati=0 WHERE SiparisNum='%s'" %(iade_olacak))
            conn.commit()
            ui.statusbar.showMessage("Kayıt Güncelleme İşlemi Gerçekleşti", 500)

            listele()
        except Exception as Hata:
            ui.statusbar.showMessage("Kayıt güncelleme başarısız", 500)
    else:
        ui.statusbar.showMessage("Lütfen tablodan bir satır seçiniz",500)


#---------------------------ÇIKIŞ-----------------------

def cikis():
    cevap = QMessageBox.question(penAna,"ÇIKIŞ", "Programı Kapatmak İstediğinize Emin Misiniz? \n Hazırlayan: Yunus Emre Arikboğa \n İzinsiz kopyalanması telif hakkına tabidir.", \
                         QMessageBox.Yes | QMessageBox.No)
    if cevap==QMessageBox.Yes:
        conn.close()
        sys.exit(Uygulama.exec_())  # çıkış yaparken uygulamayı kapat
    else:
        penAna.showMaximized()


def cikis_mhsb():
    cevap1 = QMessageBox.question(penAna2,"ÇIKIŞ", "Programı Kapatmak İstediğinize Emin Misiniz? \n Hazırlayan: Yunus Emre Arikboğa \n İzinsiz kopyalanması telif hakkına tabidir.", \
                         QMessageBox.Yes | QMessageBox.No)
    if cevap1==QMessageBox.Yes:
        conn1.close()
        sys.exit(Uygulama.exec_())  # çıkış yaparken uygulamayı kapat
    else:
        penAna2.showMaximized()

#---------------------------SİL-----------------------

def sil():
    silme = QMessageBox.question(penAna, "KAYIT SİL", "Seçili Kaydı Silmek İstediğinizden Emin Misiniz?",
                                 QMessageBox.Yes | QMessageBox.No)

    if silme == QMessageBox.Yes:
        secili = ui.tableWidget.selectedItems()
        if len(secili) > 0:
            silinecek = secili[0].text()
            try:
                curs.execute("DELETE FROM UrunStok WHERE SiparisNum='%s'"%(silinecek))
                conn.commit()
                listele()
                ui.statusbar.showMessage("Kayıt Silme İşlemi Gerçekleşti", 500)
            except Exception as Hata:
                ui.statusbar.showMessage("Kayıt Silme İşlemi Başarısız"+ str(Hata), 500)
        else:
            ui.statusbar.showMessage("Lütfen tablodan bir satır seçiniz",500)
    else:
        ui.statusbar.showMessage("Kayıt Silme İşlemi İptal Edildi", 500)

#---------------------------KAYIT ARAMA-----------------------

def gider_silme():
    silme1 = QMessageBox.question(penAna2, "KAYIT SİL", "Seçili Kaydı Silmek İstediğinizden Emin misiniz?",
                                        QMessageBox.Yes | QMessageBox.No)

    if silme1 == QMessageBox.Yes:
        secili1 = ui2.mhsb_widget.selectedItems()
        if len(secili1) > 0:
            silinecek1 = secili1[0].text()
            try:
                curs1.execute("DELETE FROM Muhasebe WHERE Id='%s'"%(silinecek1))
                conn1.commit()
                mhsb_listele()
                ui2.statusbar.showMessage("Kayıt silme işlemi başarıyla gerçekleşmiştir", 500)
            except Exception as Hata1:
                ui2.statusbar.showMessage("Kayıt silme işlemi başarısız", 500)
        else:
            ui2.statusbar.showMessage("Tablodan bir alan seçiniz", 500)



def ara():
    barkod = ui.arama_line.text()
    if len(barkod) > 0:
        try:
            curs.execute("SELECT * FROM UrunStok WHERE SiparisNum=?", barkod)
            conn.commit()
            ui.tableWidget.clear()
            for satirIndeks, satirVeri in enumerate(curs):
                for sutunIndeks, sutunVeri in enumerate(satirVeri):
                    ui.tableWidget.setItem(satirIndeks, sutunIndeks, QTableWidgetItem(str(sutunVeri)))
        except:
            ui.statusbar.showMessage('Lütfen "doğru barkod" no giriniz', 500)
    else:
        ui.statusbar.showMessage("Lütfen arama kutusuna barkod no giriniz", 500)

def muhasebe_ac():
    penAna2.showMaximized()  # pencereyi göster
    penAna.hide()

def stok_ac():
    penAna.showMaximized()
    penAna2.hide()
#-----------------------------------------------Sinyal Slot--------------------------------------


ui.stokEkleBtn.clicked.connect(ekle)
ui.stokGuncelleBtn.clicked.connect(listele)
ui.cikis.clicked.connect(cikis)
ui.stokSilBtn.clicked.connect(sil)
ui.arama_btn.clicked.connect(ara)
ui.muhasebe_gcs_btn.clicked.connect(muhasebe_ac)
ui2.stk_gcs_btn.clicked.connect(stok_ac)
ui.iade_btn.clicked.connect(iade)
ui2.gdr_btn.clicked.connect(mhsbEkle)
ui2.gider_sil.clicked.connect(gider_silme)
ui2.mhsb_cikis.clicked.connect(cikis_mhsb)



sys.exit(Uygulama.exec_())
