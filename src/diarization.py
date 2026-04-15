import warnings

import os

# Using the secure Hugging Face token from .env
HF_TOKEN = os.environ.get("HF_TOKEN")

def diarize_audio(wav_file_path: str, speech_segments: list) -> list:
    """
    Uses pyannote.audio to identify *who* is speaking and *when*.
    Returns a list of tuples: (start_sec, end_sec, Speaker_ID)
    """
    print(f"[Diarization] Loading Pyannote model from Hugging Face... (this may take a moment)")
    
    # Suppress warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        
        # Nuclear fix for PyTorch 2.8+ weights_only=True default
        import torch
        _original_torch_load = torch.load
        def _patched_load(*args, **kwargs):
            # Forcefully overwrite it, so even if hugginface_hub passes weights_only=True, we ignore it.
            kwargs['weights_only'] = False 
            return _original_torch_load(*args, **kwargs)
        torch.load = _patched_load
        
        from pyannote.audio import Pipeline
        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            use_auth_token=HF_TOKEN
        )
        print(f"[Diarization] Analyzing speakers in '{wav_file_path}'...")
        diarization = pipeline(wav_file_path)
        
        diarized_segments = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            diarized_segments.append((turn.start, turn.end, speaker))
            
    print(f"[Diarization] Completed! Identified {len(diarized_segments)} speaker segments.")
    return diarized_segments
