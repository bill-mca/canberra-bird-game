#!/usr/bin/env python3
"""
Add genus field to bird data by extracting from scientific name
"""

import json

def extract_genus(scientific_name):
    """Extract genus (first word) from scientific name"""
    return scientific_name.split()[0] if scientific_name else ''

def add_genus_fields(input_file, output_file):
    """Add genus field to all birds"""
    print(f"Loading bird data from {input_file}...")

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for bird in data.get('birds', []):
        scientific_name = bird.get('scientificName', '')
        genus = extract_genus(scientific_name)
        bird['genus'] = genus

    print(f"Added genus field to {len(data.get('birds', []))} birds")

    print(f"Writing updated data to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Done!")

if __name__ == '__main__':
    input_file = '../data/act_birds.json'
    output_file = '../data/act_birds.json'

    add_genus_fields(input_file, output_file)
