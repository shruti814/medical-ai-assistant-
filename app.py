from flask import Flask, request, jsonify, render_template
import os
import whisper
from nlp_extraction import extract_medical_info
from ai_support import ai_medical_support

app = Flask(__name__)
model = whisper.load_model("base")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process_audio", methods=["POST"])
def process_audio():
    try:
        if "audio" not in request.files:
            return jsonify({"error": "No audio file received"}), 400

        audio_file = request.files["audio"]
        if audio_file.filename == "":
            return jsonify({"error": "Empty audio file"}), 400

        file_path = os.path.join(UPLOAD_FOLDER, "temp_audio.webm")
        audio_file.save(file_path)

        result = model.transcribe(file_path)
        transcription = result.get("text", "").strip()

        extracted = extract_medical_info(transcription)

        ai_result = ai_medical_support(extracted["symptoms"])
        ai_result = {k.strip(): v for k, v in ai_result.items()}

        return jsonify({
            "transcription": transcription,
            "symptoms": extracted.get("symptoms", []),
            "medicines": extracted.get("medicines", []),
            "severity": ai_result.get("severity", "UNKNOWN"),
            "possible_conditions": ai_result.get("possible_conditions", []),
            "alerts": ai_result.get("alerts", [])
        })

    except Exception as e:
        print("Backend Error:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
