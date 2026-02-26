# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Canberra Bird Game is an educational bird identification quiz featuring 297 bird species from the Australian Capital Territory. The project has two parts:

- **Web Application** (`canberra-bird-app/`): Vue 3 SPA with three game modes (Daily Challenge, Free Play, Time Attack)
- **Data Tools** (`data-search/`): Python scripts for collecting bird photos and audio from external APIs (ALA, Xeno-canto, Wikimedia)

## Development Commands

### Web Application (canberra-bird-app/)

```bash
npm install              # Install dependencies
npm run dev              # Dev server at http://localhost:5173
npm run build            # Production build to dist/
npm run preview          # Preview production build
```

There is no test framework, linter, or formatter configured. Verify changes by running `npm run build` to check for compilation errors.

### Data Scripts (data-search/)

Python scripts for media collection. Require a virtual environment:

```bash
cd data-search
python3 -m venv .venv && source .venv/bin/activate
pip install requests     # Main dependency
```

Key scripts: `search_ala_photos.py` (ALA photo search), `search_audio.py` (Xeno-canto audio), `add_rarity_fields.py` (rarity classification), `optimize_wikimedia_urls.py` (thumbnail optimization).

## Architecture

### Routing

The app uses **custom client-side routing** (no Vue Router). `App.vue` holds a `currentView` ref with string values (`'daily'`, `'menu'`, `'freeplay'`, `'timeattack'`, `'links'`, `'stats'`, `'about'`). Views are conditionally rendered with `v-if` and navigate by emitting a `@navigate` event that calls `navigateTo(view)`. There is no URL-based routing or deep linking.

The default view on app load is `'daily'` (Daily Challenge).

### Data Loading

`App.vue` calls `loadBirdData()` from `utils/birdData.js` on mount, which fetches `/act_birds.json` from the public directory. All views access the loaded data through utility functions rather than props — `birdData.js` caches the data in a module-level variable.

**Important:** Bird data exists in two locations:
- `data/act_birds.json` — master copy for data scripts to modify
- `canberra-bird-app/public/act_birds.json` — copy served by the web app

These must be kept in sync manually.

### Game Components

Two shared components power all game modes:
- **`GameScreen.vue`**: Quiz interface with photo display, multiple-choice buttons, hints, timer, and progress counter
- **`ResultsScreen.vue`**: Post-answer display with bird info, audio player, photo gallery, and attribution

Views manage their own game state and pass data to these components.

### Utility Modules (src/utils/)

All modules are pure JavaScript with no Vue dependencies:

- **`birdData.js`**: Data loading, filtering (difficulty/family/rarity/conservation/origin), random selection, and multiple-choice generation. Contains `DIFFICULTY_LEVELS` config and `getTaxonomicWrongOptions()` which generates wrong answers from the same genus/family for harder difficulties.
- **`dailySeed.js`**: Deterministic daily bird selection using date-seeded Mulberry32 PRNG — same date always produces the same bird for all players.
- **`storage.js`**: LocalStorage wrapper for streaks, stats, and daily completion state. All keys prefixed with `canberra_birds_`.
- **`scoring.js`**: Simplified to just `calculateSessionStats(results)` — returns correct/incorrect counts, accuracy %, and average time.

### Difficulty System

Three levels defined in `DIFFICULTY_LEVELS` (birdData.js):
- **Beginner**: Very Common + Common birds, 4 answer options, random wrong answers
- **Intermediate**: Adds Uncommon + Rare, 6 options, prefers same-family wrong answers
- **Advanced**: All 297 species, 8 options, prefers same-genus wrong answers

### Daily Challenge

Uses deterministic seeding (`hashString('canberra-birds-YYYY-MM-DD')` → Mulberry32 PRNG) so all players see the same bird each day. Streak increments on correct answers and breaks only if a day is missed (not on wrong answers). Completion state prevents replay on the same day.

### Bird Data Schema

Each bird in `act_birds.json` has: `commonName`, `scientificName`, `family`, `genus`, `statusInACT`, `rarity` (very_common/common/uncommon/rare/vagrant/extinct), `isIntroduced`, `conservationStatus` (ACT/NSW/National/IUCN), `photos[]` and `audio[]` arrays with `url`, `pageUrl`, `source`, `licence`, `attribution`.

## Deployment

### Frontend (Cloudflare Workers + Git Integration)

The frontend is deployed as a **Cloudflare Workers** project (not Pages) named `canberra-bird-game`, connected to the `bill-mca/canberra-bird-game` GitHub repo. It auto-deploys on push to `main`.

- **Production domain:** `birdguesser.org`
- **Workers domain:** `canberra-bird-game.<account>.workers.dev`
- **Config:** `canberra-bird-app/wrangler.jsonc`
- **Build:** `npm run build` → output `dist/`

Branch/preview deployments can be triggered manually:
```bash
cd canberra-bird-app && npm run build && wrangler versions upload
```

### Push Notification Worker

A separate Cloudflare Worker at `push-worker/` handles push subscriptions and daily notification cron.

- **Worker name:** `bird-guesser-push`
- **URL:** `https://bird-guesser-push.u5007063.workers.dev`
- **Config:** `push-worker/wrangler.toml`
- **Deploy:** `cd push-worker && wrangler deploy`

**Important:** The push worker's `FRONTEND_ORIGIN` var and the frontend's `VITE_PUSH_WORKER_URL` env must stay in sync with the actual deployed URLs.

## Code Style

- Vue 3 Composition API with `<script setup>`, vanilla JavaScript (no TypeScript)
- CSS custom properties for theming (defined in `App.vue` `:root`), vanilla CSS, mobile-first responsive
- Global utility classes (`.btn`, `.btn-primary`, `.card`) defined in `App.vue`'s unscoped `<style>` block

## Task Management

Tasks are tracked in `backlog.md` at the repository root. Progress is documented in `PROGRESS.md`.
