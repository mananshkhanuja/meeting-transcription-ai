import os
from groq import Groq

# Using the secure Groq key from .env
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

def create_markdown_transcript(transcriptions: list) -> str:
    """Formats the raw dictionary transcriptions into a readable string format."""
    transcript_text = ""
    for item in transcriptions:
        start_time = f"{item['start']:.1f}s"
        speaker = item['speaker']
        text = item['text']
        transcript_text += f"**{speaker}** ({start_time}): {text}\n\n"
    return transcript_text.strip()

def generate_report(transcriptions: list, output_path: str) -> str:
    """
    Takes the final transcribed/diarized text, creates a clean Markdown transcript,
    and uses the Groq Llama-3 API to generate an intelligent Executive Summary and Action Items.
    """
    print(f"[Output Formatter] Formatting transcript and pinging Groq Llama-3 for intelligent summarization...")
    
    # 1. Format raw transcript text
    transcript_text = create_markdown_transcript(transcriptions)
    
    # 2. Call LLM for Summarization
    if not transcript_text:
        llm_summary = "No speech detected in the audio file."
    else:
        try:
            client = Groq(api_key=GROQ_API_KEY)
            
            prompt = f"""
You are an expert AI meeting assistant. Below is an exact transcript of a meeting with timestamps.
Please analyze the conversation and generate:
1. An Executive Summary (3-4 sentences)
2. Key Decisions Made (bullet points)
3. Action Items (bullet points, specifically inferring who is assigned what based on the text if possible)

Here is the transcript:
{transcript_text}
"""
            
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a helpful and precise executive assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1024,
                top_p=1,
            )
            
            llm_summary = completion.choices[0].message.content.strip()
        except Exception as e:
            print(f"[Output Formatter Warning] Groq API Failed: {e}")
            llm_summary = f"> *Groq LLM summarization failed: {e}*"
            
    # 3. Build Markdown Report
    final_report = f"""# Automated Meeting Minutes

## Executive Summary & Action Items
{llm_summary}

---

## Complete Transcript
{transcript_text}
"""
    
    # 4. Save to Disk
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_report)
        
    print(f"[Output Formatter] Success! Intelligent meeting report saved to '{output_path}'.")
    return output_path
