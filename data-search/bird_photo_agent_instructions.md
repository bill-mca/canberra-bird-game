# AI Agent Instructions: Populating Bird Photo Data

## Objective

You are tasked with finding and adding photo URLs to a JSON file containing 297 bird species from the ACT (Australian Capital Territory). For each bird, you must find between 1 and 5 photos with appropriate licensing and attribution information.

## Input File

**Location:** `act_birds_cog.json`

The JSON contains an array of bird objects under the `birds` key. Each bird has:
- `commonName`: The common English name
- `scientificName`: The binomial scientific name (use this for searches)
- `family`: Taxonomic family
- `statusInACT`: Conservation/residency status
- `photos`: An empty array to be populated

## Output Structure

For each bird, populate the `photos` array with photo objects in this format:

```json
{
  "photos": [
    {
      "url": "https://example.com/direct-image-url.jpg",
      "pageUrl": "https://example.com/page-containing-image",
      "source": "Wikimedia Commons",
      "licence": "CC BY-SA 4.0",
      "attribution": "Photographer Name",
      "description": "Brief description if available"
    }
  ]
}
```

### Field Definitions

| Field | Required | Description |
|-------|----------|-------------|
| `url` | Yes | Direct URL to the image file (must end in .jpg, .jpeg, .png, .gif, or .webp) |
| `pageUrl` | Yes | URL of the page where the image is hosted (for verification/context) |
| `source` | Yes | One of: "Wikimedia Commons", "Atlas of Living Australia", "iNaturalist" |
| `licence` | Yes | The licence type (see Acceptable Licences below) |
| `attribution` | Conditional | Required unless licence is CC0 or Public Domain |
| `description` | No | Optional brief description of the image content |

## Source Priority (in order of preference)

### 1. Wikimedia Commons (Preferred)

**Search Method:**
1. Use the Wikimedia Commons API or search interface
2. Search by scientific name: `"Dromaius novaehollandiae"`
3. Also try common name if scientific name yields few results

**API Endpoint:**
```
https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch={scientific_name}&srnamespace=6&format=json
```

**To get image details:**
```
https://commons.wikimedia.org/w/api.php?action=query&titles=File:{filename}&prop=imageinfo&iiprop=url|extmetadata&format=json
```

**Extracting Data:**
- `url`: Use the direct file URL from `imageinfo.url`
- `pageUrl`: `https://commons.wikimedia.org/wiki/File:{filename}`
- `licence`: Extract from `extmetadata.LicenseShortName`
- `attribution`: Extract from `extmetadata.Artist` (strip HTML tags)

### 2. Atlas of Living Australia (Secondary)

**Search Method:**
1. Use the ALA species search API
2. Search by scientific name to get the species GUID
3. Retrieve images associated with that species

**Species Search:**
```
https://bie.ala.org.au/ws/search?q={scientific_name}&fq=idxtype:TAXON
```

**Image Search:**
```
https://images.ala.org.au/ws/search?q=scientific_name:"{scientific_name}"&fq=recognisedLicence:*
```

**Extracting Data:**
- `url`: Use the `largeImageUrl` or `imageUrl` field
- `pageUrl`: `https://images.ala.org.au/image/{imageId}`
- `licence`: From `recognisedLicence` field
- `attribution`: From `creator` or `rightsholder` field

### 3. iNaturalist (Tertiary)

**Search Method:**
1. Search for taxa by scientific name
2. Get observation photos for that taxon

**Taxa Search:**
```
https://api.inaturalist.org/v1/taxa?q={scientific_name}&rank=species
```

**Observation Photos:**
```
https://api.inaturalist.org/v1/observations?taxon_id={taxon_id}&photos=true&quality_grade=research&per_page=10
```

**Extracting Data:**
- `url`: Use `photos[].url` (replace "square" with "large" in URL)
- `pageUrl`: `https://www.inaturalist.org/observations/{observation_id}`
- `licence`: From `photos[].license_code` (convert to full name)
- `attribution`: From `photos[].attribution`

**iNaturalist Licence Codes:**
| Code | Full Name |
|------|-----------|
| cc-by | CC BY 4.0 |
| cc-by-nc | CC BY-NC 4.0 |
| cc-by-sa | CC BY-SA 4.0 |
| cc-by-nc-sa | CC BY-NC-SA 4.0 |
| cc-by-nd | CC BY-ND 4.0 |
| cc-by-nc-nd | CC BY-NC-ND 4.0 |
| cc0 | CC0 1.0 |

## Acceptable Licences

Only include photos with these licences:

**Preferred (most permissive):**
- CC0 1.0 (Public Domain Dedication)
- Public Domain
- CC BY 4.0 / CC BY 3.0 / CC BY 2.0
- CC BY-SA 4.0 / CC BY-SA 3.0 / CC BY-SA 2.0

**Acceptable (non-commercial):**
- CC BY-NC 4.0 / CC BY-NC 3.0 / CC BY-NC 2.0
- CC BY-NC-SA 4.0 / CC BY-NC-SA 3.0 / CC BY-NC-SA 2.0

**Do NOT include:**
- CC BY-ND (No Derivatives)
- CC BY-NC-ND (No Derivatives)
- All Rights Reserved
- Custom/proprietary licences
- Unknown or unspecified licences

