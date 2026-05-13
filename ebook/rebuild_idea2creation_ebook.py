from __future__ import annotations

import html
import math
import os
import re
import subprocess
from pathlib import Path
from typing import List, Dict, Any

import cairo

ROOT = Path('/data/.openclaw/workspace/Idea2Creation')
RECOVERY = ROOT / '_ebook_recovery'
EBOOK_DIR = ROOT / 'ebook'
ASSET_DIR = EBOOK_DIR / 'assets' / 'generated'
HTML_OUT = EBOOK_DIR / 'idea2creation-final-ebook.html'
PDF_OUT = ROOT / 'Idea2Creation.pdf'

CHAPTER_FILES = [RECOVERY / f'ebook_chapter{i}.md' for i in range(1, 10)]
APPENDIX_FILE = RECOVERY / 'ebook_appendices.md'

PALETTES = [
    ((19/255, 30/255, 54/255), (57/255, 87/255, 167/255), (98/255, 181/255, 229/255), (234/255, 173/255, 66/255)),
    ((29/255, 16/255, 60/255), (111/255, 66/255, 193/255), (191/255, 134/255, 255/255), (79/255, 229/255, 174/255)),
    ((18/255, 44/255, 48/255), (31/255, 113/255, 133/255), (98/255, 206/255, 203/255), (255/255, 192/255, 103/255)),
    ((51/255, 24/255, 24/255), (163/255, 75/255, 75/255), (237/255, 127/255, 96/255), (255/255, 217/255, 102/255)),
]


def slugify(text: str) -> str:
    slug = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
    return slug or 'section'


def clean_text(text: str) -> str:
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    text = re.sub(r'<[^>]+>', '', text)
    return re.sub(r'\s+', ' ', text).strip()


def format_inline(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)
    return text


def md_to_blocks(text: str, chapter_num: int | None = None) -> List[Dict[str, Any]]:
    blocks: List[Dict[str, Any]] = []
    lines = text.splitlines()
    i = 0
    current_chapter = chapter_num
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if not stripped:
            i += 1
            continue
        if stripped.startswith('```'):
            fence_lang = stripped[3:].strip()
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1
            blocks.append({'type': 'code', 'lang': fence_lang, 'text': '\n'.join(code_lines), 'chapter': current_chapter})
            continue
        m = re.match(r'^(#{1,3})\s+(.+)$', stripped)
        if m:
            level = len(m.group(1))
            title = clean_text(m.group(2))
            chap_match = re.match(r'^Chapter\s+(\d+):', title, re.I)
            if chap_match:
                current_chapter = int(chap_match.group(1))
            blocks.append({'type': 'heading', 'level': level, 'text': title, 'chapter': current_chapter, 'id': slugify(title)})
            i += 1
            continue
        if stripped in {'---', '***'}:
            blocks.append({'type': 'hr', 'chapter': current_chapter})
            i += 1
            continue
        if stripped.startswith('>'):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                quote_lines.append(lines[i].strip()[1:].strip())
                i += 1
            blocks.append({'type': 'blockquote', 'text': ' '.join(quote_lines), 'chapter': current_chapter})
            continue
        if re.match(r'^\s*[-*+]\s+', line):
            items = []
            while i < len(lines) and re.match(r'^\s*[-*+]\s+', lines[i]):
                items.append(re.sub(r'^\s*[-*+]\s+', '', lines[i].rstrip()))
                i += 1
            blocks.append({'type': 'ul', 'items': items, 'chapter': current_chapter})
            continue
        if re.match(r'^\s*\d+\.\s+', line):
            items = []
            while i < len(lines) and re.match(r'^\s*\d+\.\s+', lines[i]):
                items.append(re.sub(r'^\s*\d+\.\s+', '', lines[i].rstrip()))
                i += 1
            blocks.append({'type': 'ol', 'items': items, 'chapter': current_chapter})
            continue
        para_lines = [stripped]
        i += 1
        while i < len(lines):
            nxt = lines[i].strip()
            if not nxt:
                i += 1
                break
            if nxt.startswith('```') or nxt.startswith('>') or nxt in {'---', '***'}:
                break
            if re.match(r'^(#{1,3})\s+(.+)$', nxt) or re.match(r'^\s*[-*+]\s+', lines[i]) or re.match(r'^\s*\d+\.\s+', lines[i]):
                break
            para_lines.append(nxt)
            i += 1
        blocks.append({'type': 'paragraph', 'text': ' '.join(para_lines), 'chapter': current_chapter})
    return blocks


