# Demo Document: Infooware Edu Prototype Pipeline
## Overview
This prototype is a fully automated Python pipeline that takes a single-chapter PDF as input and generates two outputs:

1.nA visually engaging PowerPoint slide deck (6–12 slides).
2. A short animated explainer video (30–90 seconds) with narration, transitions, and background music.

The entire process runs locally (after initial setup) with no web downloads during execution.
# How the Pipeline Works (Step-by-Step)

1.PDF Text Extraction
  
    Uses pdfplumber to extract headings and paragraphs from the input PDF.
      
    Identifies the top 6–10 key sections using Groq LLM (via LangChain) for intelligent ranking.

2.Content Summarization

      For each key section, the Groq LLM generates:
      
      A concise slide title (6–20 words).
      
      1–2 short supporting bullets.
      
      One speaker note sentence for narration.
  

3.Visual Selection & Generation
   
    Semantically matches the slide title to local royalty-free icons in assets/icons/ using sentence-transformers embeddings.
  
    If no strong match is found, generates a simple placeholder image using Pillow.

4.Slide Assembly

    Builds a consistent PowerPoint file (slides.pptx) using python-pptx.
    
    Layout: centered title, left-aligned bullets, right-side visual, light themed background.

5.Video Generation
   
    Recreates each slide as a high-quality image using Pillow (for reliable rendering).
    
    Applies fade transitions and a subtle Ken Burns zoom effect with MoviePy v2+.
  
    Adds offline TTS narration (pyttsx3) from speaker notes.
    
    Overlays low-volume royalty-free background music.
    
    Exports as video.mp4.


# One-sentence architecture:
    PDF → Text Extraction → LLM Summarization → Visual Matching → Slide Creation → Video Assembly with TTS & Effects
    
# How to Run It Locally

1.Clone the repository and navigate to the project folder.

2.Create and activate a virtual environment (recommended).

3.Install dependencies: pip install -r requirements.txt

4.set your Groq API key: export GROQ_API_KEY=your_key_here

5.Prepare assets:

  Place royalty-free icons in assets/icons/ (better filenames = better matching).
  
  Place a background music loop in assets/music/background.mp3.

7.     Run the pipeline:python run_pipeline.py --input sample.pdf --outdir output/
8.Outputs will be generated in the output/ folder: slides.pptx, video.mp4


