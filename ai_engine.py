import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_text(text: str) -> str:
    """
    Summarizes the given text into a 2-minute podcast script using GPT-4o.
    """
    prompt = (
        "You are an expert podcast host. Your task is to summarize the following research paper "
        "into a compelling, easy-to-understand 2-minute podcast script. "
        "Focus on the key findings, the problem being solved, and the implications. "
        "Keep the tone engaging and accessible to a general tech-savvy audience. "
        "Do not include sound effects or music cues, just the spoken script.\n\n"
        f"Input Text:\n{text[:20000]}" # Truncate to avoid context limit issues for MVP
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

def generate_audio(script: str, output_path: str):
    """
    Converts the script to audio using OpenAI's TTS API.
    """
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=script
    )
    
    response.stream_to_file(output_path)
