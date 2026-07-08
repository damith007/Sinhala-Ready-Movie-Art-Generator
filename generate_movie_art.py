#!/usr/bin/env python3
"""
Movie Art Generator — Python script called from WordPress PHP
Handles proper Sinhala text shaping via PIL + libraqm (HarfBuzz)

Usage (from PHP):
    python3 /path/to/generate_movie_art.py \
        --poster   "/tmp/poster.jpg" \
        --backdrop "/tmp/backdrop.jpg" \
        --author   "ලේඛකයාගේ නම" \
        --rating   "8.4" \
        --watermark "THURUWA SUBZ.LK" \
        --logo     "/path/to/logo.png" \
        --output   "/wp-content/uploads/2024/01/movie_art_123.jpg" \
        --font     "/path/to/SinhalaLatin-Merged.ttf"
"""

import sys, os, argparse
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--poster',    required=True)
    p.add_argument('--backdrop',  required=True)
    p.add_argument('--author',    default='Unknown')
    p.add_argument('--rating',    default='N/A')
    p.add_argument('--watermark', default='SUBZ.LK')
    p.add_argument('--logo',      default='')
    p.add_argument('--output',    required=True)
    p.add_argument('--font',      required=True)
    return p.parse_args()

def load_font(font_path, size):
    try:
        return ImageFont.truetype(font_path, size)
    except:
        return ImageFont.load_default()

def draw_text_si(draw, pos, text, font, fill, language='si'):
    """Draw text with proper Sinhala shaping (requires libraqm)."""
    try:
        draw.text(pos, text, font=font, fill=fill, language=language)
    except TypeError:
        # Older PIL without language param
        draw.text(pos, text, font=font, fill=fill)

def generate(args):
    # ── Load Images ───────────────────────────────────────────────────────────
    backdrop = Image.open(args.backdrop).convert('RGB')
    poster   = Image.open(args.poster).convert('RGB')

    bw, bh = backdrop.size

    canvas = backdrop.copy()
    draw   = ImageDraw.Draw(canvas)

    # ── Poster (left side, 65% height) ───────────────────────────────────────
    ph     = int(bh * 0.65)
    ratio  = poster.width / poster.height
    pw     = int(ph * ratio)
    poster = poster.resize((pw, ph), Image.LANCZOS)

    px = 50
    py = (bh - ph) // 2

    # White border
    border = 3
    draw.rectangle([px - border, py - border, px + pw + border, py + ph + border],
                   outline=(220, 220, 220), width=border)
    canvas.paste(poster, (px, py))

    # ── Footer Bar ────────────────────────────────────────────────────────────
    footer_h = 88
    wm_h     = 26
    footer_y = bh - footer_h - wm_h

    footer_overlay = Image.new('RGBA', (bw, footer_h), (0, 0, 0, 180))
    canvas.paste(Image.new('RGB', (bw, footer_h), (0,0,0)),
                 (0, footer_y),
                 footer_overlay)

    draw = ImageDraw.Draw(canvas)

    # ── Fonts ─────────────────────────────────────────────────────────────────
    f_bold   = load_font(args.font, 18)
    f_medium = load_font(args.font, 14)
    f_small  = load_font(args.font, 10)
    f_wm     = load_font(args.font, 9)

    white  = (255, 255, 255)
    gray   = (160, 160, 160)
    accent = (100, 180, 255)

    # ── Rating (bottom-left) ──────────────────────────────────────────────────
    rating_text = f"OMDB RATING: {args.rating}/10"
    sub_text    = "A vertical poster from OMDB"

    draw_text_si(draw, (px, footer_y + 20), rating_text, f_bold,   white, language='en')
    draw_text_si(draw, (px, footer_y + 48), sub_text,    f_small,  gray,  language='en')

    # ── Author (bottom-right) — සිංහල හෝ English ──────────────────────────────
    author_text = f"AUTHOR: {args.author.upper()}"
    bbox  = draw.textbbox((0, 0), author_text, font=f_bold)
    tw    = bbox[2] - bbox[0]

    logo_space = 80 if args.logo and os.path.exists(args.logo) else 20
    ax = bw - tw - logo_space
    draw_text_si(draw, (ax, footer_y + 34), author_text, f_bold, white, language='si')

    # ── Logo ──────────────────────────────────────────────────────────────────
    if args.logo and os.path.exists(args.logo):
        logo = Image.open(args.logo).convert('RGBA')
        max_h = 55
        scale = max_h / logo.height
        logo  = logo.resize((int(logo.width * scale), max_h), Image.LANCZOS)
        lx    = bw - logo.width - 15
        ly    = footer_y + (footer_h - max_h) // 2
        canvas.paste(logo, (lx, ly), logo)

    # ── Watermark Strip ───────────────────────────────────────────────────────
    wm_y = bh - wm_h
    wm_strip = Image.new('RGB', (bw, wm_h), (8, 8, 8))
    canvas.paste(wm_strip, (0, wm_y))

    draw   = ImageDraw.Draw(canvas)
    wm_col = (75, 75, 75)
    wm_x   = 10
    wm_text = args.watermark
    while wm_x < bw:
        draw_text_si(draw, (wm_x, wm_y + 7), wm_text, f_wm, wm_col, language='si')
        wm_x += 185

    # ── Save ──────────────────────────────────────────────────────────────────
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    canvas.save(args.output, 'JPEG', quality=95)
    print(args.output)   # PHP reads this stdout
    return 0

if __name__ == '__main__':
    sys.exit(generate(parse_args()))
