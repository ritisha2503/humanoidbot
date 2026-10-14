from src.stt import speech_to_text

import os
import tempfile
import speech_recognition as sr

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
recognizer = sr.Recognizer()

with sr.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source, duration=1) # adjusting for background noise
    print("Microphone is live! Say something...")
    audio_data = recognizer.listen(source)
    print("Recording captured. Processing with Whisper...")

with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
    # Write the raw microphone data as a valid WAV file
    temp_audio_file.write(audio_data.get_wav_data())
    temp_file_path = temp_audio_file.name

result = speech_to_text(temp_file_path)
print("\nFinal Result:")
if result['success']:
    print(result['text'])
else:
    print(f"Error encountered: {result['error']}")

if os.path.exists(temp_file_path):
    os.remove(temp_file_path)
