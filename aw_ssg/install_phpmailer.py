import os
import ftplib
import requests
import zipfile
import shutil
from io import BytesIO
from datetime import datetime
import time
from dotenv import load_dotenv, set_key


def preprocess_env_var(value):
    if value and '|' in value:
        return value.split('|')[0]
    return value


def update_env_var(key, value, env_file='.env'):
    with open(env_file, 'r') as file:
        lines = file.readlines()

    with open(env_file, 'w') as file:
        found = False
        for line in lines:
            if line.startswith(f'{key}='):
                file.write(f'{key}={value}\n')
                found = True
            else:
                file.write(line)
        if not found:
            file.write(f'{key}={value}\n')


load_dotenv()

# FTP credentials and directory details
remote_dir = preprocess_env_var(os.getenv('REMOTE_DIR'))
ftp_address = preprocess_env_var(os.getenv('FTP_ADDRESS'))
ftp_user = preprocess_env_var(os.getenv('FTP_USER'))
ftp_pwd = preprocess_env_var(os.getenv('FTP_PWD'))
email = preprocess_env_var(os.getenv('MAIL_ADDRESS'))
email_pwd = preprocess_env_var(os.getenv('MAIL_PWD'))
phpmailer_installed = preprocess_env_var(os.getenv('PHPMAILER_INSTALLED', 'FALSE'))

# Directory to extract the zip file
extract_dir = 'extracted_files'
local_test_email_path = 'testemail.html'

# Get the current short date/timestamp
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Debug statements to verify environment variables and timestamp
print(f"{timestamp} - Connecting to {ftp_address}")


def download_and_extract_zip(url, extract_to):
    print(f"Downloading {url}")
    response = requests.get(url)
    if response.status_code == 200:
        with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"Extracted to {extract_to}")
    else:
        print(f"Failed to download the zip file. Status code: {response.status_code}")


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


def check_and_upload_files(ftp, local_dir, remote_dir):
    copied_files = 0
    skipped_files = 0

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

            if remote_file_size is None or local_file_size != remote_file_size:
                print(f"Uploading {local_file_path} to {remote_file_path}")
                upload_file(ftp, local_file_path, remote_file_path)
                copied_files += 1
            else:
                skipped_files += 1

    return copied_files, skipped_files


def inject_values_in_php(email, email_pwd, template_path, output_path):
    with open(template_path, 'r') as file:
        php_content = file.read()

    php_content = php_content.replace('{{ email }}', email).replace('{{ email_pwd }}', email_pwd)

    with open(output_path, 'w') as file:
        file.write(php_content)


def main():
    if phpmailer_installed == 'TRUE':
        test_email_url = f"http://{ftp_user}/testemail.html"
        print(f"PHPMAILER is already installed. Did you test the e-mail feature with {test_email_url}? (y/n)")
        answer = input().strip().lower()
        if answer == 'y':
            ftp = get_ftp_connection()
            try:
                ftp.delete(f'{remote_dir}/testemail.html')
                print("testemail.html deleted.")
            finally:
                ftp.quit()
            return
        else:
            print("Please test the email feature first.")
            return

    start_time = time.time()

    # Step 1: Download and extract the GitHub master zip
    github_zip_url = "https://github.com/PHPMailer/PHPMailer/archive/refs/heads/master.zip"
    download_and_extract_zip(github_zip_url, extract_dir)

    # Step 2: Get FTP connection and upload files
    ftp = get_ftp_connection()
    copied_files = skipped_files = 0
    try:
        copied_files, skipped_files = check_and_upload_files(ftp, extract_dir, remote_dir)
    finally:
        ftp.quit()

    # Step 3: Inject values into the PHP script and upload
    php_template_path = 'send-email.php'
    php_temp_path = 'temp-send-email.php'
    inject_values_in_php(email, email_pwd, php_template_path, php_temp_path)

    ftp = get_ftp_connection()
    try:
        upload_file(ftp, php_temp_path, os.path.join(remote_dir, 'send-email.php').replace("\\", "/"))
        upload_file(ftp, local_test_email_path, os.path.join(remote_dir, 'testemail.html').replace("\\", "/"))
    finally:
        ftp.quit()

    # Cleanup extracted files and temporary PHP script
    shutil.rmtree(extract_dir)
    os.remove(php_temp_path)

    # Update the .env file to set PHPMAILER_INSTALLED=TRUE
    update_env_var('PHPMAILER_INSTALLED', 'TRUE')

    end_time = time.time()
    duration = end_time - start_time

    print(f"Time taken: {duration:.2f} seconds")
    print(f"Files copied: {copied_files}")
    print(f"Files skipped: {skipped_files}")


if __name__ == "__main__":
    main()
