# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Canberra Bird Game is an educational bird identification game featuring all 297 bird species found in the Australian Capital Territory. The project consists of:

- **Main Application** (`canberra-bird-app/`): A Vue 3 web application with three game modes (Daily Challenge, Free Play, Time Attack)
- **Data Tools** (`data-search/`): Python scripts for searching and collecting bird photos and audio from online sources
- **Bird Data** (`data/act_birds.json`): Master dataset with 297 bird species including 1,435 photos and 1,272 audio recordings

## Development Commands

### Web Application (canberra-bird-app/)

```bash
# Install dependencies
npm install

# Start development server (http://localhost:5173)
npm run dev

# Build for production (outputs to dist/)
npm run build

# Preview production build
npm run preview
```

### Data Collection Scripts (data-search/)

```bash
# Search for bird photos
python3 search_photos.py

# Search for bird audio from Xeno-canto
python3 search_audio.py

# Add/update rarity fields in bird data
python3 add_rarity_fields.py

# Test Xeno-canto API
python3 test_xeno_canto_api.py
```

## Architecture

### Vue Application Structure

The app uses Vue 3 Composition API with `<script setup>` syntax and a simple client-side routing system:

- **App.vue**: Root component that manages view navigation and initial data loading
  - Loads bird data on mount via `loadBirdData()` from `utils/birdData.js`
  - Renders current view based on `currentView` ref (daily, menu, freeplay, etc.)
  - Provides global navigation via `navigateTo()` function passed to child components

- **Views** (`src/views/`): Full-page components for each game mode/screen
  - Each view receives a `@navigate` event handler to switch between views
  - Views manage their own game state (current question, score, results)

- **Components** (`src/components/`): Reusable game interface components
  - `GameScreen.vue`: Main quiz interface with photo/audio display and multiple choice buttons
  - `ResultsScreen.vue`: Displays bird information after answering

- **Utils** (`src/utils/`): Pure JavaScript modules with no Vue dependencies
  - `birdData.js`: Data loading, filtering (by difficulty/family/rarity), random selection
  - `scoring.js`: Point calculations based on rarity with multipliers (no hints, fast answer)
  - `storage.js`: LocalStorage persistence for streaks, stats, daily challenge completion
  - `dailySeed.js`: Deterministic daily bird selection using date-based seeding

### Data Flow

1. App loads `act_birds.json` from `/public` on mount
2. Views filter birds based on difficulty/settings using `birdData.js` utilities
3. Game modes select birds and generate multiple choice options
4. User answers trigger scoring calculations via `scoring.js`
5. Results are persisted to LocalStorage via `storage.js`
6. Daily Challenge uses deterministic seeding to ensure all players see the same bird

### Bird Data Schema

The `act_birds.json` file contains:
- `commonName`, `scientificName`, `family`: Bird identification
- `statusInACT`: Original status text from checklist
- `rarity`: Standardized field (very_common, common, uncommon, rare, vagrant, extinct)
- `isIntroduced`: Boolean for non-native species
- `conservationStatus`: Object with ACT/NSW/National/IUCN status codes
- `photos`: Array of objects with `url`, `pageUrl`, `source`, `licence`, `attribution`
- `audio`: Array of objects with `url`, `pageUrl`, `source`, `licence`, `attribution`

### Difficulty System

Three difficulty levels defined in `DIFFICULTY_LEVELS` (birdData.js):
- **Beginner**: Very Common + Common birds (164 species, 4 options)
- **Intermediate**: Adds Uncommon + Rare birds (228 species, 6 options)
- **Advanced**: All birds including Vagrant/Extinct (297 species, 8 options)

### Scoring System

Base points by rarity (scoring.js):
- Very Common: 10 pts
- Common: 25 pts
- Uncommon: 40 pts
- Rare: 50 pts
- Vagrant: 100 pts
- Extinct: 150 pts

Multipliers: No hints (1.5x), Fast answer <5s (1.25x), Audio-only (2x - future feature)

### Daily Challenge Mechanism

Uses deterministic seeding to ensure consistent daily birds:
1. Generate seed from date string: `hashString('canberra-birds-YYYY-MM-DD')`
2. Use Mulberry32 PRNG with that seed
3. Select bird at index `floor(random() * totalBirds)`
4. Same date always produces same bird for all players

Streak tracking:
- Increments on correct daily challenge answers
- Persists in LocalStorage with last played date
- Only breaks if user misses a day (not if they answer incorrectly)

### Storage Keys

LocalStorage uses prefixed keys to avoid conflicts:
- `canberra_birds_daily_streak`: Current streak count
- `canberra_birds_daily_completed`: JSON with today's result
- `canberra_birds_stats`: All-time statistics object
- `canberra_birds_last_played`: Last played date (YYYY-MM-DD)

## Deployment

The app is a static site built with Vite. No backend required.

**Cloudflare Pages** (recommended):
- Build command: `npm run build`
- Build output: `dist`
- Root directory: `canberra-bird-app`

The `dist/` folder contains all static assets and can be deployed to any static hosting service.

## Data Sources and Licensing

- Bird checklist: Canberra Ornithologists Group
- Photos: Wikimedia Commons, Atlas of Living Australia, iNaturalist (various CC licenses)
- Audio: Xeno-canto community recordings (CC licenses)
- All media includes full attribution metadata in `act_birds.json`

## Code Style

- Vue 3 Composition API with `<script setup>`
- No TypeScript (vanilla JavaScript)
- CSS custom properties for theming in App.vue
- Vanilla CSS (no preprocessors or utility frameworks)
- Mobile-first responsive design
- Semantic HTML for accessibility
