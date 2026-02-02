#!/usr/bin/env python3
"""
Test script for Xeno-canto API v3
Tests API connectivity and response format with a single species
"""

import json
import os
import sys
import urllib.request
import urllib.parse

# Get API key from environment
XENO_CANTO_API_KEY = os.environ.get('XENO_CANTO_API_KEY', '')

def test_api():
    """Test Xeno-canto API with a well-known species"""

    if not XENO_CANTO_API_KEY:
        print("ERROR: XENO_CANTO_API_KEY environment variable not set!")
        print("\nTo get your API key:")
        print("1. Register at https://xeno-canto.org/account")
        print("2. Verify your email")
        print("3. Get your API key from your account page")
        print("4. Run this test with:")
        print("   export XENO_CANTO_API_KEY='your_key_here'")
        print("   python3 test_xeno_canto_api.py")
        sys.exit(1)

    print("Testing Xeno-canto API v3...")
    print("=" * 50)

    # Test with Superb Fairy-wren (should have many recordings)
    test_species = "Malurus cyaneus"
    print(f"\nTest species: {test_species}")

    # Build query
    query = f'sp:"{test_species}"'
    params = {
        'query': query,
        'key': XENO_CANTO_API_KEY
    }

    url = f"https://xeno-canto.org/api/3/recordings?{urllib.parse.urlencode(params)}"

    try:
        # Make request
        headers = {
            'User-Agent': 'XenoCanto API Test/1.0',
            'Accept': 'application/json'
        }
        req = urllib.request.Request(url, headers=headers)

        print(f"Making API request...")
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read().decode('utf-8')
            result = json.loads(data)

            # Check for errors
            if 'error' in result:
                print(f"\n❌ API Error: {result.get('message', 'Unknown error')}")
                return False

            # Display results
            num_recordings = result.get('numRecordings', 0)
            num_pages = result.get('numPages', 0)
            recordings = result.get('recordings', [])

            print(f"\n✅ API connection successful!")
            print(f"\nResults:")
            print(f"  Total recordings found: {num_recordings}")
            print(f"  Number of pages: {num_pages}")
            print(f"  Recordings in this page: {len(recordings)}")

            if recordings:
                print(f"\n📊 Sample Recording Details:")
                rec = recordings[0]
                print(f"  Recording ID: {rec.get('id')}")
                print(f"  Species: {rec.get('en', 'N/A')} ({rec.get('gen')} {rec.get('sp')})")
                print(f"  Recordist: {rec.get('rec', 'N/A')}")
                print(f"  Country: {rec.get('cnt', 'N/A')}")
                print(f"  Location: {rec.get('loc', 'N/A')}")
                print(f"  Quality: {rec.get('q', 'N/A')}")
                print(f"  Type: {rec.get('type', 'N/A')}")
                print(f"  Length: {rec.get('length', 'N/A')}")
                print(f"  License: {rec.get('lic', 'N/A')}")
                print(f"  Audio URL: {rec.get('file', 'N/A')}")
                print(f"  Page URL: https://xeno-canto.org/{rec.get('id')}")

                # Show quality distribution
                print(f"\n📈 Quality Distribution (first 50 results):")
                qualities = {}
                for r in recordings[:50]:
                    q = r.get('q', 'no score')
                    qualities[q] = qualities.get(q, 0) + 1

                for quality in ['A', 'B', 'C', 'D', 'E', 'no score']:
                    count = qualities.get(quality, 0)
                    if count > 0:
                        print(f"  {quality}: {count} recordings")

                # Show license distribution
                print(f"\n📜 License Distribution (first 50 results):")
                licenses = {}
                for r in recordings[:50]:
                    lic = r.get('lic', 'Unknown')
                    # Normalize license name
                    if 'by-nc-sa' in lic.lower():
                        lic_short = 'CC BY-NC-SA'
                    elif 'by-nc-nd' in lic.lower():
                        lic_short = 'CC BY-NC-ND'
                    elif 'by-nc' in lic.lower():
                        lic_short = 'CC BY-NC'
                    elif 'by-sa' in lic.lower():
                        lic_short = 'CC BY-SA'
                    elif 'by-nd' in lic.lower():
                        lic_short = 'CC BY-ND'
                    elif 'by' in lic.lower() and 'nc' not in lic.lower():
                        lic_short = 'CC BY'
                    elif 'cc0' in lic.lower():
                        lic_short = 'CC0'
                    else:
                        lic_short = 'Other'

                    licenses[lic_short] = licenses.get(lic_short, 0) + 1

                for lic, count in sorted(licenses.items(), key=lambda x: x[1], reverse=True):
                    acceptable = "✅" if lic in ['CC BY', 'CC BY-SA', 'CC BY-NC', 'CC BY-NC-SA', 'CC0'] else "❌"
                    print(f"  {acceptable} {lic}: {count} recordings")

            print("\n" + "=" * 50)
            print("✅ Test completed successfully!")
            print("\nYou can now run: python3 search_audio.py")

            return True

    except urllib.error.HTTPError as e:
        print(f"\n❌ HTTP Error: {e.code} - {e.reason}")
        print(f"Response: {e.read().decode('utf-8')}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


if __name__ == '__main__':
    success = test_api()
    sys.exit(0 if success else 1)
