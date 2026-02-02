I'll search for information about the Xeno-canto API, licensing, and recording quality.Based on my research, here's what I've found about Xeno-canto API access, licensing, and quality:

## API Access

**Yes, Xeno-canto has a fully functional API.** The main endpoint is:
- `https://xeno-canto.org/api/2/recordings?query=[your_query]`

There are multiple Python wrappers available (xeno-canto-py, XenoPy, pyxctools) and Node.js libraries as well. The API supports comprehensive search parameters including species names, quality ratings, countries, recording types, and more.

**Note:** According to their terms of service, the Xeno-canto server can't accommodate indiscriminate automated mass downloads. For large-scale data retrieval, you'd need to contact them directly to request a data dump or work out a suitable arrangement.

## Licensing

**All recordings use Creative Commons licences** - this is excellent news for reuse. However, individual recordings may use different CC licence versions (not all the same), including:
- CC BY (Attribution)
- CC BY-NC (Attribution-NonCommercial) 
- CC BY-NC-ND (Attribution-NonCommercial-NoDerivatives)
- Others

The API returns the licence URL for each recording in the metadata (in the `lic` field), so you can filter based on your needs.

## Quality Ratings

Xeno-canto uses a **quality rating system from A to E**, plus unrated recordings (0):
- **A** = highest quality
- **B** = good quality
- **C** = fair quality  
- **D** = poor quality
- **E** = lowest quality

You can filter via API using parameters like:
- `q:A` - only A-rated recordings
- `q_gt:C` - quality greater than C (returns B and A)
- `q_lt:C` - quality less than C (returns D and E)

## Single Species Recordings

Here's the challenge: Xeno-canto recordings are **"weakly labelled"** - meaning they're tagged with a species name but may contain:
- Background birds of other species
- Environmental noise
- Multiple individuals

Research papers note this is a known limitation. However, you can improve your chances of getting single-species recordings by:
1. Filtering for **high quality ratings (A or B)** - these typically have better signal-to-noise ratios
2. Looking at the **'type' field** - recordings labelled as 'song' tend to be more focused than soundscapes
3. Checking the **remarks field** (`rmk`) - recordists often note background species
4. Some recordists are more meticulous than others about focal recordings

The scikit-maad library has examples of automatically segmenting and filtering Xeno-canto recordings to extract clean bird vocalisations if you need to process them further.
