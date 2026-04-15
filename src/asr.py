import warnings
from groq import Groq
import os

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

def get_speaker_for_segment(target_start: float, target_end: float, diarized_segments: list) -> str:
    """Finds the speaker from diarized_segments that has the largest overlap with the Whisper text segment."""
    best_speaker = "Unknown Speaker"
    max_overlap = 0.0
    
    for (spk_start, spk_end, speaker_label) in diarized_segments:
        # Calculate time overlap
        overlap_start = max(target_start, spk_start)
        overlap_end = min(target_end, spk_end)
        overlap = overlap_end - overlap_start
        
        if overlap > max_overlap:
            max_overlap = overlap
            best_speaker = speaker_label
            
    return best_speaker

def transcribe_segments(wav_file_path: str, diarized_segments: list) -> list:
    """
    Uses Groq's Whisper Large-v3 API to transcribe the audio.
    Then merges Whisper's text with Pyannote's speaker labels.
    """
    print(f"[ASR] Routing audio to Groq Whisper 'large-v3' endpoint... (lightning fast)")
    
    client = Groq(api_key=GROQ_API_KEY)
    
    print(f"[ASR] Uploading and transcribing '{wav_file_path}'...")
    
    # Send the audio file to Groq
    with open(wav_file_path, "rb") as file:
        result = client.audio.transcriptions.create(
            file=(os.path.basename(wav_file_path), file.read()),
            model="whisper-large-v3",
            response_format="verbose_json"
        )
    
    transcriptions = []
    
    # Handle Groq's API return type (Pydantic objects or dicts)
    segments = result.segments if hasattr(result, 'segments') else result.get('segments', [])
    
    for segment in segments:
        if isinstance(segment, dict):
            start = segment["start"]
            end = segment["end"]
            text = segment["text"].strip()
        else:
            start = segment.start
            end = segment.end
            text = segment.text.strip()
            
        # Merge Whisper's text timestamp with Pyannote's speaker timestamp
        speaker = get_speaker_for_segment(start, end, diarized_segments)
        
        transcriptions.append({
            "start": start,
            "end": end,
            "speaker": speaker,
            "text": text
        })
        
    print(f"[ASR] Transcription complete. Merged Whisper and Pyannote data for {len(transcriptions)} text segments.")
    return transcriptions
