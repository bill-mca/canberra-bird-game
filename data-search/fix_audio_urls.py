#!/usr/bin/env python3
"""
Fix duplicate xeno-canto.org prefixes in audio URLs
"""

import json
import sys

def fix_audio_url(url):
    """Remove duplicate xeno-canto.org prefix if present"""
    if url.startswith('https://xeno-canto.org/https://xeno-canto.org/'):
        return url.replace('https://xeno-canto.org/https://xeno-canto.org/', 'https://xeno-canto.org/', 1)
    elif url.startswith('https://xeno-canto.org/http://xeno-canto.org/'):
        return url.replace('https://xeno-canto.org/http://xeno-canto.org/', 'https://xeno-canto.org/', 1)
    elif url.startswith('http://xeno-canto.org/https://xeno-canto.org/'):
        return url.replace('http://xeno-canto.org/https://xeno-canto.org/', 'https://xeno-canto.org/', 1)
    return url

def fix_bird_data(input_file, output_file):
    """Fix audio URLs in bird data"""
    print(f"Loading bird data from {input_file}...")

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    fixed_count = 0

    for bird in data.get('birds', []):
        if 'audio' in bird:
            for audio in bird['audio']:
                original_url = audio.get('url', '')
                fixed_url = fix_audio_url(original_url)
                if original_url != fixed_url:
                    audio['url'] = fixed_url
                    fixed_count += 1

    print(f"Fixed {fixed_count} audio URLs")

    print(f"Writing fixed data to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Done!")

if __name__ == '__main__':
    input_file = '../data/act_birds.json'
    output_file = '../data/act_birds.json'

    fix_bird_data(input_file, output_file)
