import os
import xml.etree.ElementTree as ET
from datetime import datetime
from urllib.parse import urljoin
import mimetypes  # To detect the MIME type of the image file

# Mapping of Dutch month abbreviations to English equivalents
DUTCH_TO_ENGLISH_MONTHS = {
    'jan': 'Jan',
    'feb': 'Feb',
    'mrt': 'Mar',
    'apr': 'Apr',
    'mei': 'May',
    'jun': 'Jun',
    'jul': 'Jul',
    'aug': 'Aug',
    'sep': 'Sep',
    'okt': 'Oct',
    'nov': 'Nov',
    'dec': 'Dec'
}


def convert_dutch_date_to_rss_format(dutch_date):
    """
    Convert a Dutch date string (e.g., 'jun 23, 2020') to RSS-compliant format.

    Parameters:
        dutch_date (str): The date string in Dutch format.

    Returns:
        str: The date string in RSS-compliant format.
    """
    # Split the date string into components
    for dutch_month, english_month in DUTCH_TO_ENGLISH_MONTHS.items():
        if dutch_month in dutch_date.lower():
            dutch_date = dutch_date.lower().replace(dutch_month, english_month)

    # Parse the updated string into a datetime object
    try:
        date_obj = datetime.strptime(dutch_date, '%b %d, %Y')
    except ValueError as e:
        raise ValueError(f"Error parsing date '{dutch_date}': {e}")

    # Convert the datetime object to RSS format
    return date_obj.strftime('%a, %d %b %Y %H:%M:%S +0000')


def create_rss_feed(page_references, base_url, language="en", output_path='output/rss.xml'):
    """
    Generate an RSS feed from the blog metadata.

    Parameters:
        page_references (list): List of dictionaries containing blog metadata.
        base_url (str): The base URL of the website.
        language (str): Language for the RSS feed (default is "en").
        output_path (str): The file path to save the RSS XML file.
    """
    # Manually create the root element to ensure proper attributes
    rss = ET.Element("rss")
    rss.set("version", "2.0")  # Set version as an attribute

    channel = ET.SubElement(rss, "channel")

    # Add required channel metadata
    ET.SubElement(channel, "title").text = "NTG Blog"  # Replace with your blog's title in Dutch
    ET.SubElement(channel, "link").text = base_url
    ET.SubElement(channel, "description").text = "Blijf op de hoogte van onze nieuwste blogposts."  # Dutch description
    ET.SubElement(channel, "language").text = language
    ET.SubElement(channel, "lastBuildDate").text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')

    # Add each blog post as an item
    for blog in page_references:
        item = ET.SubElement(channel, "item")
        page_url = urljoin(base_url, f"blog/{blog['page_name']}/")
        ET.SubElement(item, "title").text = blog['page_title']
        ET.SubElement(item, "link").text = page_url
        ET.SubElement(item, "guid").text = page_url

        # Convert the Dutch date to RSS-compliant format
        try:
            rss_date = convert_dutch_date_to_rss_format(blog['post_date'])
            ET.SubElement(item, "pubDate").text = rss_date
        except ValueError as e:
            print(f"Skipping blog '{blog['page_name']}' due to invalid date: {e}")
            continue

        ET.SubElement(item, "description").text = f"Lees meer over {blog['page_title']}."

        # Add an enclosure for the blog picture
        if 'page_picture' in blog and blog['page_picture']:
            picture_url = urljoin(base_url, f"static/images/{blog['page_picture']}")
            ET.SubElement(item, "enclosure", {
                "url": picture_url,
                "type": mimetypes.guess_type(blog['page_picture'])[0] or "image/jpeg"
            })

    # Convert the XML tree to a string
    tree = ET.ElementTree(rss)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    print(f"RSS feed gegenereerd op {output_path}")
