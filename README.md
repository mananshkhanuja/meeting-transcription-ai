# Automated Meeting Transcription System

This is the project repository for Group 85. 
This codebase converts raw multi-speaker audio into structured meeting minutes.

## Structure

*   `src/`: Contains the pipeline modules.
*   `data/`: Put your raw audio files here (e.g., `sample_meeting.mp4`).
*   `output/`: Generated meeting minutes and transcripts appear here.

## How to Test the Skeleton Code

Right now, the pipeline is a "skeleton". It proves the logic works but uses dummy data instead of heavy AI models. 

1. Open your terminal.
2. Navigate into `SaS Project\meeting_transcription`.
3. Run the main script:
   ```bash
   python src/main.py
   ```
4. Look in the `output/` folder and you will find `meeting_minutes.md` containing the simulated transcript!

## Next Steps for the Team
- **Manansh:** Start integrating `pydub` (or similar) into `preprocessing.py` to actually convert real `.mp4` files.
- **Kumar:** Start plugging `pyannote.audio` code into `diarization.py`.
- **Ansh:** Start plugging OpenAI Whisper into `asr.py`.
- **Bhavjot:** Play around with extracting text via an LLM (OpenAI API or similar) inside `output_formatter.py`.
