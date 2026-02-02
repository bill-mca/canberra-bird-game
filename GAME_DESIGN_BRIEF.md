# Canberra Bird Game - Design Brief

## Overview

An educational bird identification game featuring all 297 bird species found in the Australian Capital Territory. Players learn to identify birds through photos, sounds, and factual information while progressing through difficulty levels.

---

## Available Data Assets

### Bird Species: 297 total
- **Photos**: 1,435 images (4.83 per bird, 100% coverage)
- **Audio**: 1,272 recordings (4.28 per bird, 91.6% coverage)
- **Metadata**: Scientific names, families, status information

### Rarity Distribution
- Very Common: 36 species (12%)
- Common: 128 species (43%)
- Rare: 64 species (22%)
- Vagrant: 63 species (21%)
- Extinct: 5 species (2%)

### Conservation Status
- Critically Endangered: 2 species
- Endangered: 8 species
- Vulnerable: 32 species
- Total threatened: 42 species (14%)

### Origin
- Native species: 282 (95%)
- Introduced species: 15 (5%)

---

## Core Game Mechanics

### 1. Identification Challenge

**Visual Mode:**
- Show a random bird photo
- Player identifies from multiple choice or free text
- Reveal information after answer

**Audio Mode:**
- Play a bird call/song recording
- Player identifies by sound alone
- Higher difficulty, higher points

**Mixed Mode:**
- Combine visual and audio clues
- Most realistic to real birding experience

### 2. Difficulty Levels

#### 🟢 Beginner (164 species)
**Species Pool:** Very Common + Common birds
- Species that are regularly seen
- Easy to identify with distinctive features
- **Examples:** Australian Magpie, Crimson Rosella, Superb Fairy-wren

**Game Features:**
- Multiple choice with 4 options
- Show helpful hints (family, size)
- Audio optional, visual primary
- Forgiving scoring

#### 🟡 Intermediate (228 species)
**Species Pool:** Add Uncommon + Some Rare birds
- Mix of common and less frequently seen species
- More similar-looking birds (thornbills, honeyeaters)
- **Examples:** Spotted Pardalote, Yellow-rumped Thornbill, Gang-gang Cockatoo

**Game Features:**
- Multiple choice with 6 options
- Fewer hints available
- Audio + visual challenges
- Stricter time limits

#### 🔴 Advanced (297 species)
**Species Pool:** All birds including Rare + Vagrant
- Includes rarely-seen migrants and vagrants
- Very similar species (requires expert knowledge)
- **Examples:** Sharp-tailed Sandpiper, Red-necked Stint, Grey Falcon

**Game Features:**
- Multiple choice with 8+ options OR free text
- Minimal hints
- Audio-only challenges included
- Expert-level scoring

#### ⭐ Expert Mode Variants

**Audio-Only Challenge:**
- Identify birds by call/song alone
- 272 species available (those with audio)
- True birding experience

**Time Attack:**
- Identify as many birds as possible in limited time
- Progressive difficulty (common → rare)

**Conservation Focus:**
- Only threatened/endangered species (42 species)
- Educational about conservation status
- Highlight ACT, NSW, and Federal (EPBC) listings

---

## Game Modes

### Campaign Mode
**Linear progression through difficulty levels**

1. Start with Very Common birds (36 species)
2. Unlock Common birds after mastering 80% (128 species)
3. Progress to Rare and Vagrant species
4. Final challenge: All 297 species

**Progression System:**
- Earn stars for correct identifications
- Unlock species information cards
- Build a personal "field guide"
- Track statistics (accuracy, speed, favorites)

### Free Play Mode
**Customize your experience**

- Select difficulty level
- Choose specific families (e.g., only honeyeaters, parrots)
- Filter by rarity
- Filter by conservation status
- Native vs Introduced species

### Daily Challenge
**New challenge every day**

- 10 random birds from mixed difficulties
- Global leaderboard
- Share results with friends
- Seasonal themes (breeding visitors in summer, winter migrants)

### Conservation Quest
**Educational focus on threatened species**

**Mission:** Learn about ACT's threatened birds
- 2 Critically Endangered species
- 8 Endangered species
- 32 Vulnerable species

**Features:**
- Why they're threatened
- Conservation efforts in ACT
- How to report sightings
- Links to conservation organizations

