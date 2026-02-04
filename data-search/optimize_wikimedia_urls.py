#!/usr/bin/env python3
"""
Optimize Wikimedia Commons photo URLs to use thumbnail API for faster loading
"""

import json
import re

def convert_to_thumbnail(url, width=960):
    """
    Convert Wikimedia Commons URL to thumbnail format

    Example:
    https://upload.wikimedia.org/wikipedia/commons/e/e0/File.jpg
    -> https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/File.jpg/960px-File.jpg
    """
    # Only process Wikimedia Commons URLs
    if 'upload.wikimedia.org/wikipedia/commons/' not in url:
        return url

    # Skip if already a thumbnail URL
    if '/thumb/' in url:
        return url

    # Match pattern: .../commons/{path}/{filename}
    pattern = r'(https://upload\.wikimedia\.org/wikipedia/commons/)([^/]+/[^/]+/[^/]+)$'
    match = re.match(pattern, url)

    if not match:
        return url

    base = match.group(1)
    path_and_file = match.group(2)
    filename = path_and_file.split('/')[-1]

    # Construct thumbnail URL
    thumbnail_url = f"{base}thumb/{path_and_file}/{width}px-{filename}"

    return thumbnail_url

def optimize_bird_photos(input_file, output_file, main_image_width=960, thumbnail_width=330):
    """
    Optimize Wikimedia photo URLs in bird data
    Uses larger size for main images, smaller for thumbnails
    """
    print(f"Loading bird data from {input_file}...")

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    optimized_count = 0

    for bird in data.get('birds', []):
        if 'photos' in bird:
            for i, photo in enumerate(bird['photos']):
                original_url = photo.get('url', '')

                # Use larger size for first photo (main display), smaller for others
                width = main_image_width if i == 0 else thumbnail_width
                optimized_url = convert_to_thumbnail(original_url, width)

                if original_url != optimized_url:
                    photo['url'] = optimized_url
                    optimized_count += 1

    print(f"Optimized {optimized_count} Wikimedia Commons photo URLs")
    print(f"Main images: {main_image_width}px, Thumbnails: {thumbnail_width}px")

    print(f"Writing optimized data to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Done!")

if __name__ == '__main__':
    input_file = '../data/act_birds.json'
    output_file = '../data/act_birds.json'

    # Main images at 960px, additional photos at 330px
    optimize_bird_photos(input_file, output_file, main_image_width=960, thumbnail_width=330)
