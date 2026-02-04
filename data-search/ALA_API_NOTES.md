# Atlas of Living Australia (ALA) / GALAH API Notes

## Overview

The Atlas of Living Australia provides biodiversity data through their API and the GALAH R package (Python wrapper available).

## API Access

### Base URLs
- **Main API**: `https://biocache-ws.ala.org.au/ws/`
- **Species API**: `https://bie-ws.ala.org.au/ws/species/`
- **Image Service**: `https://images.ala.org.au/`

### Authentication
- No API key required for basic public queries
- Rate limiting: Please implement delays between requests (1-2 seconds recommended)
- User-Agent header should identify your application

## Searching for Bird Photos

### Method 1: Occurrences Search with Images

Search for occurrence records that have images:

```
GET https://biocache-ws.ala.org.au/ws/occurrences/search

Parameters:
- q: scientificName:"Genus species"
- fq: multimedia:"Image"
- fq: geospatial_kosher:true
- fq: state:"Australian Capital Territory"
- pageSize: 20
- startIndex: 0
```

Example:
```
https://biocache-ws.ala.org.au/ws/occurrences/search?q=scientificName:"Dromaius novaehollandiae"&fq=multimedia:Image&fq=geospatial_kosher:true&fq=state:"Australian Capital Territory"&pageSize=20
```

### Method 2: Direct Image Search

```
GET https://images.ala.org.au/ws/search

Parameters:
- q: scientificName:"Genus species"
- fq: recognisedLicence:CC*
- rows: 20
- start: 0
```

### Response Format

Occurrence records include:
- `image`: Image ID or URL
- `imageUrl`: Direct link to image
- `thumbnail`: Thumbnail URL
- `dataResourceName`: Source of the record
- `license`: License type
- `rightsHolder`: Copyright holder
- `creator`: Photographer/observer name

Image records include:
- `imageIdentifier`: Unique ID
- `imageUrl`: Full-size image URL
- `thumbUrl`: Thumbnail URL
- `largeThumbUrl`: Larger thumbnail
- `squareThumbUrl`: Square thumbnail
- `tileZoomLevels`: Available zoom levels
- `creator`: Photographer
- `rights`: Rights statement
- `licence`: License type (e.g., "CC BY 4.0")
- `dateTaken`: When photo was taken
- `recognisedLicence`: Standardized license

## License Filtering

Acceptable Creative Commons licenses:
- CC BY
- CC BY-SA
- CC BY-NC
- CC BY-NC-SA
- CC0

**Exclude**:
- CC BY-ND (No Derivatives)
- CC BY-NC-ND (No Derivatives)
- All Rights Reserved
- Copyright

Filter query: `fq=recognisedLicence:CC*`

## Image URLs

ALA images are hosted on: `https://images.ala.org.au/`

URL patterns:
- Original: `https://images.ala.org.au/image/{imageId}`
- Thumbnail: `https://images.ala.org.au/image/thumbnail?id={imageId}`
- Large: `https://images.ala.org.au/image/proxyImageThumbnailLarge?imageId={imageId}`

## Best Practices

1. **Rate Limiting**:
   - Add 1-2 second delays between requests
   - Batch requests where possible

2. **User-Agent**:
   ```python
   headers = {
       'User-Agent': 'Canberra Bird Game/1.0 (educational project; contact@example.com)'
   }
   ```

3. **Error Handling**:
   - Handle 429 (Too Many Requests)
   - Handle 503 (Service Unavailable)
   - Implement retry logic with exponential backoff

4. **Data Quality**:
   - Use `fq=geospatial_kosher:true` to exclude records with data quality issues
   - Check license field is not empty
   - Verify image URLs are accessible

## Species with Few Photos (Need ALA Sourcing)

After analysis of act_birds.json, the following species have fewer than 3 photos and could benefit from ALA sourcing:

- Species with 1-2 photos (need verification of actual counts)
- Focus on species with no Wikimedia Commons presence
- Prioritize rare and vagrant species

## Python Example Code

```python
import requests
import time

def search_ala_images(scientific_name, max_results=10):
    """Search ALA for bird images with appropriate licenses"""
    base_url = "https://biocache-ws.ala.org.au/ws/occurrences/search"

    params = {
        'q': f'scientificName:"{scientific_name}"',
        'fq': [
            'multimedia:Image',
            'geospatial_kosher:true',
            'state:"Australian Capital Territory"',
            'recognisedLicence:CC*'
        ],
        'pageSize': max_results,
        'startIndex': 0
    }

    headers = {
        'User-Agent': 'Canberra Bird Game/1.0 (educational project)'
    }

    try:
        response = requests.get(base_url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()

        occurrences = data.get('occurrences', [])
        images = []

        for occ in occurrences:
            if occ.get('image'):
                images.append({
                    'url': occ.get('imageUrl') or occ.get('image'),
                    'thumbnail': occ.get('thumbnail'),
                    'source': 'Atlas of Living Australia',
                    'licence': occ.get('license', 'Unknown'),
                    'attribution': occ.get('creator') or occ.get('rightsHolder'),
                    'dataResource': occ.get('dataResourceName'),
                    'recordId': occ.get('uuid')
                })

        return images

    except requests.exceptions.RequestException as e:
        print(f"Error searching ALA: {e}")
        return []

# Example usage
images = search_ala_images("Dromaius novaehollandiae")
time.sleep(2)  # Rate limiting
```

## Known Limitations

1. **Image Quality**: Variable quality, not all images are high-resolution
2. **Geographic Filtering**: ACT-specific filtering may miss some records
3. **License Inconsistency**: Some records have incomplete license information
4. **Availability**: Image URLs may change or become unavailable over time
5. **Attribution**: Creator/attribution information may be incomplete

## Next Steps for Implementation

1. Create `search_ala_photos.py` script based on above code
2. Identify species with <3 photos in current dataset
3. Test API with sample species
4. Implement error handling and retry logic
5. Add rate limiting (1-2s between requests)
6. Format output to match existing photo data structure
7. Generate report of found images for human review
8. Do NOT automatically add to dataset - create a separate file for review

## Resources

- ALA API Documentation: https://api.ala.org.au/
- ALA Images API: https://images.ala.org.au/
- BioCache Web Services: https://biocache-ws.ala.org.au/
- GALAH Package: https://galah.ala.org.au/
- Creative Commons Licenses: https://creativecommons.org/licenses/
