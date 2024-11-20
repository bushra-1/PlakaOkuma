import cv2
import pytesseract
import os
import re
import json

# Tesseract yolunu belirtin
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

def plaka_ocr(ayrik_karakterler):
    # Dosyanın varlığını kontrol et
    if not os.path.exists(ayrik_karakterler):
        print(f"Dosya bulunamadı: {ayrik_karakterler}")
        return ""
    
    # Görseli yükleyin
    img = cv2.imread(ayrik_karakterler)
    
    if img is None:
        print(f"Görsel okuma hatası: {ayrik_karakterler}")
        return ""
    
    # Gri tonlara dönüştürme
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Histogram eşitleme
    gray = cv2.equalizeHist(gray)  # Kontrast artırılarak karakterler daha net hale getirilir

    # Gürültü azaltma (Gaussian bulanıklaştırma)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    # Binarizasyon (Siyah-Beyaz yapmak için)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # OCR'yi uygula
    plaka_metni = pytesseract.image_to_string(thresh, config='--psm 8').strip()  # PSM 8: Tek satır metin

    # Regex ile gereksiz karakterleri temizleme
    plaka_metni = re.sub(r'[^A-Za-z0-9\s]', '', plaka_metni)  

    if plaka_metni.startswith('L'):
        plaka_metni = plaka_metni[1:].strip()  # Başındaki "L"yi kaldır

    return plaka_metni

def plaka_json_yazdir(plaka, dosya_adi="plaka_bilgisi.txt"):
    # JSON formatında veri oluştur
    plaka_verisi = {
        "plaka": plaka
    }
    
    # JSON formatını bir .txt dosyasına yazdır
    with open(dosya_adi, "w", encoding="utf-8") as dosya:
        json.dump(plaka_verisi, dosya, ensure_ascii=False, indent=4)
    
    print(f"Plaka bilgisi JSON formatında '{dosya_adi}' dosyasına yazıldı.")

if __name__ == "__main__":
    # Örnek olarak, karakterler klasöründeki bir resim
    plaka_yolu = 'karakterler/karakter_resim2_1.png'  # Burada dosya yolunu kontrol edin
    tespit_edilen_plaka = plaka_ocr(plaka_yolu)
    
    if tespit_edilen_plaka:
        print(f"Tespit Edilen Plaka: {tespit_edilen_plaka}")
        plaka_json_yazdir(tespit_edilen_plaka)  # Plakayı JSON olarak yazdır
    else:
        print("Plaka tespiti başarısız oldu.")
