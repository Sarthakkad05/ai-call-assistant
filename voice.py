from openai import OpenAI
import uuid
from dotenv import load_dotenv

import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import tempfile
import time


load_dotenv()
client = OpenAI()


# -------- SPEECH → TEXT --------
def speech_to_text(audio_path: str) -> str:
    with open(audio_path, "rb") as audio:
        transcript = client.audio.transcriptions.create(
            model="gpt-4o-transcribe",
            file=audio,
            language="en"
        )
    return transcript.text


# -------- TEXT → SPEECH --------
def text_to_speech(text: str) -> str:
    output_file = f"response_{uuid.uuid4().hex}.mp3"

    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    ) as response:
        response.stream_to_file(output_file)

    return output_file

# -------- TEMPORARY MIC UNTILL WE CONNECT WITH ACTAUL PHONES --------

def record_from_mic(
    sample_rate=16000,
    silence_threshold = 0.005,
    silence_duration=1.0,
    max_duration=15
) -> str:
    """
    Records audio until silence is detected.
    """

    print("🎤 Listening...")

    frames = []
    silence_start = None
    start_time = time.time()

    def callback(indata, frames_count, time_info, status):
        nonlocal silence_start
        volume = np.sqrt(np.mean(indata**2))

        frames.append(indata.copy())

        if volume < silence_threshold:
            if silence_start is None:
                silence_start = time.time()
        else:
            silence_start = None

    with sd.InputStream(
        samplerate=sample_rate,
        channels=1,
        dtype="float32",
        callback=callback
    ):
        while True:
            time.sleep(0.1)

            if silence_start and (time.time() - silence_start) > silence_duration:
                break

            if time.time() - start_time > max_duration:
                break

    audio = np.concatenate(frames, axis=0)

    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    write(temp_file.name, sample_rate, audio)

    return temp_file.name


# def record_from_mic(duration=5, sample_rate=16000) -> str:
#     print("🎤 Listening...")
#     recording = sd.rec(
#         int(duration * sample_rate),
#         samplerate=sample_rate,
#         channels=1,
#         dtype="int16"
#     )
#     sd.wait()

#     temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
#     write(temp_file.name, sample_rate, recording)

#     return temp_file.name