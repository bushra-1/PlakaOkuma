# import os
# import matplotlib.pyplot as plt
# import cv2
# from plaka_tespiti import plaka_konum_dondur

# veri = os.listdir("resimler")

# for image_url in veri:
#     img = cv2.imread("resimler/" + image_url)
#     img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Gri tonlama
#     img_resized = cv2.resize(img_gray, (500, 500))

#     # Plaka konumunu belirle ve çerçeve çiz
#     plaka_konum = plaka_konum_dondur(img)
#     if plaka_konum:
#         x, y, w, h = plaka_konum
#         cv2.rectangle(img_resized, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Yeşil çerçeve

#     plt.imshow(img_resized, cmap="gray")  # Gri tonları görüntülemek için cmap ayarı
#     plt.show()




