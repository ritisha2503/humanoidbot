from src.stt import speech_to_text
from src.tts import text_to_speech

import os
import platform
import tempfile
from pathlib import Path
import speech_recognition as sr

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

output_dir = Path("output_speech")
output_dir.mkdir(parents=True, exist_ok=True)

recognizer = sr.Recognizer()

# 1. Capture Audio from Microphone
with sr.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjusting for background noise
    print("Microphone is live! Say something...")
    audio_data = recognizer.listen(source)
    print("Recording captured. Processing Speech-to-Text...")

# 2. Save captured mic input to a temporary file
with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
    temp_audio_file.write(audio_data.get_wav_data())
    temp_file_path = temp_audio_file.name

# 3. Run Speech-to-Text (STT)
stt_result = speech_to_text(temp_file_path)

print("\n--- STT Result ---")
if stt_result['success']:
    transcribed_text = stt_result['text']
    print(f"User Said: \"{transcribed_text}\"")
    
    # 4. Pass the transcribed text into Text-to-Speech (TTS)
    print("\nProcessing Text-to-Speech...")
    tts_result = text_to_speech(transcribed_text)
    
    print("\n--- TTS Result ---")
    if tts_result['success']:
        audio_path = tts_result['audio_path']
        print("Success! Audio generated successfully.")
        print(f"Saved audio response to: {audio_path}")
        print(f"Audio payload size: {len(tts_result['audio_bytes'])} bytes")
        
        # 5. Play back the generated audio file automatically
        print("\nPlaying audio output...")
        current_os = platform.system()
        if current_os == "Windows":
            os.startfile(audio_path)
        elif current_os == "Darwin":  # macOS
            os.system(f"afplay '{audio_path}'")
        else:  # Linux
            os.system(f"xdg-open '{audio_path}'")
    else:
        print(f"TTS Error encountered: {tts_result['error']}")
        
else:
    print(f"STT Error encountered: {stt_result['error']}")

# 6. Clean up the temporary microphone recording file
if os.path.exists(temp_file_path):
    os.remove(temp_file_path)