from src.tts import text_to_speech

import os
from pathlib import Path
from playsound import playsound

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

test_text = "Hello! This is a test of the Piper text to speech engine. If you can hear this, everything is working perfectly."

print(f"Input text for testing: \"{test_text}\"")
print("Processing Text-to-Speech...")

result = text_to_speech(test_text)

print("\nFinal Result:")
if result['success']:
    print("Success! Audio generated successfully.")
    print(f"Saved audio file to: {result['audio_path']}")
    print(f"Audio payload size: {len(result['audio_bytes'])} bytes")
    print("Playing audio output...")

    playsound(result['audio_path'])
    
else:
    print(f"Error encountered: {result['error']}")