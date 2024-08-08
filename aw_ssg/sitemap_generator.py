import os
import datetime

def generate_sitemap(baseurl):
    sitemap_entries = []
    priority_map = {
        'index.html': '1.0',
        'contact/index.html': '1.0',
        'thankyou/index.html': '0.3',
        'default': '0.7'
    }
    changefreq_map = {
        'index.html': 'daily',
        'contact/index.html': 'yearly',
        'thankyou/index.html': 'yearly',
        'default': 'monthly'
    }

    for root, dirs, files in os.walk('output'):
        for file in files:
            if file.endswith('.html'):
                path = os.path.relpath(os.path.join(root, file), 'output')
                url = f"{baseurl}{path.replace(os.path.sep, '/')}"
                priority = priority_map.get(path.replace(os.path.sep, '/'), priority_map['default'])
                changefreq = changefreq_map.get(path.replace(os.path.sep, '/'), changefreq_map['default'])
                lastmod = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(root, file))).strftime('%Y-%m-%d')
                sitemap_entries.append(f"<url><loc>{url}</loc><priority>{priority}</priority><changefreq>{changefreq}</changefreq><lastmod>{lastmod}</lastmod></url>")

    sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:video="http://www.google.com/schemas/sitemap-video/1.1" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
"""
    sitemap_content += "\n".join(sitemap_entries)
    sitemap_content += "\n</urlset>"

    with open(os.path.join('output', 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    print("Sitemap generated at 'output/sitemap.xml'")

if __name__ == "__main__":
    from env_loader import crucial_vars
    generate_sitemap(crucial_vars['base_url'])
