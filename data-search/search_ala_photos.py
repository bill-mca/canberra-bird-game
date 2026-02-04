#!/usr/bin/env python3
"""
ALA (Atlas of Living Australia) Photo Search Script
Searches for bird photos with appropriate Creative Commons licenses
"""

import json
import time
import urllib.request
import urllib.parse
import urllib.error
import sys
from datetime import datetime

# ALA API configuration
ALA_OCCURRENCE_API = 'https://biocache-ws.ala.org.au/ws/occurrences/search'
ALA_IMAGE_BASE = 'https://images.ala.org.au'

# Rate limiting
REQUEST_DELAY = 2.0  # seconds between requests

# Acceptable licenses (no ND - No Derivatives)
ACCEPTABLE_LICENSES = [
    'CC BY',
    'CC BY-SA',
    'CC BY-NC',
    'CC BY-NC-SA',
    'CC0'
]

def fetch_url(url, params=None, timeout=30):
    """Fetch URL with proper headers"""
    if params:
        url = f"{url}?{urllib.parse.urlencode(params, doseq=True)}"

    headers = {
        'User-Agent': 'Canberra Bird Game/1.0 (educational project)',
        'Accept': 'application/json'
    }

    req = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
        if e.code == 429:
            print("Rate limited! Waiting 10 seconds...")
            time.sleep(10)
        return None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def normalize_license(license_str):
    """Normalize license string to standard format"""
    if not license_str:
        return None

    license_str = license_str.strip()

    # Check if it matches our acceptable licenses
    for acceptable in ACCEPTABLE_LICENSES:
        if acceptable.lower() in license_str.lower():
            # Standardize to version 4.0 for CC licenses
            if license_str.upper().startswith('CC'):
                return f"{acceptable} 4.0"
            return acceptable

    return None

def is_acceptable_license(license_str):
    """Check if license is acceptable"""
    if not license_str:
        return False

    # Reject ND (No Derivatives) licenses
    if 'nd' in license_str.lower():
        return False

    normalized = normalize_license(license_str)
    return normalized is not None

def search_ala_bird_photos(scientific_name, max_results=20, act_only=True):
    """
    Search ALA for bird photos

    Args:
        scientific_name: Scientific name of bird (e.g., "Dromaius novaehollandiae")
        max_results: Maximum number of results to return
        act_only: If True, filter to ACT records only

    Returns:
        List of photo dictionaries matching our data format
    """
    print(f"Searching ALA for: {scientific_name}")

    # Build filter queries
    filters = [
        'multimedia:Image',
        'geospatial_kosher:true',
    ]

    if act_only:
        filters.append('state:"Australian Capital Territory"')

    params = {
        'q': f'scientificName:"{scientific_name}"',
        'fq': filters,
        'pageSize': max_results,
        'startIndex': 0,
        'facets': 'license'
    }

    data = fetch_url(ALA_OCCURRENCE_API, params)

    if not data:
        print(f"  No data returned")
        return []

    occurrences = data.get('occurrences', [])
    print(f"  Found {len(occurrences)} occurrences with images")

    photos = []
    for occ in occurrences:
        # Get image data
        image_url = occ.get('imageUrl') or occ.get('image')
        if not image_url:
            continue

        # Get license info
        license_str = occ.get('license') or occ.get('licence')
        if not is_acceptable_license(license_str):
            continue

        normalized_license = normalize_license(license_str)

        # Get attribution
        creator = occ.get('creator')
        rights_holder = occ.get('rightsHolder')
        attribution = creator or rights_holder or 'Unknown'

        # Build page URL
        record_id = occ.get('uuid')
        page_url = f"https://biocache.ala.org.au/occurrences/{record_id}" if record_id else None

        # Get data resource info
        data_resource = occ.get('dataResourceName', 'Atlas of Living Australia')

        photo_entry = {
            'url': image_url,
            'pageUrl': page_url,
            'source': 'Atlas of Living Australia',
            'licence': normalized_license,
            'attribution': attribution,
            'dataResource': data_resource,
            'recordId': record_id
        }

        photos.append(photo_entry)

    print(f"  Accepted {len(photos)} photos with appropriate licenses")
    return photos

def find_species_needing_photos(bird_data_file, threshold=3):
    """
    Identify species with fewer than threshold photos

    Returns:
        List of (scientific_name, common_name, current_photo_count) tuples
    """
    with open(bird_data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    needs_photos = []

    for bird in data.get('birds', []):
        photo_count = len(bird.get('photos', []))
        if photo_count < threshold:
            needs_photos.append((
                bird['scientificName'],
                bird['commonName'],
                photo_count
            ))

    return sorted(needs_photos, key=lambda x: x[2])  # Sort by photo count

def search_multiple_species(species_list, output_file, max_per_species=10):
    """
    Search for photos for multiple species and save results

    Args:
        species_list: List of (scientific_name, common_name, current_count) tuples
        output_file: File to save results
        max_per_species: Maximum photos to fetch per species
    """
    results = {
        'searchDate': datetime.now().isoformat(),
        'totalSpeciesSearched': len(species_list),
        'species': []
    }

    for i, (scientific_name, common_name, current_count) in enumerate(species_list, 1):
        print(f"\n[{i}/{len(species_list)}] {common_name} ({scientific_name})")
        print(f"  Current photos: {current_count}")

        photos = search_ala_bird_photos(scientific_name, max_results=max_per_species)

        results['species'].append({
            'scientificName': scientific_name,
            'commonName': common_name,
            'currentPhotoCount': current_count,
            'foundPhotos': len(photos),
            'photos': photos
        })

        # Rate limiting
        if i < len(species_list):
            print(f"  Waiting {REQUEST_DELAY}s...")
            time.sleep(REQUEST_DELAY)

    # Save results
    print(f"\nSaving results to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nSearch complete!")
    print(f"Total species searched: {results['totalSpeciesSearched']}")

    species_with_photos = sum(1 for s in results['species'] if s['foundPhotos'] > 0)
    total_photos = sum(s['foundPhotos'] for s in results['species'])

    print(f"Species with photos found: {species_with_photos}")
    print(f"Total photos found: {total_photos}")

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 search_ala_photos.py <bird_data.json> [threshold] [max_per_species]")
        print("\nExample:")
        print("  python3 search_ala_photos.py ../data/act_birds.json 3 10")
        print("\nThis will search for ALA photos for species with fewer than 3 photos")
        sys.exit(1)

    bird_data_file = sys.argv[1]
    threshold = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    max_per_species = int(sys.argv[3]) if len(sys.argv) > 3 else 10

    print(f"Finding species with fewer than {threshold} photos...")
    species_list = find_species_needing_photos(bird_data_file, threshold)

    print(f"\nFound {len(species_list)} species needing more photos:")
    for scientific_name, common_name, count in species_list[:10]:
        print(f"  - {common_name} ({scientific_name}): {count} photos")

    if len(species_list) > 10:
        print(f"  ... and {len(species_list) - 10} more")

    if not species_list:
        print("All species have sufficient photos!")
        return

    # Confirm before proceeding
    print(f"\nThis will search ALA for up to {max_per_species} photos per species")
    print(f"Estimated time: ~{len(species_list) * REQUEST_DELAY / 60:.1f} minutes")

    response = input("\nProceed? (y/n): ")
    if response.lower() != 'y':
        print("Cancelled")
        return

    output_file = f"ala_photos_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    search_multiple_species(species_list, output_file, max_per_species)

    print(f"\nResults saved to: {output_file}")
    print("Review the results before integrating into the main dataset")

if __name__ == '__main__':
    main()
