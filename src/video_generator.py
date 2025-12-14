
from moviepy import ImageClip, concatenate_videoclips, AudioFileClip, vfx
import pyttsx3
import os
from PIL import Image, ImageDraw, ImageFont

def generate_video(slides_path, slides_data, output_path, outdir):
    """
    Generate animated explainer video from slides_data.
    Uses Pillow for slide images, MoviePy v2+ effects for fades/zoom.
    """
    temp_dir = os.path.join(outdir, 'temp')
    os.makedirs(temp_dir, exist_ok=True)

    slide_images = []
    audio_files = []
    engine = pyttsx3.init()
    duration_per_slide = 10  # seconds (total 30-90s for 6-12 slides)

    # Resolution
    width, height = 1280, 720
    bg_color = (240, 248, 255)  # Light blue

    for i, slide_data in enumerate(slides_data):
        # Recreate slide image
        img = Image.new('RGB', (width, height), color=bg_color)
        draw = ImageDraw.Draw(img)

        # Fonts
        try:
            title_font = ImageFont.truetype("arial.ttf", 50)
            bullet_font = ImageFont.truetype("arial.ttf", 40)
        except IOError:
            title_font = ImageFont.load_default()
            bullet_font = ImageFont.load_default()

        # Title centered
        title = slide_data['title']
        title_bbox = draw.textbbox((0, 0), title, font=title_font)
        title_w = title_bbox[2] - title_bbox[0]
        draw.text(((width - title_w) / 2, 80), title, fill=(0, 51, 102), font=title_font)

        # Bullets left
        y_offset = 220
        for bullet in slide_data['bullets'][:2]:
            draw.text((100, y_offset), f"• {bullet}", fill=(0, 0, 0), font=bullet_font)
            y_offset += 80

        # Visual right
        visual_path = slide_data.get('visual_path')
        if visual_path and os.path.exists(visual_path):
            try:
                visual = Image.open(visual_path).convert('RGB').resize((450, 350), Image.LANCZOS)
                img.paste(visual, (width - 550, 180))
            except Exception as e:
                print(f"Visual load failed: {e}")

        # Save image
        img_path = os.path.join(temp_dir, f'slide_{i}.png')
        img.save(img_path)
        slide_images.append(img_path)

        # TTS
        notes = slide_data.get('notes', 'Key information.')
        audio_path = os.path.join(temp_dir, f'audio_{i}.wav')
        engine.save_to_file(notes, audio_path)
        engine.runAndWait()
        audio_files.append(audio_path)

    # Build clips with v2 effects
    clips = []
    for img_path, audio_path in zip(slide_images, audio_files):
        clip = ImageClip(img_path).with_duration(duration_per_slide)

        # Fades + Ken Burns zoom-in
        clip = clip.with_effects([
            vfx.FadeIn(1),
            vfx.FadeOut(1),
            vfx.Resize(lambda t: 1 + 0.03 * (t / duration_per_slide))  # Zoom from 1x to 1.3x
        ])

        # Narration
        if os.path.exists(audio_path):
            narration = AudioFileClip(audio_path)
            clip = clip.with_audio(narration)

        clips.append(clip)

    # Concatenate
    final_video = concatenate_videoclips(clips, method="compose")

    # Background music
    music_path = 'assets/music/background.mp3'
    if os.path.exists(music_path):
        music = AudioFileClip(music_path).volumex(0.15).audio_loop(duration=final_video.duration)
        if final_video.audio:
            final_audio = final_video.audio.volumex(0.9).audio_overlay(music)
        else:
            final_audio = music
        final_video = final_video.with_audio(final_audio)

    # Export
    final_video.write_videofile(output_path, fps=24, codec='libx264', audio_codec='aac', threads=4)

