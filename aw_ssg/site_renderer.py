import os
import re
import json
import csv
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

from env_loader import crucial_vars, open_vars
from meta_tags_processor import load_meta_tags

TIMESTAMPS_FILE = 'template_timestamps.json'

# Load previous timestamps
if os.path.exists(TIMESTAMPS_FILE):
    with open(TIMESTAMPS_FILE, 'r', encoding='utf-8') as f:
        previous_timestamps = json.load(f)
else:
    previous_timestamps = {}

# Merge env vars into a single dict
context_vars = {k.lower(): v for k, v in open_vars.items()}

def smart_static_filter(path, depth):
    if path.endswith(('.jpg','.jpeg','.webp','.avif','.png','.gif', '.mp4', '.mov','.ico','.svg')):
        folder = 'static/images'
    else:
        folder = 'static'
    return f"{'../' * depth}{folder}/{path}"

def url_filter(path, depth):
    return f"{'../' * depth}{path.replace('.html', '')}/"

def round_to_minute(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    return datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute).timestamp()

def format_european_date(ts):
    dt = datetime.fromtimestamp(ts)
    return dt.strftime('%d %B %Y')

def preprocess_template(content, depth):
    """
    1) Handle {% include "section_..." %} partials at the same depth
    2) Convert {{ file.jpg }} placeholders to Jinja filters (static/url)
    3) Inject environment variables
    4) Convert {% extends "base.html" %} to extends "temp_base_X.html"
    """
    def include_section(match):
        included_template = match.group(1)
        if included_template.startswith("section_"):
            partial_path = os.path.join('templates', included_template)
            if os.path.exists(partial_path):
                with open(partial_path, 'r', encoding='utf-8') as pf:
                    partial_content = pf.read()
                return preprocess_template(partial_content, depth)
        return match.group(0)  # fallback: no change

    def replace_assets(match):
        file_path = match.group(1)
        if file_path.endswith(('.jpg','.jpeg','.webp','.avif','.png','.gif', '.mp4', '.mov','.ico','.svg','.css','.js','.woff2','.html','.pdf')):
            if file_path.endswith('.html'):
                return f"{{{{ '{file_path}' | url({depth}) }}}}"
            else:
                return f"{{{{ '{file_path}' | static({depth}) }}}}"
        return match.group(0)

    # Replace {% include "section_..." %} first
    content = re.sub(r"\{% include ['\"](section_[^'\"]+)['\"] %\}", include_section, content)

    # Replace {{ file.xxx }}
    content = re.sub(
        r"\{\{\s*([\w/\-\.\(\)%]+\.(?:jpg|jpeg|webp|avif|png|gif|mp4|mov|ico|svg|css|js|woff2|html|pdf))\s*\}\}",
        replace_assets,
        content
    )

    # Replace environment variables
    for k, v in context_vars.items():
        if isinstance(v, str):
            content = content.replace(f"{{{{ {k} }}}}", v)

    # Replace extends for depth-based base template
    content = content.replace('{% extends "base.html" %}',
                              f'{{% extends "temp_base_{depth}.html" %}}')
    return content

def load_social_media_links(csv_file):
    """Optional: loads links from a CSV; omit if you don’t need it."""
    social_share_links = []
    contact_follow_links = []
    if not os.path.exists(csv_file):
        return social_share_links, contact_follow_links

    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row = {k.lower(): v for k,v in row.items()}
            share_url = row.get('shareurl')
            contact_url = row.get('contacturl')
            name = row.get('name')
            icon = row.get('icon')
            bgcolor = row.get('bgcolor')
            color = row.get('color')
            text = row.get('text')
            handle = row.get('handle')

            if share_url:
                social_share_links.append({
                    'name': name,
                    'url': share_url,
                    'icon': icon,
                    'bgcolor': bgcolor,
                    'color': color
                })
            if handle and contact_url:
                formatted = contact_url.format(handle)
                contact_follow_links.append({
                    'name': name,
                    'url': formatted,
                    'icon': icon,
                    'bgcolor': bgcolor,
                    'color': color,
                    'text': text.format(handle) if text else ''
                })

    return social_share_links, contact_follow_links

