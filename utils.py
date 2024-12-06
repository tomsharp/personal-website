import os
import re
import csv
from datetime import datetime


def _extract_first_image(markdown_content):
    """Extract the first image URL from the Markdown content."""
    image_pattern = r"!\[.*?\]\((.*?)\)"
    match = re.search(image_pattern, markdown_content)
    return match.group(1) if match else None


def load_posts(newsletter_folder_path: str, posts_csv_filepath: str):
    posts = []
    if os.path.exists(posts_csv_filepath):
        with open(posts_csv_filepath, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Parse datetime fields
                row['created_datetime'] = datetime.strptime(row['created_datetime'], '%Y-%m-%d %H:%M:%S')
                row['last_modified_datetime'] = datetime.strptime(row['last_modified_datetime'], '%Y-%m-%d %H:%M:%S')
                
                # Read the post content and extract the first image
                post_path = os.path.join(newsletter_folder_path, row['filename'])
                if os.path.exists(post_path):
                    with open(post_path, 'r') as file:
                        markdown_content = file.read()
                        row['image'] = _extract_first_image(markdown_content)
                else:
                    row['image'] = None
                
                posts.append(row)
    return posts


def save_subscriber(email: str, subscribers_filepath: str):
    with open(subscribers_filepath, 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([email, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
