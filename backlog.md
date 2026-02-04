# Canberra Bird Game - Backlog

Tasks for autonomous development session based on user feedback.

## Easy Fixes

### 1. Remove bird emoji from title ✅
- [x] Remove the 🦜 emoji from the app title in App.vue
- The macaw parrot is not appropriate for Canberra birds

### 2. Remove generic attribution footer ✅
- [x] Remove the blanket attribution text from app footer
- Individual photos already have proper attribution in expandable sections

### 3. Make bird photos clickable ✅
- [x] In ResultsScreen.vue, make thumbnail photos clickable
- Clicking now opens the image's source page URL in a new tab

### 4. Remove stats box from main menu ✅
- [x] Hide the "Your Stats" box from MainMenu.vue
- Stats are still accessible via the dedicated stats page

### 5. Add About page link to main menu ✅
- [x] Add a navigation link to an About page in MainMenu.vue

### 6. Create placeholder About page ✅
- [x] Create a new AboutPage.vue in src/views/
- [x] Add simple placeholder content explaining the game
- [x] Include a note that contact/detailed info will be added later
- [x] Wire up navigation in App.vue

### 7. Remove progress summary from statistics page ✅
- [x] Hide or remove the progress summary section from StatsPage.vue

## Significant Changes

### 8. Simplify scoring system ✅
- [x] Remove complex point-based scoring system
- [x] Just track correct/incorrect answers
- [x] Update scoring.js to remove multipliers and rarity-based points
- [x] Update all game views to use simplified scoring
- [x] Update stats tracking in storage.js
- [x] Simplify results display (no point breakdowns)

### 9. Debug audio playback ✅
- [x] Investigate why audio recordings are not playing
- [x] Fix duplicate xeno-canto.org URL prefixes in audio data (1,262 URLs fixed)
- [x] Update search_audio.py to prevent future duplicate prefixes
- [x] Audio should now play correctly

### 10. Improve difficulty with taxonomic filtering ✅
- [x] Modify multiple choice option selection to use taxonomic similarity
- [x] For Advanced difficulty: prefer options from same genus, fall back to family, then random
- [x] For Intermediate difficulty: prefer options from same family, fall back to random
- [x] For Beginner difficulty: keep current random selection
- [x] Add genus field to bird data (extracted from scientific name for all 297 species)
- [x] Update birdData.js with new filtering functions
- [x] All difficulties tested and working correctly

### 11. Optimize image loading with smaller sizes ✅
- [x] Update photo URLs to use Wikimedia thumbnail API (1,435 photos optimized)
- [x] Use format: `/thumb/[path]/[width]px-[filename]`
- [x] Main images: 960px, thumbnails: 330px
- [x] Only affects Wikimedia Commons URLs, other sources preserved as-is

## Data Collection & Review Tools

### 12. Create photo review tool ✅
- [x] Create a standalone HTML tool (`data-search/photo-review-tool.html`)
- [x] Load bird data from `act_birds.json`
- [x] Display all bird photos in a scrollable grid of thumbnails
- [x] Show bird name and photo attribution on each thumbnail
- [x] Allow user to select/deselect photos (checkbox or click toggle)
- [x] Add "Select All" / "Deselect All" buttons per bird
- [x] Add "Download Selection" button that generates JSON file
- [x] JSON output identifies selected photos (by bird scientificName + photo index)
- [x] Include ability to flag photos as inappropriate (eggs, dead birds, etc.)
- [x] Style for easy review (clear thumbnails, search, live stats)

### 13. Research ALA/GALAH API for media retrieval ✅
- [x] Research ALA/GALAH API (Atlas of Living Australia) documentation
- [x] Identify endpoints for retrieving bird photos/media
- [x] Determine authentication requirements (none required for public data)
- [x] Document API usage, rate limits, and license requirements
- [x] Create comprehensive notes in `data-search/ALA_API_NOTES.md`
- [x] Document species identification method

### 14. Develop ALA media search script ✅
- [x] Create `data-search/search_ala_photos.py`
- [x] Use ALA API to search for bird photos by scientific name
- [x] Filter for appropriate licenses (CC BY, CC BY-SA, CC BY-NC, CC BY-NC-SA, CC0)
- [x] Extract photo URL, source page, license, and attribution
- [x] Format output to match existing photo data structure
- [x] Add error handling and rate limiting (2s between requests)
- [x] Output results to timestamped JSON file for review

### 15. Test ALA media search script ⏳
- [x] Create comprehensive testing guide (`data-search/ALA_TESTING_GUIDE.md`)
- [ ] Test script with a few bird species (requires human to run tests)
- [ ] Verify photo URLs are accessible and correctly formatted
- [ ] Verify attribution and license data is captured correctly
- [ ] Test with species that have no existing photos
- [ ] Test with species that already have photos
- [ ] Document any issues or limitations found
- [ ] Create a sample output file for review

**Note**: Testing requires running against live ALA API. A comprehensive testing guide has been created with 10 test cases. Human testing recommended before production use.

## Tasks Requiring Human Input (Not for Autonomous Session)

The following items from feedback cannot be completed autonomously:

- **Hosting audio files**: Infrastructure decision needed from human
- **Rename the game**: Creative/branding decision
- **Design assets/favicon**: Requires graphic design work
- **Review links page**: Human verification of accuracy needed
- **Write complete about page**: Needs human contact information and messaging
- **Actually reviewing photos with the tool**: Human needs to use the photo review tool to flag inappropriate images
- **Integrating ALA photos into dataset**: Human needs to review and approve which ALA photos to add

---

## Notes

- Work through tasks in order where possible
- Commit changes frequently with clear messages
- Run `npm run dev` to test changes locally
- If a task is blocked or unclear, document the issue and move to the next task
