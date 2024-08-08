# scripts/init_project.py

import os
import shutil
import sys

def create_initial_structure(project_path):
    source_dir = os.path.dirname(__file__)
    print(f"Source directory: {source_dir}")

    if not os.path.exists(project_path):
        os.makedirs(project_path)
        print(f"Created project directory: {project_path}")
    else:
        print(f"Project directory already exists: {project_path}")

    files_to_copy = [
        'output/.htaccess',
        'output/robots.txt',
        'output/sitemap.xml',
        'output/static/base.js',
        'output/static/popicon.css',
        'output/static/scroll-entrance-min.js',
        'output/static/images/cookies.png',
        'output/static/images/favicon.png',
        'output/static/images/placeholder.webp',
        '.env',
        'meta.txt',
        'tailwind.css',
        'testemail.html',
        'templates/404.html',
        'templates/index.html',
        'templates/base.html'
    ]

    directories_to_create = [
        'output/static/images',
        'templates'
    ]

    for directory in directories_to_create:
        full_directory_path = os.path.join(project_path, directory)
        if not os.path.exists(full_directory_path):
            os.makedirs(full_directory_path)
            print(f"Created directory: {full_directory_path}")
        else:
            print(f"Directory already exists: {full_directory_path}")

    for file in files_to_copy:
        src = os.path.join(source_dir, "..", "aw_ssg", file)
        dest = os.path.join(project_path, file)
        print(f"Copying {src} to {dest}")
        try:
            shutil.copy2(src, dest)
            print(f"Copied {src} to {dest}")
        except Exception as e:
            print(f"Failed to copy {src} to {dest}: {e}")

    print(f"Project structure created at {project_path}")

def main():
    if len(sys.argv) != 2:
        print("Usage: aw-ssg-init <project_path>")
        sys.exit(1)

    project_path = sys.argv[1]
    create_initial_structure(project_path)

if __name__ == "__main__":
    main()
