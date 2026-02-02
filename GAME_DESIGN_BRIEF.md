# Canberra Bird Game - Design Brief

## Overview

An educational bird identification game featuring all 297 bird species found in the Australian Capital Territory. Players learn to identify birds through photos, sounds, and factual information while progressing through difficulty levels.

This game will be a static website built with javascript. 
The interface will be as clean as posssible. Just focused on getting people to play with the data and learn about cool birds!
All open data will be properly attributed. 

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
- Multiple choice with 8 options
- Minimal hints
- Audio-only challenges included
- Expert-level scoring

## Game Modes

### Free Play Mode
**Customize your experience**

- Select difficulty level
- Choose specific families (e.g., only honeyeaters, parrots)
- Filter by rarity
- Filter by conservation status
- Native vs Introduced species
- Track statistics about your run
- Can share stats when you decide to finish.

### Time Attack
- How many birds can you get in a fixed time?
- Photos first, audio later.

### Daily Challenge
**New challenge every day**

- 1 random bird
- Share results with friends
- Streak tracked by browser cookie which saves a UID for each problem you correctly answered.
- Seasonal themes (breeding visitors in summer, winter migrants)

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
- Fast answer (<5 seconds): 1.25x

**Penalties:**
- Nah don't need penalties. 
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

Front page is the daily challenge. Once you answer you're shown your streak and given the main menu.

### Main Menu
- Links to game modes
- page with canberra birding info and links to Canberra bird websites sites
- Statistics
- Settings(?)

### Identification Screen
- Large photo/audio player area
- Hint button (bottom left)
- Skip button (bottom right)
- Score/streak display (top)
- Progress indicator (where relevant)
- Exciting count-down for time attack mode
- ID counter for time attack mode.

### Results Screen (For daily challenge and free play)
- Correct/Incorrect feedback
- Show correct bird name and photo
- "Learn More" button → species card
- Play audio sample
- "Next Bird" button
- Statistics update

## Accessibility

### Visual
- High contrast mode
- Adjustable text size
- Color-blind friendly indicators
- Alternative text for all images

### Audio
- Visual indicators for audio cues
- Volume controls

### Cognitive
- Adjustable time limits
- Option to disable timers
- Clear, simple instructions
- Progress saving

---

## Expansion Ideas

### Additional Content
- **Bird families mode:** Learn taxonomic relationships
- **Behavior quiz:** Identify birds by behavior descriptions
- **Habitat matching:** Which birds live in which habitats?
- **Migration patterns:** Learn about seasonal movements
- **Breeding biology:** Nesting, eggs, chicks

---

## Educational Goals

### Primary Learning Outcomes
1. Spread enthusiasm for birding!
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
- [ ] Attribution display

### Phase 2: Enhanced Features
- [ ] Audio mode
- [ ] Daily challenge
- [ ] Achievements system
- [ ] Stats

### Phase 3: Educational Focus
- [ ] Links to external resources
- [ ] Accessibility features

---

## Licensing & Attribution


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
2. Decide whether to host media local or link to external resources
2. **Choose platform** (web, mobile native, progressive web app)
3. **Select technology stack** (React, Flutter, Unity, etc.)
7. **Full development** with all 297 species
8. testing with friends
8. **Launch & promotion**

---

## Contact & Contributions

**Data collected by:** Claude Sonnet 4.5
**Date:** 2026-02-02
**Dataset:** `data/act_birds.json`
link to git reo

**Resources:**
- Photos: 1,435 images
- Audio: 1,272 recordings
- Species: 297 birds
- All properly licensed and attributed