---

## Educational Features

### Species Information Cards

After identifying a bird (correctly or incorrectly), show:

**Basic Info:**
- Common and scientific names
- Family
- Status in ACT (rarity, breeding status)

**Visuals:**
- Photo gallery (up to 5 photos per species)
- Show different angles, male/female, breeding/non-breeding plumage

**Audio:**
- Play call/song recordings (up to 5 per species)
- Label as "song", "call", "alarm", etc.
- Show audio quality rating

**Conservation:**
- Conservation status (if threatened)
- Jurisdictions (ACT/NSW/EPBC)
- Brief conservation notes

**Attribution:**
- Photo credits with links
- Audio recordist credits
- All properly licensed (CC BY, CC BY-SA, CC BY-NC, etc.)

### Field Guide
**Build as you play**

- Collect species you've correctly identified
- Review any time from main menu
- Search by name, family, rarity
- Filter by attributes
- Mark favorites
- Add personal notes

---

## Scoring System

### Points per Correct Answer

**Base Points by Difficulty:**
- Very Common: 10 points
- Common: 25 points
- Rare: 50 points
- Vagrant: 100 points
- Extinct: 150 points (historical interest)

**Multipliers:**
- Audio-only identification: 2x
- No hints used: 1.5x
- Fast answer (<10 seconds): 1.25x
- First time correct: Bonus 50 points

**Penalties:**
- Wrong answer: -5 points (min 0)
- Hint used: -10 points
- Skip: 0 points

### Achievements

**Collection Achievements:**
- ⭐ "Backyard Birder" - Identify all Very Common species
- 🌟 "Keen Observer" - Identify 100 species
- 🏆 "Master Ornithologist" - Identify all 297 species
- 🦜 "Parrot Expert" - Identify all parrots and lorikeets
- 🦆 "Waterfowl Watcher" - Identify all ducks, geese, and grebes

**Skill Achievements:**
- 🎵 "Good Ear" - 100 correct audio-only identifications
- ⚡ "Speed Demon" - 50 identifications in under 5 seconds
- 🎯 "Perfect Streak" - 20 correct in a row
- 🧠 "No Hints Needed" - 50 correct without using hints

**Conservation Achievements:**
- 🌿 "Conservation Champion" - Identify all threatened species
- 📢 "Advocate" - Share 10 conservation facts
- 🔴 "Critical Status" - Learn about critically endangered species

---

## Technical Considerations

### Data Structure
✅ Already implemented in `act_birds.json`:
- Structured rarity fields
- Conservation status with jurisdictions
- Multiple photos per species
- Multiple audio recordings per species
- Proper licensing and attribution

### Filtering Capabilities
```javascript
// Example: Get beginner-level birds
birds.filter(b =>
  ['very_common', 'common'].includes(b.rarity)
)

// Example: Get native birds only
birds.filter(b => !b.isIntroduced)

// Example: Get threatened species
birds.filter(b =>
  b.conservationStatus !== null
)

// Example: Get birds with audio
birds.filter(b =>
  b.audio && b.audio.length > 0
)
```

### Media Considerations
- **Photos:** All images hosted externally (Wikimedia, ALA, iNaturalist)
- **Audio:** All recordings hosted externally (Xeno-canto)
- **Licensing:** All media properly licensed for reuse
- **Attribution:** Display photographer/recordist names and links
- **Fallback:** Some rare species have fewer than 5 photos/audio

---

## User Interface Suggestions

### Main Menu
- Campaign Mode
- Free Play
- Daily Challenge
- Field Guide
- Statistics
- Settings

### Identification Screen
- Large photo/audio player area
- Multiple choice buttons (or text input)
- Hint button (bottom left)
- Skip button (bottom right)
- Score/streak display (top)
- Progress indicator

### Results Screen
- Correct/Incorrect feedback
- Show correct bird name and photo
- "Learn More" button → species card
- Play audio sample
- "Next Bird" button
- Statistics update

### Field Guide
- Search bar (top)
- Filter buttons (rarity, family, conservation)
- Grid or list view toggle
- Species cards with:
  - Photo thumbnail
  - Common name
  - Rarity indicator
  - Conservation status badge (if applicable)
  - "Unlocked" or "Locked" status

---

## Accessibility

