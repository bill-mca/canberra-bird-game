# ALA Photo Search Script - Testing Guide

## Overview

This guide documents how to test the `search_ala_photos.py` script before using it in production.

## Prerequisites

- Python 3.6+
- Internet connection
- `../data/act_birds.json` file

## Test Plan

### Test 1: Help and Usage

**Purpose**: Verify help message displays correctly

```bash
python3 search_ala_photos.py
```

**Expected Output**:
- Usage information
- Example command
- Exit code 1

**Status**: ✓ Tested (script structure verified)

---

### Test 2: Species Identification

**Purpose**: Verify script correctly identifies species needing photos

```bash
# Dry run - just identify species
python3 search_ala_photos.py ../data/act_birds.json 3 10
# Then answer 'n' when prompted
```

**Expected Output**:
- List of species with <3 photos
- Count of how many species found
- Estimated search time
- Prompt for confirmation

**What to Check**:
- Species names are correct
- Photo counts match actual data
- All species listed have genuinely few photos

**Status**: ⏳ Pending - Requires manual testing

---

### Test 3: Single Species Search (Manual)

**Purpose**: Test API search with a known common species

Create a test script `test_single_species.py`:

```python
#!/usr/bin/env python3
from search_ala_photos import search_ala_bird_photos
import json

# Test with a common ACT bird
result = search_ala_bird_photos("Corvus coronoides", max_results=5, act_only=True)

print(json.dumps(result, indent=2))
print(f"\nFound {len(result)} photos")

# Verify:
# 1. Photos have valid URLs
# 2. Licenses are CC-compatible
# 3. Attribution is present
# 4. Page URLs are valid
```

**Expected Output**:
- 0-5 photos for Australian Raven
- All photos have valid URLs
- All licenses are CC BY, CC BY-SA, CC BY-NC, or CC BY-NC-SA
- Attribution is populated

**What to Check**:
1. **URL Validity**: All `url` fields contain valid image URLs
2. **License Format**: Licenses match expected format (e.g., "CC BY 4.0")
3. **Attribution**: Creator or rights holder is captured
4. **Page URLs**: Links go to ALA occurrence records
5. **No ND Licenses**: No "ND" (No Derivatives) licenses present

**Status**: ⏳ Pending - Requires API access

---

### Test 4: Species with No Results

**Purpose**: Test behavior when no photos found

Test species that might not have ACT records with images:
- Rare vagrants
- Recently added species
- Species with poor photo coverage

**Expected Behavior**:
- Script handles empty results gracefully
- No crashes or errors
- Logs "0 photos" for that species

**Status**: ⏳ Pending

---

### Test 5: License Filtering

**Purpose**: Verify ND licenses are excluded

**Test Cases**:
1. Search should exclude CC BY-ND
2. Search should exclude CC BY-NC-ND
3. Search should accept CC BY
4. Search should accept CC BY-SA
5. Search should accept CC BY-NC
6. Search should accept CC BY-NC-SA
7. Search should accept CC0

**Verification**:
Check the `normalize_license()` and `is_acceptable_license()` functions in the script:

```python
# Test cases
test_licenses = [
    ("CC BY-ND 4.0", False),  # Should reject
    ("CC BY-NC-ND 4.0", False),  # Should reject
    ("CC BY 4.0", True),  # Should accept
    ("CC BY-SA 4.0", True),  # Should accept
    ("CC BY-NC 4.0", True),  # Should accept
    ("CC BY-NC-SA 4.0", True),  # Should accept
    ("CC0 1.0", True),  # Should accept
]

for license_str, should_accept in test_licenses:
    result = is_acceptable_license(license_str)
    status = "✓" if result == should_accept else "✗"
    print(f"{status} {license_str}: {result} (expected {should_accept})")
```

**Status**: ⏳ Pending

---

### Test 6: Rate Limiting

**Purpose**: Verify rate limiting works

**Test**: Search for 3-5 species and monitor timing

```bash
# Search only 3 species to avoid excessive API calls
python3 search_ala_photos.py ../data/act_birds.json 1 5
# Answer 'y' when prompted
```

**What to Check**:
- Delay of ~2 seconds between requests
- No 429 (Too Many Requests) errors
- Script completes successfully

**Status**: ⏳ Pending

---

### Test 7: Error Handling

