
# if you dont use pipenv uncomment the following:
from dotenv import load_dotenv
load_dotenv()

# VoiceBot UI with Gradio
import os
import gradio as gr

from brain import encode_image, analyze_image_with_query
from voice_of_patient import record_audio, transcribe_with_groq
from voice_of_doc import text_to_speech_with_gtts, text_to_speech_with_elevenlabs

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

system_prompt = """You have to act as a professional doctor, I know you are not but this is for learning purpose.
What's in this image? Do you find anything wrong with it medically?
If you make a differential, suggest some remedies for them.
Do not add any numbers or special characters in your response.
Your response should be in one long paragraph.
Keep your answer concise, maximum two sentences.
No preamble, start your answer right away."""


def process_inputs(audio_filepath, image_filepath):
    # Validate audio input
    if not audio_filepath:
        return "Please record or upload your voice first.", "", None

    if not GROQ_API_KEY:
        return "GROQ_API_KEY is missing from your .env file.", "", None

    # Step 1: Convert patient speech to text
    speech_to_text_output = transcribe_with_groq(
        GROQ_API_KEY=GROQ_API_KEY,
        audio_filepath=audio_filepath,
        stt_model="whisper-large-v3"
    )

    # Step 2: Analyze the image
    if image_filepath:
        doctor_response = analyze_image_with_query(
            query=system_prompt + "\nPatient symptoms: " + speech_to_text_output,
            encoded_image=encode_image(image_filepath),
            model="qwen/qwen3.8-27b"
        )
    else:
        doctor_response = (
            "Please upload an image so I can provide an image-based response. "
            "The transcribed symptoms are: " + speech_to_text_output
        )

    # Step 3: Generate doctor's voice
    output_filepath = "final.mp3"

    text_to_speech_with_elevenlabs(
        input_text=doctor_response,
        output_filepath=output_filepath
    )

    # Return the actual audio file path to Gradio
    return speech_to_text_output, doctor_response, output_filepath


# Create the interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(
            sources=["microphone", "upload"],
            type="filepath",
            label="Patient Voice"
        ),
        gr.Image(
            type="filepath",
            label="Upload Patient Image"
        )
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio(label="Doctor's Voice", type="filepath")
    ],
    title="AI Doctor with Vision and Voice"
)

iface.launch(debug=True)
