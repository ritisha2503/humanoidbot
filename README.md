# Voice-Enabled Humanoid Robot

A voice-interactive humanoid robot concept combining speech recognition, large language model (LLM)-based response generation, and speech synthesis to enable natural spoken interaction. The software pipeline is designed to capture a user's speech, convert it to text, generate a concise conversational response, and synthesize that response as audio.

> **Project focus:** Speech-to-Text (STT) · Large Language Models (LLMs) · Text-to-Speech (TTS) · Voice interaction pipeline

## Overview

The project explores how a humanoid robot can communicate with a person through spoken language. Its conversational software is split into modular components:

1. **Audio capture:** Records microphone input and adjusts for ambient noise.
2. **Speech-to-Text (STT):** Uses Faster-Whisper to transcribe spoken English into text.
3. **LLM response generation:** Sends the transcript to the Groq API using the `llama-3.3-70b-versatile` model, with a system prompt designed for warm, concise, speech-friendly responses.
4. **Text-to-Speech (TTS):** Uses Piper TTS and a local ONNX voice model to synthesize a WAV audio response.
5. **Audio output:** Saves the generated audio and opens it for playback.

The code also includes standalone tests for the individual STT and TTS modules, as well as combined STT→TTS and STT→LLM→TTS pipelines.

## Architecture

```text
User speaks
    │
    ▼
Microphone capture
(speech_recognition)
    │
    ▼
Speech-to-Text
(Faster-Whisper, base model)
    │
    ▼
Language understanding and response
(Groq API + Llama 3.3 70B)
    │
    ▼
Text-to-Speech
(Piper + Lessac medium voice)
    │
    ▼
WAV audio response
    │
    ▼
Playback
```

## Technology Stack

| Component | Technology | Role |
|---|---|---|
| Programming language | Python | Orchestrates the voice interaction pipeline |
| Microphone input | `SpeechRecognition` | Captures audio and performs ambient-noise calibration |
| STT | `faster-whisper` | Transcribes English speech using the Whisper `base` model |
| LLM | Groq API, `llama-3.3-70b-versatile` | Generates concise conversational responses |
| TTS | Piper TTS | Produces speech locally from generated text |
| Voice model | Lessac medium ONNX model | Supplies the voice used for speech synthesis |
| Audio format | WAV | Stores synthesized audio output |
| Configuration | `python-dotenv` | Loads the Groq API key from environment variables |

## Key Implementation Details

### Speech-to-Text

- Captures microphone audio and exports it to a temporary WAV file.
- Transcribes the recording with Faster-Whisper using the `base` model, CPU execution, and `int8` compute.
- Explicitly configures English transcription.
- Returns a structured result containing success status, transcript, and error information.

### LLM-Based Response Generation

- Sends the transcript to the Groq chat-completions API using `llama-3.3-70b-versatile`.
- Uses a system prompt intended to make the robot's replies empathetic, natural, concise, and suitable for spoken delivery.
- Limits responses to 150 tokens to keep interactions brief.
- Wraps the API call in error handling and returns a structured response.

### Text-to-Speech

- Uses Piper's locally loaded ONNX voice model to synthesize speech.
- Writes mono, 16-bit PCM WAV audio at the voice model's configured sample rate.
- Creates the output directory automatically and returns both the saved audio path and audio bytes.

### Modular Testing

The repository includes scripts to test STT and TTS separately and to exercise the integrated voice pipeline. This makes it easier to isolate microphone, transcription, API, synthesis, and playback issues during development.

## Repository Layout

The following is the logical layout expected by the imports in the provided code. Adjust names if your actual repository differs.

```text
project/
├── src/
│   ├── stt.py
│   ├── llm.py
│   ├── tts.py
│   └── en_US-lessac-medium.onnx
├── stt_testing.py
├── tts_testing.py
├── stt_tts_testing.py
├── stt_tts_llm_testing.py
├── .env                  # local API key; do not commit
└── output_speech/        # generated WAV files
```

## Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd <your-repository-folder>
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS:**
```bash
source .venv/bin/activate
```

### 3. Install dependencies

Install the packages used by the provided scripts:

```bash
pip install faster-whisper groq python-dotenv SpeechRecognition piper-tts playsound
```

Microphone capture may require a system audio backend such as PortAudio and a compatible `PyAudio` installation. Installation steps vary by operating system.

### 4. Configure the Groq API key

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Keep this file private. Do not commit API keys to version control.

### 5. Add the Piper voice model

Place the `en_US-lessac-medium.onnx` voice model at:

```text
src/en_US-lessac-medium.onnx
```

The provided TTS code expects this exact relative path.

## Running the Pipeline

Run commands from the project root so that the `src` imports and voice-model path resolve correctly.

- **Test speech recognition:**
  ```bash
  python stt_testing.py
  ```
- **Test speech synthesis:**
  ```bash
  python tts_testing.py
  ```
- **Test STT → TTS:**
  ```bash
  python stt_tts_testing.py
  ```
- **Test the complete STT → LLM → TTS pipeline:**
  ```bash
  python stt_tts_llm_testing.py
  ```

The complete test script listens through the microphone, transcribes the input, requests an LLM response, synthesizes the response into a WAV file, and opens the audio for playback.

## Current Scope and Limitations

- The supplied code implements the **voice conversation pipeline** and its test scripts.
- Although the overall project is a humanoid robot that can speak and move, the uploaded files do not show the movement-control, motor-driver, or hardware-integration code. Those parts should be documented separately once their implementation details are available.
- The current LLM prompt mentions future support for interpreting physical commands, but command detection and robot motion control are not implemented in the supplied `llm.py`.
- The provided STT code explicitly targets English.
- The complete pipeline uses a Groq-hosted LLM, so an internet connection and a valid API key are required for response generation. STT and TTS are configured to run locally.
- The scripts are development/testing scripts rather than a packaged application or production deployment.

## Future Improvements

- Add intent classification for commands such as “move forward,” “turn left,” and “stop.”
- Connect recognized intents to a safe, explicit motion-control interface.
- Add a conversational loop with configurable recording timeouts and turn management.
- Improve robustness with retries, clearer logging, and tests for failure cases.
- Explore wake-word detection and streaming STT/TTS to reduce interaction latency.
- Add a hardware integration layer for the robot's controller and actuators.

## CV-Ready Project Description

**Voice-Interactive Humanoid Robot | Python, Faster-Whisper, Groq API, Llama 3.3, Piper TTS**

Developed a modular voice-interaction pipeline for a humanoid robot, integrating English speech recognition with Faster-Whisper, LLM-based conversational response generation through Groq (Llama 3.3 70B), and local speech synthesis using Piper TTS. Implemented microphone capture, temporary audio handling, WAV generation, cross-platform playback, and structured error handling, with standalone tests for individual modules and the end-to-end STT→LLM→TTS workflow.

---

## Notes

- Add photos or a short demo video of the physical robot near the top of this README if available.
- If the robot's movement system is implemented in separate files, add its controller, communication protocol, actuators, and safety behavior to the architecture and documentation.
- Verify dependency versions and the voice-model license before publishing the repository.