**Purpose**: Verify error handling for network issues

**Test Cases**:
1. **Network Timeout**: Temporarily disconnect network mid-search
2. **Invalid Species**: Search for species not in ALA
3. **API Errors**: Test behavior with API errors

**Expected Behavior**:
- Script doesn't crash
- Errors are logged clearly
- Continues with next species on errors

**Status**: ⏳ Pending

---

### Test 8: Output Format

**Purpose**: Verify JSON output matches expected format

**After Running**: Check output file structure

```bash
python3 search_ala_photos.py ../data/act_birds.json 2 5
```

**Verify Output JSON**:
```json
{
  "searchDate": "2026-02-04T...",
  "totalSpeciesSearched": 5,
  "species": [
    {
      "scientificName": "...",
      "commonName": "...",
      "currentPhotoCount": 2,
      "foundPhotos": 3,
      "photos": [
        {
          "url": "https://...",
          "pageUrl": "https://...",
          "source": "Atlas of Living Australia",
          "licence": "CC BY 4.0",
          "attribution": "...",
          "dataResource": "...",
          "recordId": "..."
        }
      ]
    }
  ]
}
```

**What to Check**:
- Valid JSON structure
- All required fields present
- Photo format matches existing `act_birds.json` structure
- URLs are accessible

**Status**: ⏳ Pending

---

### Test 9: Integration Test

**Purpose**: Verify photos can be integrated into main dataset

**Steps**:
1. Run script for 1-2 species
2. Manually verify photo quality and appropriateness
3. Test adding photos to a copy of `act_birds.json`
4. Verify app still loads and displays correctly

**What to Check**:
- Photos load in the app
- Attribution displays correctly
- Licenses are correct
- No broken image links

**Status**: ⏳ Pending

---

### Test 10: Full Dataset Run (Dry Run)

**Purpose**: Estimate full run characteristics

```bash
# Just identify, don't search
python3 search_ala_photos.py ../data/act_birds.json 3 10
# Answer 'n'
```

**Document**:
- How many species need photos
- Estimated total time for full search
- Expected number of API calls

**Status**: ⏳ Pending

---

## Known Issues & Limitations

### Identified During Development

1. **ACT Geographic Filtering**: May miss some valid records
   - Some records may not have ACT tagged correctly
   - Consider searching without `act_only=True` for comprehensive results

2. **Image Quality**: Variable quality
   - ALA includes citizen science observations
   - Not all images are high-resolution
   - Manual review recommended

3. **License Data**: Inconsistent
   - Some records have incomplete license information
   - Script filters conservatively (rejects if uncertain)

4. **URL Stability**: URLs may change
   - ALA image URLs may become unavailable over time
   - Recommend periodic verification

### To Be Discovered

- API rate limits (unknown exact threshold)
- Optimal REQUEST_DELAY value
- Average photos per species
- Image availability for rare species

---

## Testing Results (To Be Completed)

### Test Run: [Date]

**Configuration**:
- Threshold: [X]
- Max per species: [Y]
- Species searched: [Z]

**Results**:
- Species with photos found: [A]
- Total photos found: [B]
- Errors encountered: [C]
- Time taken: [D] minutes

**Issues**:
- [List any issues]

**Photos Reviewed**: [Yes/No]
- Quality acceptable: [Yes/No]
- Licenses correct: [Yes/No]
- Attribution complete: [Yes/No]

**Recommendation**: [Proceed/Modify/Abandon]

---

## Recommendations for Production Use

1. **Start Small**: Test with 5-10 species first
2. **Manual Review**: Always review photos before integrating
3. **Verify URLs**: Check that URLs are accessible
4. **Quality Check**: Ensure photos are appropriate for bird ID
5. **License Verify**: Double-check licenses are correctly captured
6. **Attribution**: Verify photographer attribution is complete
7. **Backup**: Backup `act_birds.json` before integrating new photos

## Next Steps

1. ✓ Script created
2. ⏳ Run Test 1-3 (basic functionality)
3. ⏳ Run Test 4-7 (edge cases)
4. ⏳ Run Test 8-9 (output and integration)
5. ⏳ Document results
6. ⏳ Create sample output for review
7. ⏳ Get user approval for full dataset run

## Contact

For questions or issues with testing, document them in the testing results section above.
