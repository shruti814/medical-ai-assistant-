import whisper
from nlp_extraction import extract_medical_info
from ai_support import ai_medical_support

model = whisper.load_model("base")

audio_file = "test_audio.mp4"

result = model.transcribe(audio_file)
text = result["text"]

print("\n--- Transcription ---")
print(text)

info = extract_medical_info(text)

print("\n--- Extracted Medical Info ---")
print(info)

ai_result = ai_medical_support(info["symptoms"])

ai_result = {k.strip(): v for k, v in ai_result.items()}

print("\n--- AI Clinical Support ---")
print(ai_result)

medical_record = {
    "patient_id": "PATIENT_001",
    "transcription": text,
    "symptoms": info["symptoms"],
    "medicines": info["medicines"],
    "severity": ai_result["severity"]
}


