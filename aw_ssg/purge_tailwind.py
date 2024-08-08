import re
import os
import subprocess
from bs4 import BeautifulSoup
import shutil
from pathlib import Path


def extract_tailwind_classes_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'html.parser')

    class_list = []
    for tag in soup.find_all(class_=True):
        classes = tag.get('class')
        if classes:
            class_list.extend(classes)

    return class_list


def extract_tailwind_classes_from_js_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    class_list = re.findall(r'className\s*=\s*"([^"]+)"', content)
    template_literals = re.findall(r'`([^`]+)`', content)
    for literal in template_literals:
        class_list.extend(re.findall(r'class="([^"]+)"', literal))

    all_classes = []
    for classes in class_list:
        all_classes.extend(classes.split())

    return all_classes


def extract_tailwind_classes_from_directory(directory):
    class_set = set()
    for html_file in Path(directory).rglob('*.html'):
        class_set.update(extract_tailwind_classes_from_file(html_file))
    return sorted(class_set)


def extract_tailwind_classes_from_js_directory(directory):
    class_set = set()
    for js_file in Path(directory).rglob('*.js'):
        class_set.update(extract_tailwind_classes_from_js_file(js_file))
    return sorted(class_set)


def create_tailwind_config(classes, output_file='tailwind.config.js'):
    config = f"""
    module.exports = {{
      content: [],
      safelist: {classes},
      theme: {{
        extend: {{}},
      }},
      plugins: [],
    }}
    """

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(config)


def print_lines(content, step, first=False):
    print(f"\n\n--- {step} ---")
    lines = content.split('\n')
    if first:
        for line in lines[:25]:
            print(line)
    else:
        for line in lines[-25:]:
            print(line)


def purge_tailwind_css(output_css='output\\static\\tailwind_min.css'):
    # Check if npx is available
    npx_path = shutil.which('npx')
    if not npx_path:
        raise EnvironmentError(
            "npx command not found. Make sure Node.js and npm are installed and npx is available in your PATH.")

    # Run Tailwind CSS CLI to generate purged CSS
    subprocess.run([npx_path, 'tailwindcss', '-o', output_css])

    # Read the generated CSS content
    with open(output_css, 'r', encoding='utf-8') as file:
        css_content = file.read()

    print_lines(css_content, "Initial CSS Content")

    # Remove CSS comments
    css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
    print_lines(css_content, "After Removing Comments")

    # Remove attributes with empty values
    css_content = re.sub(r'--tw-[\w-]+:\s*;\s*\n', '', css_content)
    print_lines(css_content, "After Removing Attributes with Empty Values")

    # Remove improperly closed CSS blocks
    css_content = remove_improperly_closed_blocks(css_content)
    print_lines(css_content, "After Removing Improperly Closed Blocks")

    # Remove empty lines and whitespace
    css_content = re.sub(r'\n\s*\n', '\n', css_content)
    print_lines(css_content, "After Removing Empty Lines and Whitespace")

    # Ensure every CSS block is properly closed, especially for media queries
    css_content = ensure_proper_closures(css_content)
    print_lines(css_content, "After Ensuring Proper Closures", first=False)

    with open(output_css, 'w', encoding='utf-8') as file:
        file.write(css_content)


def remove_improperly_closed_blocks(css_content):
    # Remove lines with CSS properties outside of blocks
    css_content = re.sub(r'^\s*--tw-[\w-]+:\s*\'[^\']*\';\s*$', '', css_content, flags=re.MULTILINE)
    # Ensure every block is properly closed
    css_content = re.sub(r'([^{]*{[^}]*})\s*{', r'\1', css_content)
    return css_content


def ensure_proper_closures(css_content):
    # Add closing braces for unclosed media queries
    open_blocks = []
    lines = css_content.split('\n')
    fixed_lines = []

    for line in lines:
        if re.match(r'^\s*@media[^{]*{$', line):
            open_blocks.append('}')
        elif re.match(r'^\s*}$', line) and open_blocks:
            open_blocks.pop()
        fixed_lines.append(line)

    while open_blocks:
        fixed_lines.append('}')
        open_blocks.pop()

    return '\n'.join(fixed_lines)


def main():
    templates_dir = 'templates'  # Change this to your templates directory path
    static_js_dir = 'output/static'  # Directory for JavaScript files
    tailwind_config_file = 'tailwind.config.js'

    classes = set(extract_tailwind_classes_from_directory(templates_dir))
    classes.update(extract_tailwind_classes_from_js_directory(static_js_dir))
    create_tailwind_config(sorted(classes), tailwind_config_file)
    purge_tailwind_css()


if __name__ == "__main__":
    main()
