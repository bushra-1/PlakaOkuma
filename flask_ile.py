from flask import Flask, render_template
from flask_socketio import SocketIO       #?gerçek zamanlı iletişim sağlamak için kullanılır 
import time
import os

app = Flask(__name__)               #? app: Flask uygulaması başlatılır.
socketio = SocketIO(app)

@app.route('/')                             #? @app.route ile URL'leri belirliyoruz
def index():
    return render_template('index.html')

def read_file_and_emit():       #? Dosyadan plaka bilgisi oku ve istemciye gönder 

    last_data = None  # Son okunan veri (değişiklik kontrolü için)  
    
    while True:
        try:
            # Dosyanın varlığını kontrol et
            if os.path.exists('plaka_bilgisi.txt'):
                with open('plaka_bilgisi.txt', 'r') as file:
                    data = file.read().strip()  # Dosyadan veriyi oku ve boşlukları temizle
                    
                    # Eğer veri değişmişse veya ilk defa okunuyorsa
                    if data != last_data:
                        last_data = data  # Son veriyi güncelle
                        if data:  # Eğer veri boş değilse
                            print(f"Güncellenen Veri: {data}")  # Konsola sadece değişiklikleri yazdır
                            # Veriyi istemcilere gönder
                            socketio.emit('update_text', {'data': data})
                        else:
                            print("Dosya boş!")
            else:
                print("plaka_bilgisi.txt bulunamadı!")
        except Exception as e:
            print(f"Bir hata oluştu: {e}")
        
        time.sleep(1)  # Her 1 saniyede bir dosyayı kontrol et

if __name__ == '__main__':
    # Arka plan görevini başlat
    socketio.start_background_task(target=read_file_and_emit)
    # Flask-SocketIO sunucusunu çalıştır
    socketio.run(app, debug=True)
