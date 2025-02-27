import os
import ftplib
from env_loader import load_env_variables, set_env_variables  # Use your env loader

def preprocess_env_var(value):
    if value and '|' in value:
        return value.split('|')[0]
    return value

# Load environment variables
crucial_vars, open_vars = load_env_variables('.env')
set_env_variables(crucial_vars)
set_env_variables(open_vars)

# FTP credentials and directory details
remote_dir = preprocess_env_var(os.getenv('REMOTE_DIR'))
ftp_address = preprocess_env_var(os.getenv('FTP_ADDRESS'))
ftp_user = preprocess_env_var(os.getenv('FTP_USER'))
ftp_pwd = preprocess_env_var(os.getenv('FTP_PWD'))

def get_ftp_connection():
    print("Establishing FTP connection...")
    ftp = ftplib.FTP(ftp_address)
    ftp.login(ftp_user, ftp_pwd)
    print("Connected.")
    return ftp

def fetch_mod_date(ftp, path):
    """Fetch modification date for a given path."""
    try:
        mod_resp = ftp.sendcmd("MDTM " + path)
        if mod_resp.startswith("213 "):
            mod_date = mod_resp[4:]
            return f"{mod_date[6:8]}-{mod_date[4:6]}-{mod_date[0:4]}"
    except:
        pass
    return "?"

def fetch_size_kb(ftp, path):
    """Fetch size in KB for a given file path."""
    try:
        size = ftp.size(path)
        if size is not None:
            return f"{size/1024:.1f} KB"
    except:
        pass
    return "?"

def is_directory(ftp, path):
    """Check if a given path is a directory by trying to change into it."""
    original = ftp.pwd()
    try:
        ftp.cwd(path)
        ftp.cwd(original)  # revert back if successful
        return True
    except ftplib.error_perm:
        return False

def build_flat_structure(ftp, base_dir):
    """
    Build a flat two-level deep directory structure with alphabetical sorting.
    Returns:
      - selection_list: Mapping of numbers to item details.
    """
    selection_list = {}
    counter = 1

    print(f"Changing to base directory: {base_dir}")
    ftp.cwd(base_dir)

    print("Fetching top-level items...")
    try:
        top_items = sorted(ftp.nlst())
    except ftplib.error_perm:
        top_items = []

    for item in top_items:
        if item in [".", ".."]:
            continue

        item_path = os.path.join(base_dir, item).replace("\\", "/")
        indent = ""  # top-level items have no indentation
        item_info = {
            'number': counter,
            'name': item,
            'path': item_path,
            'is_dir': False,
            'size': "",
            'mod_date': "",
            'indent': indent
        }

        # Check if top-level item is a directory
        if is_directory(ftp, item_path):
            item_info['is_dir'] = True
            item_info['size'] = "-"  # Directories: size not applicable
            item_info['mod_date'] = fetch_mod_date(ftp, item_path)
            selection_list[counter] = item_info
            counter += 1

            print(f"Fetching children of directory: {item_path}")
            try:
                ftp.cwd(item_path)
                second_items = sorted(ftp.nlst())
            except ftplib.error_perm:
                second_items = []
            for sub in second_items:
                if sub in [".", ".."]:
                    continue
                sub_path = os.path.join(item_path, sub).replace("\\", "/")
                child_info = {
                    'number': counter,
                    'name': sub,
                    'path': sub_path,
                    'is_dir': False,
                    'size': "",
                    'mod_date': "",
                    'indent': "   "  # indent second-level items
                }
                if is_directory(ftp, sub_path):
                    child_info['is_dir'] = True
                    child_info['size'] = "-"
                    child_info['mod_date'] = fetch_mod_date(ftp, sub_path)
                else:
                    child_info['size'] = fetch_size_kb(ftp, sub_path)
                    child_info['mod_date'] = fetch_mod_date(ftp, sub_path)
                selection_list[counter] = child_info
                counter += 1
            ftp.cwd("..")  # Return to base directory
        else:
            # It's a file at top level
            item_info['size'] = fetch_size_kb(ftp, item_path)
            item_info['mod_date'] = fetch_mod_date(ftp, item_path)
            selection_list[counter] = item_info
            counter += 1

    print("Sorting items alphabetically by their names within each level...")
    # Sort top-level and second-level items separately
    top_level = [info for info in selection_list.values() if info['indent'] == ""]
    second_level = [info for info in selection_list.values() if info['indent'] != ""]
    top_level.sort(key=lambda x: x['name'].lower())
    second_level.sort(key=lambda x: (x['path'].rsplit('/', 2)[-2].lower(), x['name'].lower()))

    # Rebuild selection_list preserving original numbering for items that still exist.
    sorted_selection = {}
    for info in top_level + second_level:
        sorted_selection[info['number']] = info

    selection_list = sorted_selection
    print("Structure built.")
    return selection_list

def display_structure(selection_list):
    """Display the current in-memory structure without renumbering."""
    print("\nCurrent Listing:")
    for num in sorted(selection_list.keys()):
        info = selection_list[num]
        type_suffix = "/" if info['is_dir'] else ""
        print(f"{info['indent']}{info['number']}. {info['name']}{type_suffix} {info['size']} {info['mod_date']}")

def delete_file(ftp, path):
    print(f"Attempting to delete file: {path}")
    try:
        ftp.delete(path)
        print(f"Deleted file: {path}")
    except ftplib.all_errors as e:
        print(f"Error deleting file {path}: {e}")

def delete_directory(ftp, path):
    """Recursively deletes a directory and its contents."""
    print(f"Attempting to delete directory: {path}")
    try:
        ftp.cwd(path)
    except ftplib.error_perm:
        print(f"Cannot access directory {path}")
        return

    try:
        items = ftp.nlst()
    except ftplib.error_perm as e:
        print(f"Error listing directory {path}: {e}")
        items = []

    for item in items:
        if item in [".", ".."]:
            continue
        full_path = os.path.join(path, item).replace("\\", "/")
        try:
            ftp.cwd(full_path)
            ftp.cwd("..")
            delete_directory(ftp, full_path)
        except ftplib.error_perm:
            delete_file(ftp, full_path)

    ftp.cwd("..")
    try:
        ftp.rmd(path)
        print(f"Deleted directory: {path}")
    except ftplib.all_errors as e:
        print(f"Error removing directory {path}: {e}")

def main():
    print(f"Connecting to {ftp_address} ...")
    ftp = get_ftp_connection()
    try:
        selection_list = build_flat_structure(ftp, remote_dir)
        while True:
            display_structure(selection_list)
            selection = input("Enter number to delete (or 'q' to quit): ").strip()
            if selection.lower() == 'q':
                print("Quitting.")
                break

            try:
                sel_number = int(selection)
            except ValueError:
                print("Invalid selection.")
                continue

            selected = selection_list.get(sel_number)
            if not selected:
                print("No such selection.")
                continue

            path, is_dir = selected['path'], selected['is_dir']
            confirm = input(f"Are you sure you want to delete {'directory' if is_dir else 'file'} '{path}'? (y/N): ").strip()
            if confirm.lower() != 'y':
                print("Deletion cancelled.")
                continue

            if is_dir:
                delete_directory(ftp, path)
            else:
                delete_file(ftp, path)

            # Remove deleted item from in-memory listing
            if sel_number in selection_list:
                del selection_list[sel_number]

            more = input("Do you want to delete more? (y/N): ").strip().lower()
            if more != 'y':
                print("Exiting deletion loop.")
                break

    finally:
        ftp.quit()
        print("FTP connection closed.")

if __name__ == "__main__":
    main()
