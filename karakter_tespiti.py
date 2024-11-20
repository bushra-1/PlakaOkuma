import os
import cv2
import numpy as np

# Karakterlerin kaydedileceği klasör
if not os.path.exists('ayrik_karakterler'):
    os.makedirs('ayrik_karakterler')

# 'karakterler' klasöründeki plaka görselleri
karakter_adresler = os.listdir('karakterler')

def karakteri_tespit_et(karakter_img):
    # Görseli gri tonlara dönüştür
    img_gray = cv2.cvtColor(karakter_img, cv2.COLOR_BGR2GRAY)

    # Kontrastı artırmak için histogram eşitleme
    img_gray = cv2.equalizeHist(img_gray)

    # Görseli ikili (binary) hale getirme, yani siyah ve beyaz
    _, thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Gürültüyü azaltmak için dilatasyon ve erozyon işlemleri
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(thresh, kernel, iterations=1)
    eroded = cv2.erode(dilated, kernel, iterations=1)

    # Karakterlerin etrafındaki konturları tespit et
    cnt, _ = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    karakterler = []
    for c in cnt:
        x, y, w, h = cv2.boundingRect(c)

        # Çok küçük olanları yoksay
        if w > 10 and h > 20:
            karakter = karakter_img[y:y + h, x:x + w]
            karakterler.append(karakter)

    return karakterler

# Her plaka görseli için işlem
for karakter_adresi in karakter_adresler:
    # Görseli oku
    karakter_img = cv2.imread(os.path.join('karakterler', karakter_adresi))

    # Karakterlerin bölümlerini ayır
    ayrik_karakterler = karakteri_tespit_et(karakter_img)

    # Yalnızca karakterleri kaydet (plakanın tam halini değil)
    for idx, ayrik_karakter in enumerate(ayrik_karakterler):
        # Her karakterin kaydedileceği dosya adı
        karakter_kayit_adresi = f"ayrik_karakterler/{karakter_adresi.split('.')[0]}_{idx + 1}.png"
        
        # Karakteri kaydet
        cv2.imwrite(karakter_kayit_adresi, ayrik_karakter)
        print(f"Karakter {idx + 1} kaydedildi: {karakter_kayit_adresi}")
