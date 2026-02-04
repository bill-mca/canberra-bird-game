# Canberra Bird Game - Backlog

Tasks for autonomous development session based on user feedback.

## Easy Fixes

### 1. Remove bird emoji from title
- [ ] Remove the 🦜 emoji from the app title in App.vue
- The macaw parrot is not appropriate for Canberra birds

### 2. Remove generic attribution footer
- [ ] Remove the blanket attribution text from app footer
- Individual photos already have proper attribution in expandable sections

### 3. Make bird photos clickable
- [ ] In ResultsScreen.vue, make thumbnail photos clickable
- Clicking should open the image's source page URL in a new tab
- Photos currently show hover feedback but don't do anything on click

### 4. Remove stats box from main menu
- [ ] Hide the "Your Stats" box from MainMenu.vue
- Stats are still accessible via the dedicated stats page

### 5. Add About page link to main menu
- [ ] Add a navigation link to an About page in MainMenu.vue

### 6. Create placeholder About page
- [ ] Create a new AboutPage.vue in src/views/
- [ ] Add simple placeholder content explaining the game
- [ ] Include a note that contact/detailed info will be added later
- [ ] Wire up navigation in App.vue

### 7. Remove progress summary from statistics page
- [ ] Hide or remove the progress summary section from StatsPage.vue

## Significant Changes

### 8. Simplify scoring system
- [ ] Remove complex point-based scoring system
- [ ] Just track correct/incorrect answers
- [ ] Update scoring.js to remove multipliers and rarity-based points
- [ ] Update all game views to use simplified scoring
- [ ] Update stats tracking in storage.js
- [ ] Simplify results display (no point breakdowns)

### 9. Debug audio playback
- [ ] Investigate why audio recordings are not playing
- [ ] Check browser console for errors
- [ ] Verify audio URL format and accessibility
- [ ] Test with different Xeno-canto recording URLs
- [ ] Document findings (may need to host audio ourselves if unfixable)

### 10. Improve difficulty with taxonomic filtering
- [ ] Modify multiple choice option selection to use taxonomic similarity
- [ ] For Advanced difficulty: prefer options from same genus, fall back to family, then random
- [ ] For Intermediate difficulty: prefer options from same family, fall back to random
- [ ] For Beginner difficulty: keep current random selection
- [ ] Add genus field to bird data if not present (extract from scientific name)
- [ ] Update birdData.js with new filtering functions
- [ ] Test that all difficulties still have enough options

### 11. Optimize image loading with smaller sizes
- [ ] Update photo URLs to use Wikimedia thumbnail API
- [ ] Use format: `/thumb/[path]/[width]px-[filename]`
- [ ] Choose appropriate size (e.g., 960px for main images, 330px for thumbnails)
- [ ] Update image display in GameScreen.vue and ResultsScreen.vue
- [ ] Only affects Wikimedia Commons URLs, preserve other source URLs as-is

## Data Collection & Review Tools

### 12. Create photo review tool
- [ ] Create a standalone HTML tool (`data-search/photo-review-tool.html`)
- [ ] Load bird data from `act_birds.json`
- [ ] Display all bird photos in a scrollable grid of thumbnails
- [ ] Show bird name and photo attribution on each thumbnail
- [ ] Allow user to select/deselect photos (checkbox or click toggle)
- [ ] Add "Select All" / "Deselect All" buttons per bird
- [ ] Add "Download Selection" button that generates JSON file
- [ ] JSON output should identify selected photos (by bird scientificName + photo index or URL)
- [ ] Include ability to flag photos as inappropriate (eggs, dead birds, etc.)
- [ ] Style for easy review (clear thumbnails, hover zoom, etc.)

### 13. Research ALA/GALAH API for media retrieval
- [ ] Research GALAH API (Atlas of Living Australia) documentation
- [ ] Identify endpoints for retrieving bird photos/media
- [ ] Determine authentication requirements (if any)
- [ ] Document API usage, rate limits, and license requirements
- [ ] Create notes in `data-search/ALA_API_NOTES.md`
- [ ] Identify which bird species have few photos and need ALA sourcing

### 14. Develop ALA media search script
- [ ] Create `data-search/search_ala_photos.py`
- [ ] Use GALAH API to search for bird photos by scientific name
- [ ] Filter for appropriate licenses (CC BY, CC BY-SA, CC0)
- [ ] Extract photo URL, source page, license, and attribution
- [ ] Format output to match existing photo data structure
- [ ] Add error handling and rate limiting
- [ ] Log results to `data-search/ala_search_log.txt`

### 15. Test ALA media search script
- [ ] Test script with a few bird species
- [ ] Verify photo URLs are accessible and correctly formatted
- [ ] Verify attribution and license data is captured correctly
- [ ] Test with species that have no existing photos
- [ ] Test with species that already have photos (should augment, not replace)
- [ ] Document any issues or limitations found
- [ ] Create a sample output file for review

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
