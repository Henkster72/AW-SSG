import os
import ftplib
from datetime import datetime
import time
import sys
import mimetypes
from env_loader import load_env_variables, set_env_variables  # Import from env_loader.py

def preprocess_env_var(value):
    if value and '|' in value:
        return value.split('|')[0]
    return value

# Load environment variables from the .env file
crucial_vars, open_vars = load_env_variables('.env')
set_env_variables(crucial_vars)
set_env_variables(open_vars)

# FTP credentials and directory details
remote_dir = preprocess_env_var(os.getenv('REMOTE_DIR'))
ftp_address = preprocess_env_var(os.getenv('FTP_ADDRESS'))
ftp_user = preprocess_env_var(os.getenv('FTP_USER'))
ftp_pwd = preprocess_env_var(os.getenv('FTP_PWD'))
local_output_dir = preprocess_env_var(os.getenv('OUTPUT_DIR'))

# Get the current short date/timestamp
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Debug statements to verify environment variables and timestamp
print(f"{timestamp} - Connecting to {ftp_address}")

def get_ftp_connection():
    ftp = ftplib.FTP(ftp_address)
    ftp.login(ftp_user, ftp_pwd)
    return ftp

def upload_file(ftp, local_file_path, remote_file_path):
    with open(local_file_path, 'rb') as file:
        ftp.storbinary(f'STOR {remote_file_path}', file)

def get_remote_file_size(ftp, remote_file_path):
    try:
        return ftp.size(remote_file_path)
    except ftplib.error_perm:
        return None

def get_remote_file_content(ftp, remote_file_path):
    try:
        with open('temp_remote_file', 'wb') as temp_file:
            ftp.retrbinary(f"RETR {remote_file_path}", temp_file.write)
        with open('temp_remote_file', 'rb') as temp_file:
            content = temp_file.read()
        os.remove('temp_remote_file')
        return content
    except ftplib.error_perm:
        return None

def get_local_file_content(local_file_path):
    try:
        with open(local_file_path, 'rb') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading local file {local_file_path}: {e}")
        return None

def is_text_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type and mime_type.startswith('text')

def is_binary_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    binary_mime_types = [
        'application/font-woff2',
        'application/octet-stream',
        'image/jpeg',
        'image/png',
        'image/webp',
        'image/avif',
        'application/pdf',
        'application/zip',
        'application/x-gzip',
        'application/x-tar'
    ]
    return mime_type in binary_mime_types

def print_progress(progress, total):
    percentage = (progress / total) * 100
    bar_length = 40
    filled_length = int(bar_length * progress // total)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    sys.stdout.write(f'\rProgress: |{bar}| {percentage:.2f}% Complete')
    sys.stdout.flush()

def count_files(local_dir):
    total_files = 0
    for root, _, files in os.walk(local_dir):
        for file_name in files:
            total_files += 1
    return total_files

def check_and_upload_files(ftp, local_dir, remote_dir):
    copied_files = 0
    skipped_files = 0

    total_files = count_files(local_dir)
    print(f"Total files to process: {total_files}")
    processed_files = 0

    for root, _, files in os.walk(local_dir):
        relative_path = os.path.relpath(root, local_dir)
        remote_subdir = os.path.join(remote_dir, relative_path).replace("\\", "/")

        # Ensure the remote directory exists
        try:
            ftp.cwd(remote_subdir)
        except ftplib.error_perm:
            ftp.mkd(remote_subdir)
            ftp.cwd(remote_subdir)

        for file_name in files:
            local_file_path = os.path.join(root, file_name)
            remote_file_path = os.path.join(remote_subdir, file_name).replace("\\", "/")

            local_file_size = os.path.getsize(local_file_path)
            remote_file_size = get_remote_file_size(ftp, remote_file_path)

            if remote_file_size is None:
                sys.stdout.write(f"\nCopying new file {local_file_path} to {remote_file_path}\n")
                upload_file(ftp, local_file_path, remote_file_path)
                copied_files += 1
            else:
                if is_text_file(local_file_path):
                    local_content = get_local_file_content(local_file_path)
                    remote_content = get_remote_file_content(ftp, remote_file_path)
                    if local_file_size != remote_file_size or local_content != remote_content:
                        sys.stdout.write(f"\nUpdating existing file {local_file_path} to {remote_file_path}\n")
                        upload_file(ftp, local_file_path, remote_file_path)
                        copied_files += 1
                    else:
                        skipped_files += 1
                elif is_binary_file(local_file_path) or True:  # Handle binary files and ensure size comparison
                    if local_file_size != remote_file_size:
                        sys.stdout.write(f"\nUpdating existing file {local_file_path} to {remote_file_path}\n")
                        upload_file(ftp, local_file_path, remote_file_path)
                        copied_files += 1
                    else:
                        skipped_files += 1

            processed_files += 1
            print_progress(processed_files, total_files)

    sys.stdout.write('\n')  # To move to the next line after the progress bar
    sys.stdout.flush()
    return copied_files, skipped_files

def main():
    start_time = time.time()
    ftp = get_ftp_connection()
    copied_files = skipped_files = 0
    try:
        copied_files, skipped_files = check_and_upload_files(ftp, local_output_dir, remote_dir)
    finally:
        ftp.quit()
    end_time = time.time()
    duration = end_time - start_time

    print(f"\nTime taken: {duration:.2f} seconds")
    print(f"Files copied: {copied_files}")
    print(f"Files skipped: {skipped_files}")

if __name__ == "__main__":
    main()
