# Audio Search Implementation - Xeno-canto

This document describes how to use the audio search scripts to add bird call and song recordings to the ACT birds dataset.

## Overview

The audio search implementation uses the **Xeno-canto API v3** to find high-quality bird audio recordings. Xeno-canto is a collaborative database of bird sounds from around the world with over 900,000 recordings.

## Features

- Searches by scientific name for accurate species matching
- Filters by **quality ratings** (prefers A and B, rejects D and E)
- Filters by **licenses** (accepts CC BY, CC BY-SA, CC BY-NC, CC BY-NC-SA, CC0)
- **Rejects** CC BY-NC-ND (No Derivatives) licenses
- Targets **5 audio recordings per species**
- Sorts by quality (highest quality first)
- Includes rate limiting (1 second between requests)
- Generates detailed statistics and logs

## Setup Requirements

### 1. Get Xeno-canto API Key

The Xeno-canto API v3 requires an API key (free for registered users):

1. Go to https://xeno-canto.org/account
2. Create an account (free)
3. Verify your email address
4. Log in and navigate to your account page
5. Find and copy your API key

### 2. Set Environment Variable

Set the API key as an environment variable:

```bash
export XENO_CANTO_API_KEY='your_api_key_here'
```

Or add it to your `~/.bashrc` or `~/.zshrc` for persistence:

```bash
echo "export XENO_CANTO_API_KEY='your_api_key_here'" >> ~/.bashrc
source ~/.bashrc
```

## Usage

### Step 1: Test API Connection

Before running the full search, test your API key:

```bash
python3 test_xeno_canto_api.py
```

This will:
- Verify your API key is valid
- Test connectivity to Xeno-canto
- Show sample results for Superb Fairy-wren
- Display quality and license distributions
- Confirm everything is working

**Expected output:**
```
Testing Xeno-canto API v3...
==================================================

Test species: Malurus cyaneus
Making API request...

✅ API connection successful!

Results:
  Total recordings found: 243
  Number of pages: 5
  Recordings in this page: 50

📊 Sample Recording Details:
  [detailed recording info...]

✅ Test completed successfully!
```

### Step 2: Run Audio Search

Once the test passes, run the full audio search:

```bash
python3 search_audio.py
```

This will:
- Process all 297 ACT bird species
- Search Xeno-canto for up to 5 audio recordings per species
- Filter by quality and license
- Update `data/act_birds.json` with audio data
- Generate `audio_search_log.txt` with statistics

**Estimated time:** 5-10 minutes (1 second per species due to rate limiting)

### Step 3: Review Results

Check the log file for results:

```bash
cat audio_search_log.txt
```

The log will show:
- Total species processed
- Number of species with audio
- Number of species without audio
- Total audio recordings found
- List of species needing manual review (if any)

## Audio Data Structure

Each bird in `act_birds.json` will have an `audio` array:

```json
{
  "commonName": "Superb Fairy-wren",
  "scientificName": "Malurus cyaneus",
  "photos": [...],
  "audio": [
    {
      "url": "https://xeno-canto.org/sounds/uploaded/...",
      "pageUrl": "https://xeno-canto.org/123456",
      "source": "Xeno-canto",
      "licence": "CC BY 4.0",
      "attribution": "Recordist Name",
      "quality": "A",
      "type": "song",
      "length": "0:45",
      "recordingId": "123456",
      "description": "Male territorial song"
    }
  ]
}
```

## Quality Ratings

Xeno-canto uses quality ratings A through E:

- **A** - Highest quality (preferred)
- **B** - Good quality (preferred)
- **C** - Fair quality (acceptable)
- **D** - Poor quality (rejected)
- **E** - Lowest quality (rejected)

The script automatically prefers A and B rated recordings and skips D and E.

## Acceptable Licenses

The script accepts these Creative Commons licenses:

✅ **Accepted:**
- CC BY (Attribution)
- CC BY-SA (Attribution-ShareAlike)
- CC BY-NC (Attribution-NonCommercial)
- CC BY-NC-SA (Attribution-NonCommercial-ShareAlike)
- CC0 (Public Domain)

❌ **Rejected:**
- CC BY-NC-ND (No Derivatives - not acceptable)
- CC BY-ND (No Derivatives - not acceptable)

## Rate Limiting

The script implements **1 second delay** between requests to be respectful of the Xeno-canto API. This means:
- 297 species × 1 second = ~5 minutes minimum
- Actual time may be 5-10 minutes with processing

**Note:** According to Xeno-canto's terms of service, the server can't accommodate indiscriminate automated mass downloads. Our implementation:
- Uses reasonable rate limiting (1 req/sec)
- Only downloads metadata (not audio files)
- Limits to 5 recordings per species
- Should be acceptable for research/educational use

If you need to do this frequently or for larger datasets, consider contacting Xeno-canto directly.

## Troubleshooting

### Error: Missing or invalid 'key' parameter

**Problem:** API key not set or invalid

**Solution:**
1. Check that `XENO_CANTO_API_KEY` is set: `echo $XENO_CANTO_API_KEY`
2. Verify the key is correct on your Xeno-canto account page
3. Make sure you've verified your email address

### Error: No audio found for many species

**Problem:** Query might be too strict or API issues

**Solution:**
1. Check the log file to see which species have no audio
2. Manually search a few on xeno-canto.org to verify recordings exist
3. The script already handles scientific name variations
4. Some rare/vagrant species may genuinely have no recordings

### Script runs slowly

**Expected behavior:** The script intentionally runs slowly (1 req/sec) to respect API rate limits. This is by design.

## Files

- `search_audio.py` - Main audio search script
- `test_xeno_canto_api.py` - API connectivity test
- `xeno-canto.md` - Resource documentation
- `audio_search_log.txt` - Generated after running search
- `data/act_birds.json` - Updated with audio data

## Next Steps

After running the audio search:
1. Review the results in `audio_search_log.txt`
2. Check species without audio (if any)
3. Optionally verify audio URLs (Phase 3 in backlog)
4. Commit the updated `act_birds.json` to git

## Resources

- Xeno-canto website: https://xeno-canto.org
- API documentation: https://xeno-canto.org/explore/api
- Account/API key: https://xeno-canto.org/account
