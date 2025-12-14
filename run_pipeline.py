# run_pipeline.py
import argparse
import os
from src.pdf_extractor import extract_key_sections
from src.summarizer import summarize_sections
from src.visual_selector import select_or_generate_visual
from src.slide_assembler import assemble_slides
from src.video_generator import generate_video

def main():
    parser = argparse.ArgumentParser(description="PDF to Slides & Video Pipeline")
    parser.add_argument('--input', required=True, help='Input PDF file')
    parser.add_argument('--outdir', default='output/', help='Output directory')
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    os.makedirs(os.path.join(args.outdir, 'temp'), exist_ok=True)

    # Step 1: Extract
    sections = extract_key_sections(args.input)

    # Step 2: Summarize
    slides_data = summarize_sections(sections)

    # Step 3: Visuals
    for i, slide in enumerate(slides_data):
        visual_path = select_or_generate_visual(slide['title'], i, args.outdir)
        slide['visual_path'] = visual_path

    # Step 4: Assemble slides
    slides_path = os.path.join(args.outdir, 'slides.pptx')
    assemble_slides(slides_data, slides_path)

    # Step 5: Generate video
    video_path = os.path.join(args.outdir, 'video.mp4')
    generate_video(slides_path, slides_data, video_path, args.outdir)

    print(f"Generated {slides_path} and {video_path}")

if __name__ == '__main__':
    main()