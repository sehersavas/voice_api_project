# voice_api_project - SES İŞLEME PROJESİ

## Proje Tanımı
Bu proje ile geliştirilen REST API uygulaması ile, .wav ve .mp3 uzantılı ses dosyaları kaydedilip içerikteki ses yazıya çevrilir, yazı analiz edilir, opsiyonel olarak tekrar sese çevirlir, tüm süreç kaydedilir ve sonuca erişim sağlanır.

## Kurulum Talimatları
Bu proje ile geliştirilen API'nin kurulumu ve çalıştırılması aşağıdaki talimatlar ile gerçekleştirilir:

1- Python 3.9 veya üzeri kurulu olmalıdır.
2- Projeyi bilgisayarınıza klonlayın veya indirin:
   ```bash
   git clone https://github.com/sehersavas/voice_api_project.git 
```
3- Proje klasörüne girin :
```bash
 cd voice_api_project 
 ```
4- Sanal ortam (virtual environment) oluşturun ve aktif hale getirin:
* macOS/Linux için:
```bash
python3 -m venv venv
source venv/bin/activate 
```
* Windows için: 
```bash
 python -m venv venv
venv\Scripts\activate
```
5- Gerekli Python kütüphanelerini yükleyin:
```bash
 pip install -r requirements.txt
```
6- API sunucusunu başlatın:
```bash 
uvicorn main:app --reload
```
7- Tarayıcınızdan http://127.0.0.1:8000/docs adresine giderek API'yi test edebilir ve kullanabilirsiniz.

## Kullanılan Kütüphaneler
Python 3.9+
FastAPI (REST API için)
Uvicorn (ASGI sunucusu)
Whisper (Speech-to-Text için)
OpenAI API / Dummy Duygu Analizi
gTTS / pyttsx3 (Text-to-Speech için)
SQLite (veya JSON) veri kaydı
UUID (dosya isimlendirme için)

## API Kullanımı
* POST /webhook/audio
Ses dosyasını (.wav veya .mp3) yükleyip, uploads/ klasörüne UUID ile kaydeder.
Dönen cevapta dosyanın ID'si verilir.
* POST /process/{id}
Daha önce yüklenmiş ses dosyasını ID ile alır, speech-to-text ile yazıya çevirir, metni duygu analizine gönderir ve sonuçları kaydeder.
* POST /tts
Gönderilen metni text-to-speech ile sese çevirir ve audio_responses/ klasörüne kaydeder. Dosya yolu cevapta döner.
* GET /results/{id}
İşlenmiş ses dosyasına ait transkript, duygu analizi sonucu ve varsa TTS dosya yolunu JSON olarak döner.

### Proje Yorumları
Bu projede, ses işleme sürecini geliştirmek için OpenAI'nin ChatGPT modelinden yararlandım.
Yapay zekâ destekli bileşenlerin entegrasyonunu deneyimleyerek, modern API geliştirme pratiklerini uygulama fırsatı buldum.

Projede karşılaştığım en büyük zorluklardan biri, yeni geliştirme ortamlarına adaptasyon süreci oldu. Ayrıca, farklı bileşenlerin (ses dosyası yükleme, speech-to-text, duygu analizi, text-to-speech) test aşamalarının entegre edilmesi ve düzgün çalışmasının sağlanması zaman ve dikkat gerektirdi.

Python konusunda henüz yeni olmama rağmen, bu proje sayesinde hem temel programlama becerilerimi hem de REST API geliştirme yeteneklerimi önemli ölçüde ilerlettim.

Öğrenmeye ve geliştirmeye açık olduğum bu süreçte, gerçek dünyadaki uygulamalara yönelik pratik deneyim kazandım.