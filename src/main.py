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
    data_dir = os.path.join(base_dir, "data")
    
    # 1. Discover available audio files
    valid_extensions = ('.mp3', '.m4a', '.wav', '.mp4')
    available_files = []
    
    if os.path.exists(data_dir):
        for f in os.listdir(data_dir):
            # Ignore hidden files and check extension
            if not f.startswith('.') and f.lower().endswith(valid_extensions):
                available_files.append(f)
                
    if not available_files:
        print(f"\n[Error] No audio files found in {data_dir}")
        print("Please place your audio/video files in the data/ folder and try again.")
        sys.exit(1)
        
    # 2. Present options to the user
    print("\nAvailable Files in data/:")
    for idx, f in enumerate(available_files):
        print(f"  [{idx + 1}] {f}")
        
    # 3. Get user input
    selected_idx = -1
    while selected_idx < 0 or selected_idx >= len(available_files):
        choice = input(f"\nEnter the number of the file you want to process (1-{len(available_files)}): ")
        try:
            selected_idx = int(choice) - 1
            if selected_idx < 0 or selected_idx >= len(available_files):
                print("Number out of range.")
        except ValueError:
            print("Invalid input. Please enter a number.")
            
    selected_file = available_files[selected_idx]
    
    # 4. Set dynamic paths
    input_audio = os.path.join(data_dir, selected_file)
    temp_wav = os.path.join(data_dir, "temp_16khz.wav")
    
    # Name the output file automatically based on the input file
    base_name = os.path.splitext(selected_file)[0]
    final_report = os.path.join(base_dir, "output", f"meeting_minutes_{base_name}.md")
    
    print(f"\n>>> Selected: {selected_file}")
    
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
