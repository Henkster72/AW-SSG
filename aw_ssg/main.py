import subprocess
from env_loader import crucial_vars, open_vars, set_env_variables
from sitemap_generator import generate_sitemap
from rss_feed_generator import create_rss_feed

# Import your main site-rendering logic from a separate file
from site_renderer import render_site

def main():
    # 1) Prompt for dev mode
    development_mode = input("Is this development mode? (y/n): ").lower() == 'y'

    # 2) Render the site (subdirectory-agnostic, includes logic for 'section_' partials)
    render_site(development_mode=development_mode)

    # 3) Generate a sitemap (if you want it)
    generate_sitemap(crucial_vars['BASE_URL'])

    # 4) Optionally generate an RSS feed
    #    (If you want a universal feed for all subdirectories, do it here,
    #     or do it inside render_site if you prefer.)
    create_rss_feed(
        page_references=[],  # Supply your references if collected in site_renderer
        base_url=crucial_vars['BASE_URL'],
        language="nl",
        output_path='output/rss.xml'
    )

    print("Site generated in the 'output' directory.")

    # 5) If NOT dev mode, optionally purge CSS
    if not development_mode:
        purge = input("Do you want to purge and minify CSS? (y/n): ").lower() == 'y'
        if purge:
            subprocess.run(["python3", "purge_tailwind.py"])

        # 6) Optionally upload to FTP
        upload = input("Do you want to upload to the FTP server? (y/n): ").lower() == 'y'
        if upload:
            subprocess.run(["python3", "upload_output.py"])

if __name__ == "__main__":
    main()