## Processing Instructions

### Step-by-Step Workflow

1. **Load the JSON file** and parse the birds array

2. **For each bird in the array:**

   a. **Search Wikimedia Commons first:**
      - Query using the `scientificName`
      - Filter for images only (namespace 6)
      - Select up to 5 appropriately licenced images
      - Prefer images that show the bird clearly (avoid range maps, diagrams)
   
   b. **If fewer than 5 photos found, search ALA:**
      - Query using scientific name
      - Add photos until you have 5 total (or no more available)
   
   c. **If still fewer than 5 photos, search iNaturalist:**
      - Query using scientific name
      - Filter for research-grade observations
      - Add photos until you have 5 total (or no more available)
   
   d. **If still 0 photos found:**
      - Try searching by common name on all three sources
      - Log the species as requiring manual review

3. **Validate each photo before adding:**
   - Confirm the URL is accessible (returns 200 OK)
   - Verify the licence is on the acceptable list
   - Ensure attribution is captured for non-CC0/PD images

4. **Update the statistics** at the end of the JSON:
   ```json
   "statistics": {
     "totalBirds": 297,
     "birdsWithPhotos": <count>,
     "birdsWithoutPhotos": <count>,
     "totalPhotos": <total across all birds>,
     "averagePhotosPerBird": <calculated average>
   }
   ```

5. **Save the updated JSON** with proper formatting (2-space indent)

### Handling Special Cases

**Hybrids (e.g., "Pacific Black Duck x Domestic Mallard"):**
- Search for the hybrid name first
- If no results, use photos of the primary parent species
- Note in description: "Photo shows parent species: {species name}"

**Subspecies:**
- The scientific name should work directly
- If not, try the species name without subspecies

**Introduced/Domestic species:**
- Search normally by scientific name
- Domestic variants (e.g., "Domestic Mallard") may need common name search

**Extinct species (from ACT):**
- Still search for photos (species exists elsewhere)
- These are only locally extinct

## Quality Guidelines

**Prefer images that:**
- Show the bird clearly and in focus
- Display identifying features
- Are well-lit
- Show the bird in a natural setting
- Have higher resolution

**Avoid images that:**
- Are blurry or poorly exposed
- Show only parts of the bird (unless notable feature)
- Are heavily cropped or edited
- Are illustrations or drawings (unless no photos exist)
- Are range maps or distribution diagrams

## Rate Limiting

Respect API rate limits:
- **Wikimedia Commons:** 200 requests/second (be conservative, use 10/sec)
- **ALA:** No published limit (use 5/sec to be safe)
- **iNaturalist:** 60 requests/minute (1/sec)

Add delays between requests to avoid being blocked.

## Error Handling

- Log any species where no photos were found
- Log any API errors or timeouts
- Continue processing remaining species if one fails
- Generate a summary report at the end listing:
  - Species with 0 photos (need manual review)
  - Species with only 1-2 photos (could use more)
  - Any errors encountered

## Example Output

After processing, a bird entry should look like:

```json
{
  "commonName": "Superb Fairywren",
  "scientificName": "Malurus cyaneus",
  "family": "Maluridae",
  "statusInACT": "Very common, breeding resident",
  "photos": [
    {
      "url": "https://upload.wikimedia.org/wikipedia/commons/9/96/Superb_fairy-wren.jpg",
      "pageUrl": "https://commons.wikimedia.org/wiki/File:Superb_fairy-wren.jpg",
      "source": "Wikimedia Commons",
      "licence": "CC BY-SA 3.0",
      "attribution": "JJ Harrison",
      "description": "Male in breeding plumage"
    },
    {
      "url": "https://upload.wikimedia.org/wikipedia/commons/a/ab/Female_superb_fairy_wren.jpg",
      "pageUrl": "https://commons.wikimedia.org/wiki/File:Female_superb_fairy_wren.jpg",
      "source": "Wikimedia Commons",
      "licence": "CC BY 2.0",
      "attribution": "Patrick K59",
      "description": "Female"
    },
    {
      "url": "https://images.ala.org.au/store/0/1/2/3/example.jpg",
      "pageUrl": "https://images.ala.org.au/image/abc123",
      "source": "Atlas of Living Australia",
      "licence": "CC BY 4.0",
      "attribution": "David Cook",
      "description": null
    }
  ]
}
```

## Verification Checklist

Before marking the task complete, verify:

- [ ] All 297 birds have been processed
- [ ] Each bird has at least 1 photo (or is logged for manual review)
- [ ] All photo URLs are valid and accessible
- [ ] All licences are from the acceptable list
- [ ] Attribution is present for all non-CC0/PD photos
- [ ] Source priority was followed (Wikimedia > ALA > iNaturalist)
- [ ] Statistics section is updated accurately
- [ ] JSON is valid and properly formatted
- [ ] Error/review log is generated for any issues

## Files to Produce

1. **Updated JSON:** `act_birds_cog_with_photos.json`
2. **Processing log:** `photo_search_log.txt` containing:
   - Timestamp of processing
   - Count of photos found per source
   - List of species needing manual review
   - Any errors encountered
