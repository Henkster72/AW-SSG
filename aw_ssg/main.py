import os
import re
import json
import subprocess
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from env_loader import crucial_vars, open_vars, set_env_variables
from sitemap_generator import generate_sitemap
from meta_tags_processor import load_meta_tags

# Path to the file storing the last modified times of the templates
TIMESTAMPS_FILE = 'template_timestamps.json'

# Load the previous timestamps
if os.path.exists(TIMESTAMPS_FILE):
    with open(TIMESTAMPS_FILE, 'r', encoding='utf-8') as f:
        previous_timestamps = json.load(f)
else:
    previous_timestamps = {}

# Debug statement to check crucial_vars and open_vars content
print("Crucial Vars:", crucial_vars)
print("Open Vars:", open_vars)

# Extracting the variables for template rendering
context_vars = {key.lower(): value for key, value in open_vars.items()}

def format_european_date(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime('%d %B %Y')

# Define the smart static file filter
def smart_static_filter(path, depth):
    if path.endswith(('.jpg', '.jpeg', '.webp', '.avif', '.png', '.gif', '.ico', '.svg')):
        folder = 'static/images'
    else:
        folder = 'static'
    return f"{'../' * depth}{folder}/{path}"


# Define the URL filter
def url_filter(path, depth):
    return f"{'../' * depth}{path.replace('.html', '')}/"


# Initialize Jinja2 environment
env = Environment(loader=FileSystemLoader('templates'))

# Add custom filters to the environment
env.filters['static'] = smart_static_filter
env.filters['url'] = url_filter


# Function to preprocess templates
def preprocess_template(content, depth):
    replacements = []

    # Replace placeholders like {{ glitter.jpg }} with {{ 'glitter.jpg' | static(depth) }}
    def replace_match(match):
        file_path = match.group(1)
        if file_path.endswith(
                ('.jpg', '.jpeg', '.webp', '.avif', '.png', '.gif', '.ico', '.svg', '.css', '.js', '.woff2', '.html')):
            if file_path.endswith('.html'):
                replacement = f"{{{{ '{file_path}' | url({depth}) }}}}"
            else:
                replacement = f"{{{{ '{file_path}' | static({depth}) }}}}"
            replacements.append((match.group(0), replacement))
            return replacement
        return match.group(0)

    # Regular expression to match placeholders with file extensions
    pattern = re.compile(r"\{\{\s*([\w-]+\.(jpg|jpeg|webp|avif|png|gif|ico|svg|css|js|woff2|html))\s*\}\}")
    content = pattern.sub(replace_match, content)

    # Replace environment variables in content
    for key, value in context_vars.items():
        content = content.replace(f"{{{{ {key} }}}}", value)

    # Ensure {% extends "base.html" %} is replaced with the correct depth-specific temp_base.html
    content = content.replace('{% extends "base.html" %}', f'{{% extends "temp_base_{depth}.html" %}}')

    return content

# Function to round timestamps to the nearest minute
def round_to_minute(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    return datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute).timestamp()

# Function to render templates
def render_templates(development_mode=False, tabsdata=None):
    # Initialize Jinja2 environment
    env = Environment(loader=FileSystemLoader('templates'))

    # Register custom filters
    env.filters['static'] = smart_static_filter
    env.filters['url'] = url_filter

    # Get all template files
    templates = [f for f in os.listdir('templates') if f.endswith('.html')]

    # Get the modification time of base.html
    base_path = os.path.join('templates', 'base.html')
    base_modified_time = round_to_minute(os.path.getmtime(base_path))
    base_changed = previous_timestamps.get('base.html', 0) < base_modified_time

    # Update the timestamp for base.html
    previous_timestamps['base.html'] = base_modified_time

    # Preprocess the base template first for each depth
    with open(base_path, 'r', encoding='utf-8') as f:
        base_content = f.read()

    for depth in range(3):  # Assuming depth can be 0, 1, or 2
        temp_base_content = preprocess_template(base_content, depth)

        # Load and inject meta tags
        meta_tags = load_meta_tags('meta.txt', {**crucial_vars, **open_vars})
        temp_base_content = temp_base_content.replace('{{ meta_tags }}', meta_tags)

        temp_base_path = os.path.join('templates', f'temp_base_{depth}.html')
        with open(temp_base_path, 'w', encoding='utf-8') as f:
            f.write(temp_base_content)

    # Initialize a list to hold blog references
    blog_references = []

    temp_files = []

    # Render each template
    for template_name in templates:
        if template_name.startswith('temp_') or template_name == 'base.html':
            continue

        # print(f"Processing template: {template_name}")
        template_path = os.path.join('templates', template_name)

        # Determine depth for static file references
        if template_name.startswith('blog_'):
            depth = 2
            template_time = round_to_minute(os.path.getctime(template_path))  # creation time
        elif template_name == 'index.html':
            depth = 0  # Special depth for root index.html
            template_time = round_to_minute(os.path.getmtime(template_path)) #modification time
        else:
            depth = 1
            template_time = round_to_minute(os.path.getmtime(template_path)) #modification time

        # Skip rendering if the template has not changed and base.html has not changed
        if not base_changed and not template_name.startswith('blog_') and previous_timestamps.get(template_name, 0) >= template_time:
            print(f"Skipping {template_name} (unchanged)")
            continue

        # Read the template content
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Preprocess the template
        preprocessed_content = preprocess_template(content, depth)

        # Write preprocessed content to a temporary file for debugging
        temp_template_path = os.path.join('templates', f'temp_{template_name}')
        with open(temp_template_path, 'w', encoding='utf-8') as f:
            f.write(preprocessed_content)

        temp_files.append(temp_template_path)

        # Extract variables from the template content
        title_match = re.search(r'{% set blog_title = "(.*?)" %}', preprocessed_content)
        blog_title = title_match.group(1) if title_match else "Blog Post"

        watermark_match = re.search(r'{% set watermark_icon = "(.*?)" %}', preprocessed_content)
        watermark_icon = watermark_match.group(1) if watermark_match else "edit"

        picture_match = re.search(r'{% set blog_picture = "(.*?)" %}', preprocessed_content)
        blog_picture = picture_match.group(1) if picture_match else "contentlaptop.webp"

        # Ensure all necessary variables are defined
        template_vars = {
            'depth': depth,
            'development_mode': development_mode,
            'tabsdata': tabsdata,
            **context_vars,
            'blog_title': blog_title,
            'watermark_icon': watermark_icon,
            'blog_picture': blog_picture,
            'created_time': format_european_date(template_time)
        }

        # Render the template with the variables
        template = env.get_template(f'temp_{template_name}')
        output_content = template.render(template_vars)

        # Determine output path based on template name
        if template_name.startswith('blog_'):
            blog_name = template_name.replace('blog_', '').replace('.html', '')
            output_dir = os.path.join('output', 'blog', blog_name)
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, 'index.html')

            # Add reference to blog for blog.html template
            blog_references.append(
                f"""
                <div class="bg-white p-6 rounded-lg shadow-md card flex flex-col items-center text-center">
                    <a href="../blog/{blog_name}/" class="link flex flex-col items-center"><img src="{{{{ '{blog_picture}' | static(1) }}}}" class="rounded-md" alt="{blog_title}">
                    <h3>{blog_title}</h3>
                    <em class="text-sm">Published {template_vars['created_time']}</em>
                    <span class="link">Read more <span class="pi pi-rightcaret ml-2"></span></span><span class="pi pi-{watermark_icon} ml-2 text-xl basecol"></span></a>
                </div>
                """
            )
        else:
            if template_name == 'index.html':
                output_path = os.path.join('output', 'index.html')
            else:
                dir_name = template_name.split('.')[0]
                output_dir = os.path.join('output', dir_name)
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, 'index.html')

        # Write the rendered content to the output file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output_content)

        print(f"Rendered {template_name} to {output_path}")

        # Update the timestamp
        previous_timestamps[template_name] = template_time

    # Update blog.html with blog references
    if blog_references:
        with open(os.path.join('templates', 'blog.html'), 'r', encoding='utf-8') as f:
            blog_content = f.read()

        blog_content = blog_content.replace(
            '<div id="blogs" class="grid grid-cols-1 md:grid-cols-3 gap-8"></div>',
            f"<div id='blogs' class='grid grid-cols-1 md:grid-cols-3 gap-8'>{''.join(blog_references)}</div>"
        )

        with open(os.path.join('templates', 'temp_blog.html'), 'w', encoding='utf-8') as f:
            f.write(preprocess_template(blog_content, 1))

        temp_files.append(os.path.join('templates', 'temp_blog.html'))

        blog_template = env.get_template('temp_blog.html')
        blog_output_content = blog_template.render(
            depth=1,
            development_mode=development_mode,
            **context_vars
        )

        blog_output_path = os.path.join('output', 'blog', 'index.html')
        os.makedirs(os.path.dirname(blog_output_path), exist_ok=True)
        with open(blog_output_path, 'w', encoding='utf-8') as f:
            f.write(blog_output_content)

    # Cleanup temporary files
    for temp_file in temp_files:
        if os.path.exists(temp_file):
            os.remove(temp_file)

    # Cleanup temporary base files
    for depth in range(3):
        temp_base_path = os.path.join('templates', f'temp_base_{depth}.html')
        if os.path.exists(temp_base_path):
            os.remove(temp_base_path)

    # Save the updated timestamps
    with open(TIMESTAMPS_FILE, 'w', encoding='utf-8') as f:
        json.dump(previous_timestamps, f)

    # Generate sitemap
    generate_sitemap(crucial_vars['BASE_URL'])

if __name__ == "__main__":
    development_mode = input("Is this development mode? (y/n): ").lower() == 'y'

    # Load tabs data
    tabsdata = None
    try:
        with open('output/static/tabsdata.json', 'r', encoding='utf-8') as f:
            tabsdata = json.load(f)
    except FileNotFoundError:
        print("Warning: 'tabsdata.json' not found. Continuing without tabs data.")
    except json.JSONDecodeError:
        print("Error: 'tabsdata.json' is not a valid JSON file. Exiting.")
        exit(1)
    except Exception as e:
        print(f"Error: An unexpected error occurred while loading 'tabsdata.json': {e}")
        exit(1)

    render_templates(development_mode, tabsdata=tabsdata)
    print("Site generated in the 'output' directory.")

    if not development_mode:
        purge = input("Do you want to purge Tailwind classes? (y/n): ").lower() == 'y'
        if purge:
            subprocess.run(["python", "purge_tailwind.py"])

        upload = input("Do you want to upload to the FTP server? (y/n): ").lower() == 'y'
        if upload:
            subprocess.run(["python", "upload_output.py"])
