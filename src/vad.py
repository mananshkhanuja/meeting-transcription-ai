import torch
import warnings

def detect_speech(wav_file_path: str) -> list:
    """
    Uses Silero VAD (Voice Activity Detection) via PyTorch Hub to drop silence.
    Returns a list of tuples representing active speech segments (start_sec, end_sec).
    """
    print(f"[VAD] Loading Silero-VAD model via PyTorch Hub...")
    
    # Suppress warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        # Load the pre-trained Silero VAD model 
        model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                                      model='silero_vad',
                                      force_reload=False,
                                      trust_repo=True)
                                      
        (get_speech_timestamps, save_audio, read_audio, VADIterator, collect_chunks) = utils
         
        print(f"[VAD] Reading audio '{wav_file_path}'...")
        wav = read_audio(wav_file_path, sampling_rate=16000)
        
        print("[VAD] Detecting active speech regions...")
        speech_timestamps = get_speech_timestamps(wav, model, sampling_rate=16000)
        
        segments = []
        for ts in speech_timestamps:
            start_sec = ts['start'] / 16000.0
            end_sec = ts['end'] / 16000.0
            segments.append((start_sec, end_sec))
            
    print(f"[VAD] Found {len(segments)} active speech segments (silence removed).")
    return segments
