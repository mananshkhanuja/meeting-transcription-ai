import os
import sys
import glob

# Dynamically add FFmpeg to PATH so OpenAI Whisper can find it
winget_ffmpeg_dir = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg.Essentials*\*\bin")
matches = glob.glob(winget_ffmpeg_dir)
if matches:
    os.environ["PATH"] += os.pathsep + matches[0]

# Add src to python path so we can import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load API keys from secure .env file
try:
    from dotenv import load_dotenv
    dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    load_dotenv(dotenv_path)
except ImportError:
    pass

from preprocessing import convert_audio_to_wav
from vad import detect_speech
from diarization import diarize_audio
from asr import transcribe_segments
from output_formatter import generate_report

def main():
    print("=== Automated Meeting Transcription System ===")
    
    # Define paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_audio = os.path.join(base_dir, "data", "Recording.mp3")
    temp_wav = os.path.join(base_dir, "data", "temp_16khz.wav")
    final_report = os.path.join(base_dir, "output", "meeting_minutes.md")
    
    # Just skipping input checking for the dummy version, but in reality 
    # we would check if input_audio exists.
    
    print("\n--- Step 1: Pre-processing ---")
    clean_audio_path = convert_audio_to_wav(input_audio, temp_wav)
    
    print("\n--- Step 2: Voice Activity Detection ---")
    speech_segments = detect_speech(clean_audio_path)
    
    print("\n--- Step 3: Speaker Diarization ---")
    diarized_segments = diarize_audio(clean_audio_path, speech_segments)
    
    print("\n--- Step 4: ASR Transcription ---")
    final_transcription = transcribe_segments(clean_audio_path, diarized_segments)
    
    print("\n--- Step 5: Report Generation ---")
    generate_report(final_transcription, final_report)
    
    print("\n=== System Pipeline Executed Successfully ===")

if __name__ == "__main__":
    main()