def load_blocks() -> List[Dict[str, Any]]:
    blocks: List[Dict[str, Any]] = []
    for idx, path in enumerate(CHAPTER_FILES, start=1):
        blocks.extend(md_to_blocks(path.read_text(), idx))
    if APPENDIX_FILE.exists():
        appendix_blocks = md_to_blocks(APPENDIX_FILE.read_text(), 10)
        for block in appendix_blocks:
            if block['type'] == 'heading' and block['level'] == 1 and not block['text'].lower().startswith('chapter'):
                block['text'] = 'Appendices'
                block['id'] = 'appendices'
                block['chapter'] = 10
                break
        blocks.extend(appendix_blocks)
    return blocks


def summarize_after(blocks: List[Dict[str, Any]], idx: int) -> str:
    for j in range(idx + 1, min(len(blocks), idx + 10)):
        if blocks[j]['type'] == 'paragraph':
            txt = clean_text(blocks[j]['text'])
            parts = re.split(r'(?<=[.!?])\s+', txt)
            candidate = parts[0].strip()
            if len(candidate) < 60 and len(parts) > 1:
                candidate = (candidate + ' ' + parts[1]).strip()
            return candidate[:170]
    return 'A practical visual snapshot from the Idea2Creation operating system.'


def choose_visual_slots(blocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    heading_indices_by_chapter: Dict[int, List[int]] = {}
    chapter_titles: Dict[int, int] = {}
    for i, block in enumerate(blocks):
        if block['type'] != 'heading':
            continue
        chap = block.get('chapter') or 0
        heading_indices_by_chapter.setdefault(chap, []).append(i)
        if block['level'] == 1 and chap not in chapter_titles:
            chapter_titles[chap] = i
    selected: List[int] = []
    for chap in range(1, 10):
        indices = [i for i in heading_indices_by_chapter.get(chap, []) if blocks[i]['level'] in (2, 3)]
        if chap in chapter_titles:
            selected.append(chapter_titles[chap])
        if not indices:
            continue
        picks = {0, len(indices) // 3, (2 * len(indices)) // 3}
        for pos in sorted(picks):
            selected.append(indices[min(pos, len(indices) - 1)])
    appendix_indices = [i for i in heading_indices_by_chapter.get(10, []) if blocks[i]['level'] in (1, 2, 3)]
    if appendix_indices:
        selected.append(appendix_indices[0])
    seen = set()
    unique = []
    for idx in selected:
        if idx not in seen:
            unique.append(idx)
            seen.add(idx)
    slots = []
    for order, idx in enumerate(unique, start=1):
        block = blocks[idx]
        slots.append({
            'order': order,
            'block_index': idx,
            'chapter': block.get('chapter') or 0,
            'title': block['text'],
            'subtitle': summarize_after(blocks, idx),
        })
    return slots


def wrap_text(ctx: cairo.Context, text: str, max_width: float, font_size: float) -> List[str]:
    ctx.set_font_size(font_size)
    words = text.split()
    lines: List[str] = []
    current = ''
    for word in words:
        test = word if not current else current + ' ' + word
        if ctx.text_extents(test).width <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def rounded_rect(ctx: cairo.Context, x: float, y: float, w: float, h: float, r: float) -> None:
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    ctx.close_path()


def generate_visual(slot: Dict[str, Any], out_path: Path) -> None:
    width, height = 1600, 900
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)
    palette = PALETTES[(slot['order'] - 1) % len(PALETTES)]
    bg1, bg2, accent, gold = palette

    grad = cairo.LinearGradient(0, 0, width, height)
    grad.add_color_stop_rgb(0, *bg1)
    grad.add_color_stop_rgb(0.55, *bg2)
    grad.add_color_stop_rgb(1, bg1[0] * 0.9, bg1[1] * 0.9, bg1[2] * 1.1)
    ctx.rectangle(0, 0, width, height)
    ctx.set_source(grad)
    ctx.fill()

    glow = cairo.RadialGradient(width * 0.18, height * 0.2, 60, width * 0.18, height * 0.2, 520)
    glow.add_color_stop_rgba(0, 1, 1, 1, 0.18)
    glow.add_color_stop_rgba(1, 1, 1, 1, 0)
    ctx.set_source(glow)
    ctx.paint()

    ctx.set_line_width(1.2)
    ctx.set_source_rgba(1, 1, 1, 0.05)
    for x in range(0, width, 96):
        ctx.move_to(x, 0)
        ctx.line_to(x, height)
    for y in range(0, height, 96):
        ctx.move_to(0, y)
        ctx.line_to(width, y)
    ctx.stroke()

    for n in range(9):
        radius = 54 + n * 22
        ctx.arc(width * 0.83, height * 0.24, radius, 0, 2 * math.pi)
        ctx.set_source_rgba(accent[0], accent[1], accent[2], max(0.02, 0.12 - n * 0.01))
        ctx.set_line_width(2.5)
        ctx.stroke()

    # premium book/device composition on the right
    ctx.save()
    ctx.translate(1160, 235)
    ctx.rotate(-0.12)
    rounded_rect(ctx, -120, -130, 290, 390, 24)
    ctx.set_source_rgba(0, 0, 0, 0.22)
    ctx.fill()
    rounded_rect(ctx, -145, -155, 290, 390, 24)
    device = cairo.LinearGradient(-145, -155, 145, 235)
    device.add_color_stop_rgb(0, 0.97, 0.98, 1)
    device.add_color_stop_rgb(1, 0.86, 0.9, 0.98)
    ctx.set_source(device)
    ctx.fill_preserve()
    ctx.set_source_rgba(1, 1, 1, 0.4)
    ctx.set_line_width(2)
    ctx.stroke()
    rounded_rect(ctx, -118, -128, 236, 336, 18)
    screen = cairo.LinearGradient(-118, -128, 118, 208)
    screen.add_color_stop_rgb(0, bg1[0] * 1.1, bg1[1] * 1.05, bg1[2] * 1.2)
    screen.add_color_stop_rgb(1, accent[0] * 0.95, accent[1] * 0.95, accent[2] * 0.95)
    ctx.set_source(screen)
    ctx.fill()
    ctx.restore()

    # AI nodes on the device screen zone
    nodes = [(1110, 208), (1238, 178), (1368, 228), (1196, 330), (1340, 372)]
    ctx.set_source_rgba(1, 1, 1, 0.2)
    ctx.set_line_width(2)
    for a, b in zip(nodes, nodes[1:]):
        ctx.move_to(*a)
        ctx.line_to(*b)
    ctx.stroke()
    for x, y in nodes:
        ctx.arc(x, y, 11, 0, 2 * math.pi)
        ctx.set_source_rgb(*gold)
        ctx.fill_preserve()
        ctx.set_source_rgba(1, 1, 1, 0.75)
        ctx.set_line_width(3)
        ctx.stroke()

    # Growth rail along the bottom
    rail_y = 710
    points = [(170, rail_y), (410, rail_y - 84), (700, rail_y - 18), (985, rail_y - 102), (1290, rail_y - 38)]
    ctx.set_source_rgba(1, 1, 1, 0.18)
    ctx.set_line_width(6)
    for a, b in zip(points, points[1:]):
        ctx.move_to(*a)
        ctx.line_to(*b)
    ctx.stroke()
    for i, (px, py) in enumerate(points):
        ctx.arc(px, py, 18, 0, 2 * math.pi)
        ctx.set_source_rgb(*gold)
        ctx.fill_preserve()
        ctx.set_source_rgba(1, 1, 1, 0.82)
        ctx.set_line_width(4)
        ctx.stroke()
        ctx.select_font_face('Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(20)
        ctx.set_source_rgba(1, 1, 1, 0.88)
        label = str(i + 1)
        ext = ctx.text_extents(label)
        ctx.move_to(px - ext.width / 2 - ext.x_bearing, py + ext.height / 2)
        ctx.show_text(label)

    # Main narrative card
    rounded_rect(ctx, 82, 82, 952, 500, 30)
    card_grad = cairo.LinearGradient(82, 82, 1034, 582)
    card_grad.add_color_stop_rgba(0, 1, 1, 1, 0.10)
    card_grad.add_color_stop_rgba(1, 1, 1, 1, 0.04)
    ctx.set_source(card_grad)
    ctx.fill_preserve()
    ctx.set_source_rgba(1, 1, 1, 0.12)
    ctx.set_line_width(2)
    ctx.stroke()

    ctx.rectangle(118, 136, 150, 4)
    ctx.set_source_rgb(*gold)
    ctx.fill()

    badge = f"IDEA2CREATION • PREMIUM INSERT {slot['order']:02d}"
    ctx.select_font_face('Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(26)
    ctx.set_source_rgb(*gold)
    ctx.move_to(118, 170)
    ctx.show_text(badge)

    chapter_label = 'Appendices' if slot['chapter'] == 10 else f"Chapter {slot['chapter']} • Growth System"
    ctx.set_font_size(22)
    ctx.set_source_rgba(1, 1, 1, 0.78)
    ctx.move_to(118, 214)
    ctx.show_text(chapter_label)

    ctx.select_font_face('Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    title_lines = wrap_text(ctx, slot['title'], 810, 58)
    y = 292
    ctx.set_source_rgb(1, 1, 1)
    for line in title_lines[:3]:
        ctx.move_to(118, y)
        ctx.show_text(line)
        y += 72

    ctx.select_font_face('Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    subtitle_lines = wrap_text(ctx, slot['subtitle'], 780, 27)
    y += 6
    ctx.set_source_rgba(1, 1, 1, 0.88)
    for line in subtitle_lines[:4]:
        ctx.move_to(118, y)
        ctx.show_text(line)
        y += 36

    labels = ['Offer design', 'AI workflow', 'Revenue motion']
    sublabels = [
        'Sharper structure for a more premium product experience.',
        'Connected systems that move from idea to execution.',
        'Positioning built to support sales, delivery, and scale.',
    ]
    for i, (label, sublabel) in enumerate(zip(labels, sublabels)):
        px = 1098
        py = 462 + i * 86
        rounded_rect(ctx, px, py, 388, 68, 20)
        panel = cairo.LinearGradient(px, py, px + 388, py + 68)
        panel.add_color_stop_rgba(0, accent[0], accent[1], accent[2], 0.16)
        panel.add_color_stop_rgba(1, 1, 1, 1, 0.03)
        ctx.set_source(panel)
        ctx.fill_preserve()
        ctx.set_source_rgba(1, 1, 1, 0.16)
        ctx.set_line_width(1.2)
        ctx.stroke()
        ctx.arc(px + 28, py + 24, 8, 0, 2 * math.pi)
        ctx.set_source_rgb(*gold)
        ctx.fill()
        ctx.select_font_face('Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(22)
        ctx.set_source_rgb(1, 1, 1)
        ctx.move_to(px + 48, py + 28)
        ctx.show_text(label)
        ctx.select_font_face('Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        ctx.set_font_size(15)
        ctx.set_source_rgba(1, 1, 1, 0.76)
        ctx.move_to(px + 48, py + 50)
        ctx.show_text(sublabel)

    ctx.select_font_face('Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(18)
    ctx.set_source_rgba(1, 1, 1, 0.72)
    ctx.move_to(118, 842)
    ctx.show_text('Premium ebook art direction • AI systems • digital offer positioning • rebuilt from source')

    out_path.parent.mkdir(parents=True, exist_ok=True)
    surface.write_to_png(str(out_path))


def ensure_visual_assets(slots: List[Dict[str, Any]]) -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    for slot in slots:
        out_path = ASSET_DIR / f"visual-{slot['order']:02d}.png"
        generate_visual(slot, out_path)
        slot['image_path'] = out_path
        slot['image_rel'] = out_path.relative_to(EBOOK_DIR).as_posix()
        slot['caption'] = f"{slot['title']} — premium visual insert {slot['order']:02d}."


def build_html(blocks: List[Dict[str, Any]], slots: List[Dict[str, Any]]) -> str:
    slot_map = {slot['block_index']: slot for slot in slots}
    toc_items = []
    for block in blocks:
        if block['type'] == 'heading' and block['level'] == 1 and (block.get('chapter') or 0) <= 10:
            toc_items.append((block['text'], block['id']))

    parts: List[str] = []
    parts.append("<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>")
    parts.append("<title>Idea2Creation Final Ebook</title>")
    parts.append("<style>")
    parts.append("""
        @page { size: 8.5in 11in; margin: 0.7in 0.72in 0.8in 0.72in; }
        * { box-sizing: border-box; }
        body { margin: 0; font-family: Georgia, 'Times New Roman', serif; color: #172033; background: #f5f7fb; }
        .cover, .toc, .chapter-open { page-break-after: always; }
        .cover {
            position: relative; overflow: hidden;
            min-height: 10in; display: flex; flex-direction: column; justify-content: center;
            padding: 0.85in; color: white;
            background: radial-gradient(circle at 15% 18%, rgba(255,255,255,.16), transparent 24%), radial-gradient(circle at 82% 18%, rgba(241,201,98,.22), transparent 18%), linear-gradient(135deg, #10192f, #24488c 54%, #56a8dc);
        }
        .cover::before {
            content: ''; position: absolute; inset: 0.42in; border-radius: 28px;
            border: 1px solid rgba(255,255,255,.14); background: linear-gradient(135deg, rgba(255,255,255,.08), rgba(255,255,255,.02));
        }
        .cover::after {
            content: ''; position: absolute; right: -0.5in; bottom: -0.6in; width: 4.8in; height: 4.8in; border-radius: 50%;
            border: 1px solid rgba(255,255,255,.14); box-shadow: 0 0 0 32px rgba(255,255,255,.04), 0 0 0 74px rgba(255,255,255,.03);
        }
        .cover > * { position: relative; z-index: 1; }
        .cover-kicker { font: 700 12px/1.2 Arial, sans-serif; letter-spacing: 0.25em; text-transform: uppercase; color: #f3ca6a; }
        .cover-rule { width: 1.5in; height: 4px; background: linear-gradient(90deg, #f3ca6a, rgba(243,202,106,.15)); border-radius: 999px; margin: 14px 0 18px; }
        .cover h1 { font: 700 36px/1.05 Arial, sans-serif; margin: 0 0 14px; max-width: 7.2in; }
        .cover p { font-size: 15px; line-height: 1.68; max-width: 6.3in; margin: 0 0 12px; }
        .cover-meta { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; max-width: 6.1in; margin-top: 16px; }
        .cover-card { border: 1px solid rgba(255,255,255,.16); border-radius: 18px; padding: 14px 16px; background: rgba(7,17,34,.24); }
        .cover-card strong { display: block; font: 700 12px Arial, sans-serif; letter-spacing: .14em; text-transform: uppercase; color: #f3ca6a; margin-bottom: 8px; }
        .cover-card span { font-size: 13px; line-height: 1.55; display: block; }
        .cover-badges { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 18px; max-width: 6.5in; }
        .cover-badge { border: 1px solid rgba(255,255,255,.22); padding: 10px 14px; border-radius: 999px; font: 600 12px Arial, sans-serif; background: rgba(255,255,255,.08); }
        .cover-footer { margin-top: 26px; font: 500 12px Arial, sans-serif; opacity: .82; }
        .toc { background: white; min-height: 10in; padding: 0.4in 0; }
        .toc h2 { font: 700 28px Arial, sans-serif; margin: 0 0 18px; color: #172033; }
        .toc-grid { border-top: 3px solid #3158a7; padding-top: 12px; }
        .toc-item { display: flex; align-items: baseline; gap: 10px; padding: 8px 0; font-size: 15px; }
        .toc-item .dots { flex: 1; border-bottom: 1px dotted #9eb2d0; transform: translateY(-2px); }
        .toc-note { margin-top: 20px; color: #4b5a77; font-size: 13px; }
        .chapter-open {
            position: relative; overflow: hidden;
            min-height: 10in; display: flex; flex-direction: column; justify-content: flex-end; gap: 16px;
            padding: 0.6in; color: white; background: linear-gradient(150deg, #0f1930, #224687 60%, #59aadb);
        }
        .chapter-open::before {
            content: ''; position: absolute; inset: 0.38in; border-radius: 26px; border: 1px solid rgba(255,255,255,.14);
            background: linear-gradient(135deg, rgba(255,255,255,.04), rgba(255,255,255,.01));
        }
        .chapter-open > * { position: relative; z-index: 1; }
        .chapter-open .eyebrow { font: 700 12px Arial, sans-serif; text-transform: uppercase; letter-spacing: .22em; color: #f4cf72; }
        .chapter-open h2 { font: 700 30px/1.08 Arial, sans-serif; margin: 0; max-width: 6.5in; }
        .chapter-open p { margin: 0; font-size: 15px; line-height: 1.62; max-width: 6.2in; }
        .chapter-open .chapter-open-grid { display: grid; grid-template-columns: 1.02fr .98fr; gap: 18px; align-items: end; }
        .chapter-open .chapter-open-copy { display: flex; flex-direction: column; gap: 14px; }
        .chapter-open .chapter-open-panel { border: 1px solid rgba(255,255,255,.14); border-radius: 20px; padding: 16px; background: rgba(9,18,37,.26); }
        .chapter-open .chapter-open-panel strong { display: block; font: 700 12px Arial, sans-serif; text-transform: uppercase; letter-spacing: .14em; color: #f4cf72; margin-bottom: 8px; }
        .chapter-open img { width: 100%; border-radius: 18px; margin-top: 10px; box-shadow: 0 18px 42px rgba(7, 17, 34, .28); }
        .chapter-body { background: white; padding-top: 10px; }
        h1.section-title { font: 700 26px Arial, sans-serif; color: #17315d; margin: 36px 0 14px; page-break-before: always; }
        h2 { font: 700 20px Arial, sans-serif; color: #1d3767; margin: 30px 0 12px; }
        h3 { font: 700 16px Arial, sans-serif; color: #39517e; margin: 24px 0 10px; }
        p { margin: 0 0 14px; font-size: 13.2px; line-height: 1.72; text-align: justify; }
        ul, ol { margin: 0 0 16px 20px; padding-left: 16px; }
        li { margin: 0 0 8px; font-size: 13.2px; line-height: 1.62; }
        blockquote { margin: 20px 0; padding: 16px 18px; border-left: 4px solid #4f82d8; background: #f4f8fe; color: #22324f; }
        pre { white-space: pre-wrap; background: #101a30; color: #eff4ff; border-radius: 14px; padding: 16px; font: 12px/1.55 'Courier New', monospace; overflow-wrap: anywhere; margin: 18px 0 22px; }
        code { background: #eef3fb; padding: 2px 5px; border-radius: 5px; font: 12px 'Courier New', monospace; }
        hr { border: 0; height: 1px; background: linear-gradient(90deg, transparent, #7ea1da, transparent); margin: 26px 0; }
        figure.visual { margin: 20px 0 24px; }
        figure.visual img { width: 100%; border-radius: 18px; display: block; box-shadow: 0 14px 34px rgba(13, 30, 62, .16); }
        figure.visual figcaption { font: italic 11.5px/1.5 Georgia, serif; color: #536381; margin-top: 8px; }
        .two-up { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 22px 0; }
        .panel { border: 1px solid #d9e4f5; border-radius: 16px; padding: 16px; background: #f8fbff; }
        .panel h4 { margin: 0 0 8px; font: 700 14px Arial, sans-serif; color: #19315d; }
        .endcap { margin: 30px 0 8px; padding: 20px; border-radius: 18px; background: linear-gradient(135deg, #edf4ff, #f8fbff); border: 1px solid #d6e2f7; }
        .endcap strong { font-family: Arial, sans-serif; }
        a { color: #244f9e; text-decoration: none; }
    """)
    parts.append("</style></head><body>")

    parts.append("<section class='cover'>")
    parts.append("<div class='cover-kicker'>The Self Made Money Blueprint</div><div class='cover-rule'></div>")
    parts.append("<h1>Idea2Creation — premium rebuilt edition for turning raw ideas into launch-ready digital products.</h1>")
    parts.append("<p>This final sellable edition has been rebuilt from recovered source files and refined with a stronger interior art direction so the ebook feels more premium, more coherent, and more credible at delivery.</p>")
    parts.append("<p>Inside is a full operating model for moving from idea, to validation, to build, to sales, to fulfillment, to growth using OpenClaw-style agent workflows and digital offer structure.</p>")
    parts.append("<div class='cover-meta'><div class='cover-card'><strong>What this delivers</strong><span>Strategy, workflows, chapter pacing, and visual reinforcement built to make the product feel complete instead of text-heavy.</span></div><div class='cover-card'><strong>Why this version matters</strong><span>It presents better as a paid product, reads cleaner, and gives the buyer more visual relief as they move through the system.</span></div></div>")
    parts.append("<div class='cover-badges'><span class='cover-badge'>Premium interior design pass</span><span class='cover-badge'>37 visual inserts</span><span class='cover-badge'>Chapter-based pacing</span><span class='cover-badge'>Launch-ready PDF refresh</span></div>")
    parts.append("<div class='cover-footer'>Prepared for Poly Mintman • Final ebook refresh</div>")
    parts.append("</section>")

    parts.append("<section class='toc'><h2>Table of Contents</h2><div class='toc-grid'>")
    for idx, (title, anchor) in enumerate(toc_items, start=1):
        label = title if title.lower().startswith('chapter') else f'Appendices'
        parts.append(f"<div class='toc-item'><span>{idx}. <a href='#{anchor}'>{html.escape(label)}</a></span><span class='dots'></span></div>")
    parts.append("</div><div class='toc-note'>Visual pacing note: each chapter now includes multiple premium image moments so the reading experience feels more polished and sellable without becoming cluttered.</div></section>")

    chapter_open_done = set()
    for idx, block in enumerate(blocks):
        if block['type'] == 'heading' and block['level'] == 1:
            chap = block.get('chapter') or 0
            if chap not in chapter_open_done:
                opener_slot = slot_map.get(idx)
                kicker = 'Appendices' if chap == 10 else f'Chapter {chap}'
                summary = summarize_after(blocks, idx)
                parts.append(f"<section class='chapter-open' id='{block['id']}'><div class='chapter-open-grid'><div class='chapter-open-copy'><div class='eyebrow'>{kicker}</div><h2>{html.escape(block['text'])}</h2><p>{html.escape(summary)}</p><div class='chapter-open-panel'><strong>Chapter focus</strong>{html.escape('This section sharpens the reader’s understanding, moves the system forward, and keeps the book feeling like a premium guided framework instead of a raw draft.')}</div></div><div>")
                if opener_slot:
                    parts.append(f"<img src='{opener_slot['image_rel']}' alt='{html.escape(opener_slot['title'])}'>")
                parts.append("</div></div></section><div class='chapter-body'>")
                chapter_open_done.add(chap)
            parts.append(f"<h1 class='section-title'>{html.escape(block['text'])}</h1>")
            continue

        if idx in slot_map and not (block['type'] == 'heading' and block['level'] == 1):
            slot = slot_map[idx]
            parts.append(f"<figure class='visual'><img src='{slot['image_rel']}' alt='{html.escape(slot['title'])}'><figcaption>{html.escape(slot['caption'])}</figcaption></figure>")

        if block['type'] == 'heading':
            tag = 'h2' if block['level'] == 2 else 'h3'
            parts.append(f"<{tag} id='{block['id']}'>{html.escape(block['text'])}</{tag}>")
        elif block['type'] == 'paragraph':
            parts.append(f"<p>{format_inline(block['text'])}</p>")
        elif block['type'] == 'blockquote':
            parts.append(f"<blockquote>{format_inline(block['text'])}</blockquote>")
        elif block['type'] == 'ul':
            items = ''.join(f"<li>{format_inline(item)}</li>" for item in block['items'])
            parts.append(f"<ul>{items}</ul>")
        elif block['type'] == 'ol':
            items = ''.join(f"<li>{format_inline(item)}</li>" for item in block['items'])
            parts.append(f"<ol>{items}</ol>")
        elif block['type'] == 'code':
            code = html.escape(block['text'])
            parts.append(f"<pre><code>{code}</code></pre>")
        elif block['type'] == 'hr':
            parts.append('<hr>')

    parts.append("<div class='endcap'><strong>Final note:</strong> this refreshed edition is designed to read cleaner, present better, and feel more like a premium digital product at delivery time. The interior now has balanced visual relief, chapter pacing, and clearer progression from concept through deployment.</div>")
    parts.append("</div></body></html>")
    return ''.join(parts)


def export_pdf(html_path: Path, pdf_path: Path) -> None:
    cmd = [
        'chromium',
        '--headless=new',
        '--disable-gpu',
        '--no-sandbox',
        '--allow-file-access-from-files',
        f'--print-to-pdf={pdf_path}',
        str(html_path),
    ]
    subprocess.run(cmd, check=True)


def main() -> None:
    EBOOK_DIR.mkdir(parents=True, exist_ok=True)
    blocks = load_blocks()
    slots = choose_visual_slots(blocks)
    ensure_visual_assets(slots)
    html_doc = build_html(blocks, slots)
    HTML_OUT.write_text(html_doc)
    export_pdf(HTML_OUT, PDF_OUT)
    print(f'Built HTML: {HTML_OUT}')
    print(f'Built PDF: {PDF_OUT}')
    print(f'Visual count: {len(slots)}')


if __name__ == '__main__':
    main()
