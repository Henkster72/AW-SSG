import os


def generate_robots_txt(output_folder):
    robots_txt = "User-agent: *\n"

    # Walk through the output folder and list all directories
    for root, dirs, files in os.walk(output_folder):
        # Create relative path from output folder
        rel_path = os.path.relpath(root, output_folder)

        # Ignore the root of the output folder
        if rel_path != '.':
            # Convert to forward slashes for consistency
            rel_path = rel_path.replace(os.sep, '/')
            robots_txt += f"Disallow: /{rel_path}/\n"

    # Additional disallow rules for specific files
    # robots_txt += "Disallow: /static/\n"
    # robots_txt += "Disallow: /static/images/\n"

    # Allow specific paths if needed
    # robots_txt += "Allow: /path/to/specific/file.html\n"

    with open("output\\robots.txt", "w") as file:
        file.write(robots_txt)

    print("robots.txt generated successfully.")


# Specify the path to your output folder
output_folder = "output"
generate_robots_txt(output_folder)