def render_site(development_mode=False):
    """
    Renders all .html templates in a subdirectory-agnostic way:
      - processes 'section_' partials
      - collects subdir “cards”
      - writes overview pages if `<subdir>.html` exists
    """
    # Initialize local Jinja environment
    env = Environment(loader=FileSystemLoader('templates'))
    env.filters['static'] = smart_static_filter
    env.filters['url'] = url_filter

    # Optionally load your CSV for social links, if used
    social_share_links, contact_follow_links = load_social_media_links('socialmedia.csv')

    # Gather all .html except base.html, temp_*, section_*
    all_templates = []
    for root, dirs, files in os.walk('templates'):
        for file in files:
            if file.endswith('.html'):
                if file.startswith('temp_') or file == 'base.html' or file.startswith('section_'):
                    continue
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, 'templates')
                all_templates.append(rel_path)

    # Check if base.html changed
    base_path = os.path.join('templates', 'base.html')
    base_mtime = round_to_minute(os.path.getmtime(base_path))
    base_changed = previous_timestamps.get('base.html', 0) < base_mtime
    previous_timestamps['base.html'] = base_mtime

    # Preprocess base.html for each depth
    with open(base_path, 'r', encoding='utf-8') as bf:
        base_content = bf.read()
    for depth in range(3):
        pre_base = preprocess_template(base_content, depth)
        # Insert meta tags
        meta_tags = load_meta_tags('meta.txt', {**crucial_vars, **open_vars})
        pre_base = pre_base.replace('{{ meta_tags }}', meta_tags)

        temp_base_path = os.path.join('templates', f'temp_base_{depth}.html')
        with open(temp_base_path, 'w', encoding='utf-8') as tbf:
            tbf.write(pre_base)

    # Collect references for subdir pages
    subdir_references = []
    temp_files = []

    # Render each discovered template
    for rel_path in all_templates:
        parts = rel_path.split(os.sep)
        if len(parts) == 1:
            # top-level
            template_name = parts[0]
            if template_name == 'index.html':
                depth = 0
            else:
                depth = 1
        else:
            depth = 2

        full_path = os.path.join('templates', rel_path)
        file_mtime = round_to_minute(os.path.getmtime(full_path))
        last_time = previous_timestamps.get(rel_path, 0)

        # if not base_changed and last_time >= file_mtime:
        #     print(f"Skipping {rel_path} (unchanged)")
        #     continue

        with open(full_path, 'r', encoding='utf-8') as f:
            raw_content = f.read()
        pre_content = preprocess_template(raw_content, depth)

        # Write to a temp file for Jinja
        temp_template_name = f"temp_{os.path.basename(rel_path)}"
        temp_template_path = os.path.join('templates', temp_template_name)
        with open(temp_template_path, 'w', encoding='utf-8') as tf:
            tf.write(pre_content)
        temp_files.append(temp_template_path)

        # Pull out "page_" variables
        def extract_val(regex, default):
            match = re.search(regex, pre_content)
            return match.group(1) if match else default

        page_title = extract_val(r'{% set page_title = "(.*?)" %}', "Untitled")
        page_subtitle = extract_val(r'{% set page_subtitle = "(.*?)" %}', "")
        page_picture = extract_val(r'{% set page_picture = "(.*?)" %}', "placeholder.jpg")
        page_date = extract_val(r'{% set page_date = "(.*?)" %}', "")
        page_card_template = extract_val(r'{% set page_card_template = "(.*?)" %}', "generic_card.htm")

        template_vars = {
            'depth': depth,
            'development_mode': development_mode,
            **context_vars,
            'social_share_links': social_share_links,
            'contact_follow_links': contact_follow_links,
            'page_title': page_title,
            'page_subtitle': page_subtitle,
            'page_picture': page_picture,
            'page_date': page_date,
            'created_time': format_european_date(file_mtime)
        }

        # Render with Jinja
        tpl_obj = env.get_template(temp_template_name)
        rendered_html = tpl_obj.render(template_vars)

        # Output path
        if len(parts) == 1:
            if template_name == 'index.html':
                os.makedirs('output', exist_ok=True)
                output_path = os.path.join('output', 'index.html')
                sub_dir = None
                filename_no_ext = 'index'
            else:
                name_no_ext = os.path.splitext(template_name)[0]
                out_dir = os.path.join('output', name_no_ext)
                os.makedirs(out_dir, exist_ok=True)
                output_path = os.path.join(out_dir, 'index.html')
                sub_dir = None
                filename_no_ext = name_no_ext
        else:
            sub_dir = parts[0]
            filename_no_ext = os.path.splitext(parts[1])[0]
            out_dir = os.path.join('output', sub_dir, filename_no_ext)
            os.makedirs(out_dir, exist_ok=True)
            output_path = os.path.join(out_dir, 'index.html')

        with open(output_path, 'w', encoding='utf-8') as out_f:
            out_f.write(rendered_html)
        print(f"Rendered {rel_path} -> {output_path}")

        # If it's a subdir, store a card snippet
        if sub_dir:
            final_date = page_date if page_date else ""
            # final_date = page_date if page_date else template_vars['created_time']
            card_tpl = env.get_template(page_card_template)
            card_html = card_tpl.render(
                page_name=filename_no_ext,
                page_title=page_title,
                page_subtitle=page_subtitle,
                page_picture=page_picture,
                page_date=final_date
            )
            subdir_references.append({
                "sub_dir": sub_dir,
                "card_html": card_html
            })

        # Update timestamps
        previous_timestamps[rel_path] = file_mtime

    # Build subdir overview pages if <subdir>.html exists
    grouped_cards = {}
    for entry in subdir_references:
        grouped_cards.setdefault(entry["sub_dir"], []).append(entry["card_html"])

    for sub_dir, cards in grouped_cards.items():
        # e.g. templates/blog.html => output/blog/index.html
        overview_path = os.path.join('templates', f"{sub_dir}.html")
        if os.path.exists(overview_path):
            with open(overview_path, 'r', encoding='utf-8') as ovf:
                ov_raw = ovf.read()
            ov_preprocessed = preprocess_template(ov_raw, 1)
            temp_ov_name = f"temp_{sub_dir}.html"
            temp_ov_path = os.path.join('templates', temp_ov_name)
            with open(temp_ov_path, 'w', encoding='utf-8') as tof:
                tof.write(ov_preprocessed)
            temp_files.append(temp_ov_path)

            ov_tpl = env.get_template(temp_ov_name)
            ov_html = ov_tpl.render(depth=1, page_references=cards, **context_vars)

            subdir_out_dir = os.path.join('output', sub_dir)
            os.makedirs(subdir_out_dir, exist_ok=True)
            subdir_index = os.path.join(subdir_out_dir, 'index.html')
            with open(subdir_index, 'w', encoding='utf-8') as outf:
                outf.write(ov_html)

            print(f"Rendered {sub_dir}.html -> {subdir_index}")
        else:
            print(f"No overview template for subdir '{sub_dir}'. Skipping overview page.")

    # Clean up temp files
    for tmpf in temp_files:
        if os.path.exists(tmpf):
            os.remove(tmpf)

    for depth in range(3):
        tb = os.path.join('templates', f"temp_base_{depth}.html")
        if os.path.exists(tb):
            os.remove(tb)

    # Save updated timestamps
    with open(TIMESTAMPS_FILE, 'w', encoding='utf-8') as f:
        json.dump(previous_timestamps, f)

    print("Rendering complete!")
