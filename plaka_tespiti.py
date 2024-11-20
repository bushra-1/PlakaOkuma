import os                                #?Dosya sistemiyle etkileşim kurar
import cv2                               #?OpenCV--> Görüntü işleme, bilgisayarla görme
import matplotlib.pyplot as plt          #?Grafik ve çizim için
import numpy as np                       #?Matematiksel hesaplamalar, matrislerde işlem


# Görsellerin bulunduğu klasör
resim_adresler = os.listdir("resimler")

def plaka_konum_dondur(img):
    
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)                    #? Görseli gri tonlara dönüştürme 
    img_gray = cv2.equalizeHist(img_gray)                               #? Histogram eşitleme--> çok aydınlık veya çok karanlık görüntülerde kontrastı artırarak ayrıntıların daha iyi görünmesini sağlar.

   
    blurred = cv2.GaussianBlur(img_gray, (5, 5), 0)                      #? Gürültü azaltmak ve kenarları vurgulamak için bulanıklaştırma. 5x5 alandaki değerlerin ortalamasını alarak bulanıklık efektini oluşturur
    
    # Kenar tespiti
    edges = cv2.Canny(blurred, 100, 200)                                #?Canny kenar algılama algoritması, bir görüntüdeki kenarları tespit etmek için
    edges = cv2.dilate(edges, np.ones((3, 3), np.uint8), iterations=1)  #?Kenar kalınlaştırma

  
    cnt, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)     #?Kontur tespiti 
    cnt = sorted(cnt, key=cv2.contourArea, reverse=True)                         #? Kontur listesini sıralar

    
    for c in cnt:
        x, y, w, h = cv2.boundingRect(c)                        #?Verilen kontur c için en küçük dikdörtgeni (bounding box) hesaplar
        aspect_ratio = w / h                                    #?Dikdörtgenin en-boy oranını hesaplar


       
        if 100 < w < 400 and 30 < h < 80 and 2 < aspect_ratio < 5:      #? Plaka boyut ve en-boy oranlarına göre alanı kontrol eder

            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  #? Yeşil çerçeve çizer
            plaka = img_gray[y:y+h, x:x+w]                              #? Gri görselden plaka görselini keser
            plaka_yakin = cv2.resize(plaka, (300, 100))                 #? Plakayı daha belirgin hale getirmek için yakınlaştır
            return plaka_yakin, img  

    return None, img

# Her görseli işle
for resim_adresi in resim_adresler:
    
    img = cv2.imread("resimler/" + resim_adresi)            #?OpenCV'nin görüntü okuma fonksiyonudur. Bu fonksiyon, belirtilen dosya yolundaki resmi okur ve bir NumPy dizisine dönüştürür.
    img = cv2.resize(img, (500, 500))                       

    # Plaka tespitini yap
    plaka, img_with_box = plaka_konum_dondur(img)

    # Plaka bulunduysa yakınlaştırılmış gri tonlu olarak göster
    if plaka is not None:
        plt.imshow(plaka, cmap="gray")                          #?Matplotlib kütüphanesinin bir fonksiyonudur ve bir görüntüyü hazırlayıp ekran üzerinde gösterilmesini sağlar
        plt.title(f"Tespit Edilen Plaka - {resim_adresi}")
        plt.show()                                              #?Matplotlib fonksiyonudur ve görüntüyü ekranda gösterir
    else:
        print(f"{resim_adresi} için plaka bulunamadı.")

    
    # Yeşil çerçeveli orijinal görseli göster
    plt.imshow(cv2.cvtColor(img_with_box, cv2.COLOR_BGR2RGB))
    plt.title(f"Orijinal Görsel - {resim_adresi} - Çerçeveli")
    plt.show()  