#!/usr/bin/env python3
"""
Bird Audio Search Script - Xeno-canto
Searches for high-quality bird audio recordings from Xeno-canto.org
"""

import json
import time
import urllib.request
import urllib.parse
import urllib.error
import os
import sys

# Xeno-canto API v3 configuration
XENO_CANTO_API_KEY = os.environ.get('XENO_CANTO_API_KEY', '')
XENO_CANTO_API_URL = 'https://xeno-canto.org/api/3/recordings'

# Acceptable licenses (no ND - No Derivatives)
# Note: Xeno-canto URLs use format "/by-nc-sa/" not "cc-by-nc-sa"
ACCEPTABLE_LICENSES = [
    '/by/',
    '/by-sa/',
    '/by-nc/',
    '/by-nc-sa/',
    '/cc0/'
]

# Quality preference order (A is best)
QUALITY_PREFERENCE = ['A', 'B', 'C']


def fetch_url(url, timeout=30):
    """Fetch URL content with headers"""
    headers = {
        'User-Agent': 'ACT Bird Game Audio Search/1.0 (research project)',
        'Accept': 'application/json'
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def normalize_license(license_url):
    """Convert license URL to standard format"""
    license_lower = license_url.lower()

    # Map URL patterns to standard license names
    # Xeno-canto uses format: //creativecommons.org/licenses/by-nc-sa/4.0/
    if '/by-nc-sa/' in license_lower:
        return 'CC BY-NC-SA 4.0'
    elif '/by-nc-nd/' in license_lower:
        return 'CC BY-NC-ND 4.0'
    elif '/by-sa/' in license_lower:
        return 'CC BY-SA 4.0'
    elif '/by-nd/' in license_lower:
        return 'CC BY-ND 4.0'
    elif '/by-nc/' in license_lower:
        return 'CC BY-NC 4.0'
    elif '/by/' in license_lower and '/by-' not in license_lower:
        return 'CC BY 4.0'
    elif '/cc0/' in license_lower or 'cc0' in license_lower:
        return 'CC0 1.0'

    # Return original if we can't parse it
    return license_url


def is_acceptable_license(license_url):
    """Check if license is acceptable (no ND licenses)"""
    license_lower = license_url.lower()

    # Reject ND (No Derivatives) licenses
    if 'nd' in license_lower:
        return False

    # Check if it's one of our acceptable licenses
    return any(lic in license_lower for lic in ACCEPTABLE_LICENSES)


def search_xeno_canto(scientific_name, max_audio=5):
    """
    Search Xeno-canto for bird audio recordings.

    Args:
        scientific_name: Scientific name of the bird species
        max_audio: Maximum number of audio recordings to return

    Returns:
        List of audio objects with metadata
    """
    if not XENO_CANTO_API_KEY:
        print("ERROR: XENO_CANTO_API_KEY environment variable not set!")
        print("Get your API key from: https://xeno-canto.org/account")
        return []

    audio_list = []

    # Build query: search by species, prefer high quality
    # Use quoted scientific name for exact match
    query = f'sp:"{scientific_name}"'

    # URL encode the query
    params = {
        'query': query,
        'key': XENO_CANTO_API_KEY
    }

    url = f"{XENO_CANTO_API_URL}?{urllib.parse.urlencode(params)}"

    data = fetch_url(url)
    if not data:
        return audio_list

    try:
        result = json.loads(data)

        # Check for errors
        if 'error' in result:
            print(f"  API Error: {result.get('message', 'Unknown error')}")
            return audio_list

        recordings = result.get('recordings', [])

        if not recordings:
            return audio_list

        # Sort by quality (A > B > C > D > E)
        def quality_score(rec):
            quality = rec.get('q', 'E')
            if quality == 'A':
                return 5
            elif quality == 'B':
                return 4
            elif quality == 'C':
                return 3
            elif quality == 'D':
                return 2
            elif quality == 'E':
                return 1
            else:
                return 0

        # Sort by quality (highest first)
        recordings_sorted = sorted(recordings, key=quality_score, reverse=True)

        # Process recordings
        for rec in recordings_sorted:
            # Check license
            license_url = rec.get('lic', '')
            if not is_acceptable_license(license_url):
                continue

            # Skip if quality is too low (D or E)
            quality = rec.get('q', 'no score')
            if quality in ['D', 'E']:
                continue

            # Get recording details
            recording_id = rec.get('id', '')
            file_name = rec.get('file-name', '')

            # Construct URLs
            # Audio file URL format: https://xeno-canto.org/sounds/uploaded/...
            audio_url = f"https://xeno-canto.org/{rec.get('file', '')}"
            page_url = f"https://xeno-canto.org/{recording_id}"

            audio_entry = {
                'url': audio_url,
                'pageUrl': page_url,
                'source': 'Xeno-canto',
                'licence': normalize_license(license_url),
                'quality': quality,
                'type': rec.get('type', 'unknown'),
                'length': rec.get('length', 'unknown'),
                'recordingId': recording_id
            }

            # Add attribution (recordist name)
            recordist = rec.get('rec', '')
            if recordist and 'cc0' not in license_url.lower():
                audio_entry['attribution'] = recordist

            # Add optional description from remarks if useful
            remarks = rec.get('rmk', '').strip()
            if remarks and len(remarks) < 200:  # Only short remarks
                audio_entry['description'] = remarks

            audio_list.append(audio_entry)

            # Stop when we have enough
            if len(audio_list) >= max_audio:
                break

    except (json.JSONDecodeError, KeyError) as e:
        print(f"  Error parsing Xeno-canto data: {e}")

    return audio_list


def main():
    """Main processing function"""
    # Check for API key
    if not XENO_CANTO_API_KEY:
        print("ERROR: XENO_CANTO_API_KEY environment variable not set!")
        print("\nTo get your API key:")
        print("1. Register at https://xeno-canto.org/account")
        print("2. Verify your email")
        print("3. Get your API key from your account page")
        print("4. Set the environment variable:")
        print("   export XENO_CANTO_API_KEY='your_key_here'")
        print("\nOr run with: XENO_CANTO_API_KEY='your_key' python3 search_audio.py")
        sys.exit(1)

    # Load the bird data
    with open('data/act_birds.json', 'r') as f:
        data = json.load(f)

    birds = data['birds']
    total = len(birds)
    birds_with_audio = 0
    total_audio = 0
    birds_without_audio = []

    print(f"Processing {total} bird species for audio recordings...")
    print(f"Using Xeno-canto API v3")
    print(f"Target: Up to 5 audio recordings per species")
    print()

    for i, bird in enumerate(birds):
        scientific_name = bird['scientificName']
        common_name = bird['commonName']

        print(f"[{i+1}/{total}] Searching for {common_name} ({scientific_name})...")

        # Search Xeno-canto
        audio = search_xeno_canto(scientific_name, max_audio=5)

        # Store audio recordings
        bird['audio'] = audio

        if audio:
            birds_with_audio += 1
            total_audio += len(audio)
            print(f"  Found {len(audio)} audio recording(s)")
            # Show quality distribution
            qualities = {}
            for a in audio:
                q = a.get('quality', 'unknown')
                qualities[q] = qualities.get(q, 0) + 1
            quality_str = ', '.join([f"{q}: {count}" for q, count in sorted(qualities.items())])
            print(f"  Quality: {quality_str}")
        else:
            birds_without_audio.append(common_name)
            print(f"  No audio found")

        # Rate limiting - be respectful of Xeno-canto API
        # Recommended: ~1 request per second
        time.sleep(1.0)

    # Update statistics
    if 'statistics' not in data:
        data['statistics'] = {}

    data['statistics'].update({
        'birdsWithAudio': birds_with_audio,
        'birdsWithoutAudio': total - birds_with_audio,
        'totalAudio': total_audio,
        'averageAudioPerBird': round(total_audio / total, 2) if total > 0 else 0
    })

    # Save updated JSON
    output_file = 'data/act_birds.json'
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"\n=== Summary ===")
    print(f"Total birds: {total}")
    print(f"Birds with audio: {birds_with_audio}")
    print(f"Birds without audio: {total - birds_with_audio}")
    print(f"Total audio recordings: {total_audio}")
    print(f"Average audio per bird: {round(total_audio / total, 2) if total > 0 else 0}")

    # Generate log file
    with open('audio_search_log.txt', 'w') as f:
        f.write(f"Audio Search Log - Xeno-canto\n")
        f.write(f"===============================\n")
        f.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Total birds processed: {total}\n")
        f.write(f"Birds with audio: {birds_with_audio}\n")
        f.write(f"Birds without audio: {total - birds_with_audio}\n")
        f.write(f"Total audio recordings: {total_audio}\n")
        f.write(f"Average audio per bird: {round(total_audio / total, 2) if total > 0 else 0}\n\n")

        if birds_without_audio:
            f.write(f"Species without audio ({len(birds_without_audio)}):\n")
            for name in birds_without_audio:
                f.write(f"  - {name}\n")

    print(f"\nResults saved to {output_file}")
    print(f"Log saved to audio_search_log.txt")

    if birds_without_audio:
        print(f"\n{len(birds_without_audio)} species need manual review - see audio_search_log.txt")


if __name__ == '__main__':
    main()
