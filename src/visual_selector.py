# src/visual_selector.py
from PIL import Image, ImageDraw
import os
import random
from sentence_transformers import SentenceTransformer, util

# Load model for keyword matching (offline)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Assume local icons in assets/icons/
ICON_DIR = '/home/abhiram/PycharmProjects/PythonProject/assets/icons'
icons = [f for f in os.listdir(ICON_DIR) if f.endswith('.webp')]

def select_or_generate_visual(title, index, outdir):
    """
    Select local icon based on title keywords or generate simple image.
    """
    # Extract keywords (simple split)
    keywords = title.lower().split()

    # Embed title
    title_emb = model.encode(title)

    best_score = 0
    best_icon = None
    for icon in icons:
        icon_name = icon.replace('.webp', '').lower()
        icon_emb = model.encode(icon_name)
        score = util.cos_sim(title_emb, icon_emb)[0][0]
        if score > best_score:
            best_score = score
            best_icon = icon

    if best_score > 0.5 and best_icon:  # Threshold for match
        return os.path.join(ICON_DIR, best_icon)
    else:
        # Generate simple placeholder
        img = Image.new('RGB', (400, 300), color=(random.randint(0,255), random.randint(0,255), random.randint(0,255)))
        draw = ImageDraw.Draw(img)
        draw.text((10, 10), "Placeholder for: " + title[:20], fill=(0,0,0))
        visual_path = os.path.join(outdir, 'temp', f'visual_{index}.png')
        img.save(visual_path)
        return visual_path