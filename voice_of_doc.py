
# if you dont use pipenv uncomment the following:
from dotenv import load_dotenv
load_dotenv()

#Step1a: Setup Text to Speech–TTS–model with gTTS
import os
from gtts import gTTS

def text_to_speech_with_gtts_old(input_text, output_filepath):
    language="en"

    audioobj= gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)


input_text="manideep testing"
text_to_speech_with_gtts_old(input_text=input_text, output_filepath="gtts_testing.mp3")

#Step1b: Setup Text to Speech–TTS–model with ElevenLabs
import elevenlabs
from elevenlabs.client import ElevenLabs

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
def text_to_speech_with_elevenlabs_old(input_text, output_filepath):
    client=ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio= client.text_to_speech.convert(
        text=input_text,
        voice_id="FwuKjlVpi0N3exead7ji",
        output_format="mp3_22050_32",
        model_id="eleven_turbo_v2"
    )

    with open(output_filepath, "wb") as f:
        for chunk in audio:
            f.write(chunk)

#text_to_speech_with_elevenlabs_old(input_text, output_filepath="elevenlabs_testing.mp3")

#Step2: Use Model for Text output to Voice

import subprocess
import platform

def text_to_speech_with_gtts(input_text, output_filepath):
    language="en"

    audioobj= gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath], check=True)
        elif os_name == "Windows":  # Windows
            os.startfile(os.path.abspath(output_filepath))
        elif os_name == "Linux":  # Linux
            subprocess.run(['mpg123', output_filepath], check=True)
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")


#input_text="HiI AM MANIDEEP testing!"
#text_to_speech_with_gtts(input_text=input_text, output_filepath="gtts_testing_autoplay.mp3")


def text_to_speech_with_elevenlabs(input_text, output_filepath):
    client=ElevenLabs(api_key=ELEVENLABS_API_KEY)

    audio=client.text_to_speech.convert(
        text=input_text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        output_format="mp3_22050_32",
        model_id="eleven_turbo_v2"
    )

    with open(output_filepath, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    print(f"Audio saved to {output_filepath}")

    try:
        if platform.system() == "Windows":
            os.startfile(os.path.abspath(output_filepath))
        elif platform.system() == "Darwin":
            subprocess.run(['afplay', output_filepath], check=True)
        elif platform.system() == "Linux":
            subprocess.run(['mpg123', output_filepath], check=True)
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")


#text_to_speech_with_elevenlabs(
    #input_text,
    #output_filepath="elevenlabs_testing_autoplay.mp3"
#)
