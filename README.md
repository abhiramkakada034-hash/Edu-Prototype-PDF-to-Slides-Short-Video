# Setup and Dependencies

1. Clone the repositorytextgit clone https://github.com/yourusername/infooware-edu-prototype.git
2. cd infooware-edu-prototype
3. Create a virtual environment (recommended) : python -m venv venv
4. source venv/bin/activate  # On Windows: venv\Scripts\activate
5. Install dependenciestextpip install -r requirements.txt
   	Required libraries:
   
					pdfplumber
					langchain, langchain-groq
					python-pptx
					pillow
					sentence-transformers
					pyttsx3
					moviepy

6. Set up Groq API key (for LLM summarization): texport GROQ_API_KEY=your_groq_api_key_here(Add to your environment permanently or use a .env file if preferred.)
Prepare assets.

7. Create folder assets/icons/ and add royalty-free PNG icons (descriptive filenames improve matching).
   
9. Create folder assets/music/ and add a royalty-free background music loop (e.g., background.mp3).

	Add a sample PDF.Place your input PDF (e.g., sample.pdf) in the repo root or specify its path.


# How to Run
	python run_pipeline.py --input sample.pdf --outdir output/
This will generate:

output/slides.pptx — 6–12 slides with title, 1–2 bullets, and a visual per slide.

output/video.mp4 — 30–90 second animated video with transitions, Ken Burns zoom, TTS narration, and background music.

# Example Run
The repository includes a sample PDF and pre-generated outputs (slides.pptx and video.mp4) from running the pipeline on it.

Notes:
Summarization uses Groq's fast LLM via LangChain (optional but recommended for best quality).

Visuals are selected semantically from local icons or generated as placeholders.

Video uses offline TTS (pyttsx3); ensure your system has speech support.

