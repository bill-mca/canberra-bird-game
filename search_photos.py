#!/usr/bin/env python3
"""
Bird Photo Search Script
Searches for photos from Wikimedia Commons, ALA, and iNaturalist
"""

import json
import time
import urllib.request
import urllib.parse
import urllib.error
import ssl

# Create an SSL context that doesn't verify certificates (for testing)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

def fetch_url(url, timeout=30):
    """Fetch URL content with headers"""
    headers = {
        'User-Agent': 'BirdPhotoSearch/1.0 (ACT Bird Game Project; research)',
        'Accept': 'application/json'
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_context) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def search_wikimedia(scientific_name, common_name):
    """Search Wikimedia Commons for bird photos"""
    photos = []

    # Search by scientific name
    search_term = urllib.parse.quote(scientific_name)
    url = f"https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrnamespace=6&gsrsearch={search_term}&gsrlimit=5&prop=imageinfo&iiprop=url|extmetadata&format=json"

    data = fetch_url(url)
    if not data:
        return photos

    try:
        result = json.loads(data)
        if 'query' in result and 'pages' in result['query']:
            for page_id, page in result['query']['pages'].items():
                if 'imageinfo' in page:
                    for info in page['imageinfo']:
                        photo = {
                            'url': info.get('url', ''),
                            'pageUrl': info.get('descriptionurl', ''),
                            'source': 'Wikimedia Commons'
                        }

                        # Extract metadata
                        meta = info.get('extmetadata', {})
                        license_name = meta.get('LicenseShortName', {}).get('value', '')
                        artist = meta.get('Artist', {}).get('value', '')

                        # Clean up artist HTML
                        if '<' in artist:
                            import re
                            artist = re.sub('<[^>]+>', '', artist).strip()

                        photo['licence'] = license_name
                        if artist and license_name not in ['CC0', 'Public domain']:
                            photo['attribution'] = artist

                        # Only include acceptable licenses
                        acceptable = ['CC0', 'CC BY', 'CC BY-SA', 'CC BY-NC', 'CC BY-NC-SA', 'Public domain']
                        if any(lic in license_name for lic in acceptable) and 'ND' not in license_name:
                            photos.append(photo)
    except json.JSONDecodeError as e:
        print(f"JSON error for {scientific_name}: {e}")

    return photos

def search_ala(scientific_name):
    """Search Atlas of Living Australia for bird photos"""
    photos = []

    # First get species GUID
    search_url = f"https://bie.ala.org.au/ws/search?q={urllib.parse.quote(scientific_name)}&fq=idxtype:TAXON"
    data = fetch_url(search_url)

    if not data:
        return photos

    try:
        result = json.loads(data)
        if result.get('searchResults', {}).get('results'):
            taxon = result['searchResults']['results'][0]
            guid = taxon.get('guid', '')

            if guid:
                # Get images for this taxon
                img_url = f"https://images.ala.org.au/ws/search?q=*:*&fq=recognisedLsid:{urllib.parse.quote(guid)}&rows=5"
                img_data = fetch_url(img_url)

                if img_data:
                    img_result = json.loads(img_data)
                    for occ in img_result.get('occurrences', []):
                        license_code = occ.get('license', '')
                        # Map ALA licenses
                        license_map = {
                            'CC BY': 'CC BY 4.0',
                            'CC BY-NC': 'CC BY-NC 4.0',
                            'CC BY-SA': 'CC BY-SA 4.0',
                            'CC0': 'CC0 1.0',
                        }

                        photo = {
                            'url': occ.get('largeImageUrl') or occ.get('imageUrl', ''),
                            'pageUrl': f"https://images.ala.org.au/image/{occ.get('imageId', '')}",
                            'source': 'Atlas of Living Australia',
                            'licence': license_map.get(license_code, license_code)
                        }

                        creator = occ.get('creator') or occ.get('rightsholder', '')
                        if creator:
                            photo['attribution'] = creator

                        if photo['url']:
                            photos.append(photo)
    except (json.JSONDecodeError, KeyError) as e:
        print(f"ALA error for {scientific_name}: {e}")

    return photos

