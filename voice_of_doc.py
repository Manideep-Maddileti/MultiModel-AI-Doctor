# If you don't use pipenv, uncomment the following:
from dotenv import load_dotenv
load_dotenv()
import os
import subprocess
import platform
from gtts import gTTS
from elevenlabs.client import ElevenLabs

# Step 1a: Setup Text to Speech (TTS) model with gTTS

def text_to_speech_with_gtts_old(input_text, output_filepath):
    language = "en"

    audioobj = gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)


# Step 1b: Setup Text to Speech model with ElevenLabs

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")


def text_to_speech_with_elevenlabs_old(input_text, output_filepath):
    if not ELEVENLABS_API_KEY:
        raise ValueError("ELEVENLABS_API_KEY is not configured.")

    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

    audio = client.text_to_speech.convert(
        text=input_text,
        voice_id="FwuKjlVpi0N3exead7ji",
        output_format="mp3_22050_32",
        model_id="eleven_turbo_v2"
    )

    with open(output_filepath, "wb") as f:
        for chunk in audio:
            f.write(chunk)


# Step 2: Text output to voice using gTTS

def text_to_speech_with_gtts(input_text, output_filepath):
    language = "en"

    audioobj = gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)

    # Play audio only when running locally.
    if os.environ.get("RENDER") != "true":
        os_name = platform.system()

        try:
            if os_name == "Darwin":
                subprocess.run(["afplay", output_filepath], check=True)
            elif os_name == "Windows":
                os.startfile(os.path.abspath(output_filepath))
            elif os_name == "Linux":
                subprocess.run(["mpg123", output_filepath], check=True)
        except Exception as e:
            print(f"Audio playback error: {e}")


# Step 3: Text output to voice using ElevenLabs

def text_to_speech_with_elevenlabs(input_text, output_filepath):
    if not ELEVENLABS_API_KEY:
        raise ValueError("ELEVENLABS_API_KEY is not configured.")

    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

    audio = client.text_to_speech.convert(
        text=input_text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        output_format="mp3_22050_32",
        model_id="eleven_turbo_v2"
    )

    with open(output_filepath, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    print(f"Audio saved to {output_filepath}")

    # Do not try to play audio on the Render server.
    if os.environ.get("RENDER") != "true":
        try:
            if platform.system() == "Windows":
                os.startfile(os.path.abspath(output_filepath))
            elif platform.system() == "Darwin":
                subprocess.run(["afplay", output_filepath], check=True)
            elif platform.system() == "Linux":
                subprocess.run(["mpg123", output_filepath], check=True)
        except Exception as e:
            print(f"Audio playback error: {e}")

    return output_filepath


# Run this test only when executing voice_of_doc.py directly.
# It will NOT run when app.py imports this module.
if __name__ == "__main__":
    input_text = "manideep testing"

    try:
        text_to_speech_with_gtts_old(
            input_text=input_text,
            output_filepath="gtts_testing.mp3"
        )
    except Exception as e:
        print(f"gTTS test failed: {e}")