### Visual
- High contrast mode
- Adjustable text size
- Color-blind friendly indicators
- Alternative text for all images

### Audio
- Visual indicators for audio cues
- Volume controls
- Option to play audio slowly
- Subtitles for educational content

### Cognitive
- Adjustable time limits
- Option to disable timers
- Clear, simple instructions
- Progress saving

---

## Expansion Ideas

### Future Features
- **Location-based play:** Use GPS to show birds likely in your area
- **Seasonal variations:** Different bird sets for summer/winter
- **Photo upload:** Let users submit their own bird photos
- **Social features:** Friend challenges, leaderboards
- **Augmented Reality:** Point camera at real birds for ID help
- **Integration with eBird:** Import sightings, contribute observations

### Additional Content
- **Bird families mode:** Learn taxonomic relationships
- **Behavior quiz:** Identify birds by behavior descriptions
- **Habitat matching:** Which birds live in which habitats?
- **Migration patterns:** Learn about seasonal movements
- **Breeding biology:** Nesting, eggs, chicks

---

## Educational Goals

### Primary Learning Outcomes
1. Identify common ACT bird species by sight and sound
2. Understand bird families and taxonomic relationships
3. Learn about conservation status and threats
4. Develop observational skills
5. Foster appreciation for local biodiversity

### Secondary Outcomes
1. Learn about introduced vs native species
2. Understand seasonal migration patterns
3. Recognize different call types (song, alarm, contact)
4. Develop citizen science interest
5. Promote conservation awareness

---

## Target Audience

### Primary
- **Bird enthusiasts** (beginners to intermediate)
- **Students** (high school and university biology)
- **Canberra residents** wanting to learn local birds
- **Educators** teaching local ecology

### Secondary
- **Tourists** visiting ACT
- **Families** seeking educational games
- **Citizen scientists** contributing to eBird
- **Conservation advocates**

---

## Success Metrics

### Engagement
- Daily active users
- Average session length
- Return rate (7-day, 30-day)
- Campaign completion rate

### Learning
- Accuracy improvement over time
- Number of species mastered
- Field guide completeness
- Conservation content views

### Community
- Daily challenge participation
- Social shares
- User-submitted content (if enabled)
- Positive reviews/ratings

---

## Development Priorities

### Phase 1: MVP (Minimum Viable Product)
✅ Data collection complete
- [ ] Basic identification game (visual mode)
- [ ] Three difficulty levels
- [ ] Score tracking
- [ ] Simple field guide
- [ ] Attribution display

### Phase 2: Enhanced Features
- [ ] Audio mode
- [ ] Daily challenge
- [ ] Achievements system
- [ ] Enhanced field guide
- [ ] Statistics dashboard

### Phase 3: Educational Focus
- [ ] Conservation quest mode
- [ ] Detailed species information
- [ ] Educational content
- [ ] Links to external resources
- [ ] Accessibility features

### Phase 4: Community Features
- [ ] Leaderboards
- [ ] Social sharing
- [ ] User profiles
- [ ] Location-based features
- [ ] Integration with eBird/citizen science

---

## Licensing & Attribution

### Content Sources
- **Photos:** Wikimedia Commons, Atlas of Living Australia, iNaturalist
- **Audio:** Xeno-canto
- **Licenses:** CC BY, CC BY-SA, CC BY-NC, CC BY-NC-SA, CC0

### Display Requirements
Must display for each media item:
- Creator/photographer/recordist name
- License type
- Link to source page
- "View license" link

### Game Code Licensing
Recommend open source license to encourage:
- Educational use
- Adaptation for other regions
- Community contributions
- Conservation awareness

---

## Next Steps

1. **Design wireframes** for main screens
2. **Choose platform** (web, mobile native, progressive web app)
3. **Select technology stack** (React, Flutter, Unity, etc.)
4. **Create prototype** with 10-20 species
5. **User testing** with target audience
6. **Iterate based on feedback**
7. **Full development** with all 297 species
8. **Launch & promotion**

---

## Contact & Contributions

**Data prepared by:** Claude Sonnet 4.5
**Date:** 2026-02-02
**Dataset:** `data/act_birds.json`

**Resources:**
- Photos: 1,435 images
- Audio: 1,272 recordings
- Species: 297 birds
- All properly licensed and attributed

Ready for game development! 🎮🐦
