let mediaRecorder;
let audioChunks = [];

const recordBtn = document.getElementById("recordBtn");
const output = document.getElementById("output");
const transcriptionDiv = document.getElementById("transcription");
const assessmentDiv = document.getElementById("assessment");

output.style.display = "none";

navigator.mediaDevices.getUserMedia({ audio: true })
  .then(() => console.log("Mic permission granted"))
  .catch(err => {
    alert("Microphone access denied. Please allow mic permissions.");
    console.error(err);
  });

recordBtn.onclick = async () => {
  if (recordBtn.innerText.includes("Start")) {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.start();
    audioChunks = [];

    mediaRecorder.ondataavailable = (e) => audioChunks.push(e.data);

    recordBtn.innerText = "⏹️ Stop Recording";
  }

  else {
    mediaRecorder.stop();
    recordBtn.innerText = "🎙️ Start Recording";

    mediaRecorder.onstop = async () => {
      output.style.display = "block";

      transcriptionDiv.innerText = "Transcribing audio…";
      assessmentDiv.innerHTML = "Analyzing symptoms…";

      const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
      const formData = new FormData();
      formData.append("audio", audioBlob, "audio.webm");

      try {
        const res = await fetch("http://127.0.0.1:5000/process_audio", {
          method: "POST",
          body: formData,
        });

        const data = await res.json();

        transcriptionDiv.innerText =
          data.transcription || "No speech detected";

        assessmentDiv.innerHTML = `
          <p><strong>Severity:</strong> ${data.severity}</p>
          <p><strong>Symptoms:</strong> ${
            data.symptoms.length ? data.symptoms.join(", ") : "None detected"
          }</p>
          <p><strong>Medicines:</strong> ${
            data.medicines.length ? data.medicines.join(", ") : "None mentioned"
          }</p>
          <p><strong>Possible Conditions:</strong> ${
            data.possible_conditions.length
              ? data.possible_conditions.join(", ")
              : "Not identified"
          }</p>
          <p><strong>Alerts:</strong> ${
            data.alerts.length ? data.alerts.join(", ") : "None"
          }</p>
        `;
      } catch (err) {
        transcriptionDiv.innerText = "Error processing audio";
        assessmentDiv.innerText = "Backend connection failed";
        console.error(err);
      }
    };
  }
};

