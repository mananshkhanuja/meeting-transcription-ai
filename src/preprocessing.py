import os
import subprocess
import shutil
import glob

def find_ffmpeg() -> str:
    # Check if it's already in the PATH
    if shutil.which("ffmpeg"):
        return "ffmpeg"
        
    # If not in PATH (happens when the user just installed it without restarting terminal)
    # Winget installs FFmpeg here typically:
    winget_path = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg.Essentials*\*\bin\ffmpeg.exe")
    matches = glob.glob(winget_path)
    if matches:
        return matches[0]
        
    # Another common location just in case
    winget_path_alt = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WindowsApps\ffmpeg.exe")
    if os.path.exists(winget_path_alt):
        return winget_path_alt
        
    raise FileNotFoundError("FFmpeg executable not found. Please install FFmpeg and ensure it's in your PATH.")

def convert_audio_to_wav(input_path: str, output_path: str) -> str:
    """
    Converts and standardizes an audio file to a clean 16kHz Mono WAV file.
    Uses FFmpeg directly via subprocess, avoiding PATH restart issues.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input audio file not found: {input_path}")
        
    ffmpeg_exe = find_ffmpeg()
    
    print(f"[Pre-processing] Loading audio from '{input_path}'...")
    print(f"[Pre-processing] Standardizing to 16kHz Mono WAV using '{ffmpeg_exe}'...")
    
    command = [
        ffmpeg_exe,
        "-y", 
        "-i", input_path,
        "-ac", "1",
        "-ar", "16000",
        "-loglevel", "error",
        output_path
    ]
    
    try:
        subprocess.run(command, check=True)
        print(f"[Pre-processing] Saved standardized audio to '{output_path}'.")
    except subprocess.CalledProcessError as e:
        print(f"[Pre-processing Error] FFmpeg failed.")
        raise e
        
    return output_path