def search_inaturalist(scientific_name):
    """Search iNaturalist for bird photos"""
    photos = []

    # Search for taxon
    search_url = f"https://api.inaturalist.org/v1/taxa?q={urllib.parse.quote(scientific_name)}&rank=species"
    data = fetch_url(search_url)

    if not data:
        return photos

    try:
        result = json.loads(data)
        if result.get('results'):
            taxon = result['results'][0]
            taxon_id = taxon.get('id')

            if taxon_id:
                # Get observations with photos
                obs_url = f"https://api.inaturalist.org/v1/observations?taxon_id={taxon_id}&photos=true&quality_grade=research&per_page=5"
                obs_data = fetch_url(obs_url)

                if obs_data:
                    obs_result = json.loads(obs_data)
                    for obs in obs_result.get('results', []):
                        for photo in obs.get('photos', []):
                            license_code = photo.get('license_code', '')

                            # Map iNaturalist licenses
                            license_map = {
                                'cc-by': 'CC BY 4.0',
                                'cc-by-nc': 'CC BY-NC 4.0',
                                'cc-by-sa': 'CC BY-SA 4.0',
                                'cc-by-nc-sa': 'CC BY-NC-SA 4.0',
                                'cc0': 'CC0 1.0',
                            }

                            if license_code and 'nd' not in license_code.lower():
                                photo_entry = {
                                    'url': photo.get('url', '').replace('square', 'large'),
                                    'pageUrl': f"https://www.inaturalist.org/observations/{obs.get('id')}",
                                    'source': 'iNaturalist',
                                    'licence': license_map.get(license_code, license_code)
                                }

                                attribution = photo.get('attribution', '')
                                if attribution:
                                    photo_entry['attribution'] = attribution

                                if photo_entry['url']:
                                    photos.append(photo_entry)
                                    break  # One photo per observation
    except (json.JSONDecodeError, KeyError) as e:
        print(f"iNaturalist error for {scientific_name}: {e}")

    return photos

def main():
    # Load the bird data
    with open('data/act_birds.json', 'r') as f:
        data = json.load(f)

    birds = data['birds']
    total = len(birds)
    birds_with_photos = 0
    total_photos = 0
    birds_without_photos = []

    print(f"Processing {total} bird species...")

    for i, bird in enumerate(birds):
        scientific_name = bird['scientificName']
        common_name = bird['commonName']

        print(f"[{i+1}/{total}] Searching for {common_name} ({scientific_name})...")

        all_photos = []

        # Try Wikimedia Commons first (preferred)
        photos = search_wikimedia(scientific_name, common_name)
        all_photos.extend(photos)

        # If we don't have enough photos, try ALA
        if len(all_photos) < 2:
            time.sleep(0.2)  # Rate limiting
            photos = search_ala(scientific_name)
            all_photos.extend(photos)

        # If still not enough, try iNaturalist
        if len(all_photos) < 2:
            time.sleep(1)  # iNaturalist rate limit
            photos = search_inaturalist(scientific_name)
            all_photos.extend(photos)

        # Deduplicate by URL and limit to 5 photos
        seen_urls = set()
        unique_photos = []
        for photo in all_photos:
            if photo['url'] not in seen_urls and len(unique_photos) < 5:
                seen_urls.add(photo['url'])
                unique_photos.append(photo)

        bird['photos'] = unique_photos

        if unique_photos:
            birds_with_photos += 1
            total_photos += len(unique_photos)
            print(f"  Found {len(unique_photos)} photos")
        else:
            birds_without_photos.append(common_name)
            print(f"  No photos found - needs manual review")

        # Rate limiting
        time.sleep(0.1)

    # Update statistics
    data['statistics'] = {
        'totalBirds': total,
        'birdsWithPhotos': birds_with_photos,
        'birdsWithoutPhotos': total - birds_with_photos,
        'totalPhotos': total_photos,
        'averagePhotosPerBird': round(total_photos / total, 2) if total > 0 else 0
    }

    # Save updated JSON
    output_file = 'data/act_birds.json'
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"\n=== Summary ===")
    print(f"Total birds: {total}")
    print(f"Birds with photos: {birds_with_photos}")
    print(f"Birds without photos: {total - birds_with_photos}")
    print(f"Total photos: {total_photos}")
    print(f"Average photos per bird: {round(total_photos / total, 2) if total > 0 else 0}")

    # Generate log file
    with open('photo_search_log.txt', 'w') as f:
        f.write(f"Photo Search Log\n")
        f.write(f"================\n")
        f.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Total birds processed: {total}\n")
        f.write(f"Birds with photos: {birds_with_photos}\n")
        f.write(f"Birds without photos: {total - birds_with_photos}\n")
        f.write(f"Total photos found: {total_photos}\n\n")

        if birds_without_photos:
            f.write(f"Species requiring manual review:\n")
            for name in birds_without_photos:
                f.write(f"  - {name}\n")

    print(f"\nResults saved to {output_file}")
    print(f"Log saved to photo_search_log.txt")

if __name__ == '__main__':
    main()
