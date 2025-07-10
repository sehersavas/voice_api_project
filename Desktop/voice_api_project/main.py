memory_db = {}
from fastapi import FastAPI, UploadFile, File, HTTPException
import uuid
import os
import aiofiles


app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

AUDIO_RESPONSES_DIR = "audio_responses"
os.makedirs(AUDIO_RESPONSES_DIR, exist_ok=True)


ALLOWED_EXTENSIONS = {".wav", ".mp3"}
ALLOWED_MIME_TYPES = {"audio/wav", "audio/x-wav", "audio/mpeg", "audio/mp3"}

def validate_file(file: UploadFile):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Sadece .wav ve .mp3 uzantılı dosyalar kabul edilir.")
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail=f"Geçersiz MIME tipi: {file.content_type}")

@app.post("/webhook/audio")
async def upload_audio(file: UploadFile = File(...)):
    validate_file(file)  # Dosya kontrolü

    file_id = str(uuid.uuid4())  # UUID oluştur
    ext = os.path.splitext(file.filename)[1].lower()  # Dosya uzantısı
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}{ext}")  # Yeni dosya yolu

    # Dosyayı asenkron olarak kaydet
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)

    # Sadece id’yi döndür
    return {"id": file_id}
from fastapi import Path, HTTPException

# Dummy STT ve duygu analizi fonksiyonları
def dummy_stt(file_path: str) -> str:
    return "Bu bir örnek transkript metnidir."

def dummy_sentiment_analysis(text: str) -> str:
    if "iyi" in text or "güzel" in text:
        return "pozitif"
    return "negatif"

@app.post("/process/{file_id}")
async def process_audio(file_id: str = Path(...)):
    possible_extensions = [".wav", ".mp3"]
    file_path = None
    for ext in possible_extensions:
        path = os.path.join(UPLOAD_DIR, f"{file_id}{ext}")
        if os.path.exists(path):
            file_path = path
            break

    if not file_path:
        raise HTTPException(status_code=404, detail="Dosya bulunamadı")

    transcript = dummy_stt(file_path)
    sentiment = dummy_sentiment_analysis(transcript)


    memory_db[file_id] = {
        "transcript": transcript,
        "sentiment": sentiment,
        "tts_path": None  # Şimdilik boş, sonra eklenecek
    }

    return {"id": file_id, "transcript": transcript, "sentiment": sentiment}

@app.get("/results/{file_id}")
async def get_results(file_id: str = Path(...)):
    if file_id not in memory_db:
        raise HTTPException(status_code=404, detail="Sonuç bulunamadı")

    return {
        "id": file_id,
        "transcript": memory_db[file_id]["transcript"],
        "sentiment": memory_db[file_id]["sentiment"],
        "tts_path": memory_db[file_id]["tts_path"]
    }

from gtts import gTTS
@app.post("/tts/{file_id}")
async def generate_tts(file_id: str = Path(...)):
    if file_id not in memory_db:
        raise HTTPException(status_code=404, detail="Bu ID'ye ait metin bulunamadı.")

    transcript = memory_db[file_id]["transcript"]

    if not transcript.strip():
        raise HTTPException(status_code=400, detail="Boş metin sese çevrilemez.")

    tts = gTTS(transcript, lang='tr')
    tts_path = os.path.join(AUDIO_RESPONSES_DIR, f"{file_id}.mp3")
    tts.save(tts_path)

    # Bellekte TTS yolunu güncelle
    memory_db[file_id]["tts_path"] = tts_path

    return {"file_id": file_id, "tts_path": tts_path}



    