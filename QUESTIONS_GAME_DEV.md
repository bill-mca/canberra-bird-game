# Game Development Questions

## Critical Technical Decisions

### 1. Technology Stack
The design brief specifies "static website built with javascript" and wants the interface "as clean as possible."

**Question:** Should I use:
- A) **Vanilla JavaScript** (HTML, CSS, JS - no framework, simplest, fastest loading)
- B) **React** (component-based, easier to maintain, but adds complexity)
- C) **Vue** (lighter than React, good middle ground)
- D) **Other framework you prefer?**

Vue
---

### 2. CSS Framework
**Question:** Should I use:
- A) **No framework** (custom CSS, smallest file size, most control)
- B) **Tailwind CSS** (utility-first, modern, fast development)
- C) **Bootstrap** (mature, lots of components)
- D) **Other CSS framework?**

**My recommendation:** No framework (custom CSS) for clean, minimal UI

---

### 3. Build Tools
**Question:** Should I use:
- A) **No build tools** (simple HTML/CSS/JS files, works immediately)
- B) **Vite** (fast, modern, hot reload for development)
- C) **Webpack** (powerful but complex)

**My recommendation:** No build tools for simplicity (can add later if needed)

---

### 4. Media Hosting Strategy
Currently all photos and audio link to external sources (Wikimedia, Xeno-canto, etc.)

**Question:** Should I:
- A) **Keep external links** (pros: no hosting cost, smaller repo; cons: depends on external services)
- B) **Download all media locally** (pros: full control, works offline; cons: large repo, hosting costs)
- C) **Hybrid approach** (download thumbnails, link to full-size)

**My recommendation:** Keep external links (as per current data structure)

---

### 5. File Structure
**Question:** Preferred structure:
```
Option A (Simple):
canberra-bird-game/
├── index.html
├── style.css
├── script.js
├── data/
│   └── act_birds.json
└── README.md

Option B (Organized):
canberra-bird-game/
├── index.html
├── css/
│   ├── style.css
│   └── game.css
├── js/
│   ├── main.js
│   ├── game.js
│   └── data.js
├── data/
│   └── act_birds.json
├── assets/
│   └── (any local images/icons)
└── README.md

Option C (Modular):
canberra-bird-game/
├── index.html
├── css/
├── js/
│   ├── core/
│   ├── components/
│   └── utils/
├── data/
└── pages/
    ├── daily-challenge.html
    ├── free-play.html
    └── field-guide.html
```

**My recommendation:** Option B (organized but not over-engineered)

---

### 6. Development Phases Priority
The design brief outlines multiple game modes and features.

**Question:** What should I build first (MVP)?

**Option A - Minimal MVP:**
1. Basic daily challenge (1 bird, photo identification)
2. Simple results screen with species info
3. Basic attribution display
4. No persistence (no streak tracking yet)

**Option B - Enhanced MVP:**
1. Daily challenge with streak tracking (localStorage)
2. Free play mode (basic version)
3. Three difficulty levels
4. Score tracking
5. Species info cards

**Option C - Full Phase 1:**
Everything in the "Phase 1: MVP" section of design brief
- Visual identification game
- Three difficulty levels (all working)
- Score tracking
- Full attribution display
- Basic stats

Just build the whole thing Claude!!
---

### 7. Browser Storage Approach
For streak tracking, progress, field guide collection, etc.

**Question:** Should I use:
- A) **localStorage** (simple, persists, 5-10MB limit, no cross-device sync)
- B) **IndexedDB** (more powerful, unlimited storage, more complex)
- C) **No persistence yet** (build core game first, add later)

**My recommendation:** localStorage (good enough for this use case)

---

### 8. Daily Challenge Seed
The daily challenge needs the same bird for all players each day.

**Question:** How should I generate the daily bird?
- A) **Date-based random seed** (deterministic, same bird globally)
- B) **External API** (requires backend/serverless function)
- C) **Simple formula** (e.g., `birdIndex = dayOfYear % 297`)

**My recommendation:** Option A (date-based seed using hash of date string)

---

### 9. Social Sharing
Design brief mentions "share results with friends"

**Question:** Should I implement:
- A) **Web Share API** (native mobile sharing, works on modern browsers)
- B) **Copy to clipboard** (simple text results)
- C) **Both A and B**
- D) **Skip for now** (add in Phase 2)

Option A ---

### 10. Deployment/Hosting
**Question:** Where should I prepare this to be hosted?
- A) **GitHub Pages** (free, easy, static hosting)
- B) **Netlify** (free, auto-deploys from git, better features)
- C) **Vercel** (similar to Netlify)
- D) **Other platform?**
- E) **Just local files** (you'll deploy yourself)

I'll deploy it to Cloudflare pages later. 
---

### 11. Image Preloading Strategy
Photo identification games need smooth image loading.

**Question:** Should I:
- A) **Preload next image** while showing current question
- B) **Lazy load** (load on demand, faster initial page load)
- C) **No preloading** (simpler, might have delays)

**My recommendation:** Option A (preload next image for smooth UX)

---

### 12. Audio Player
**Question:** Should I use:
- A) **Native HTML5 `<audio>` element** (simple, browser-controlled UI)
- B) **Custom player** (styled to match game design, more control)
- C) **Audio-only mode** (skip for MVP, add in Phase 2)

**My recommendation:** Option A (native HTML5, add custom UI later if needed)

---

### 13. Attribution Display
All photos and audio must show attribution.

**Question:** Should attribution be:
- A) **Always visible** (text under photo/audio player)
- B) **Expandable info icon** ("ⓘ" click to see credits)
- C) **Separate credits page** (linked from each media)
- D) **Show after answering** (in results screen)

B - exapandable ---

#---

### 15. Time Attack Mode
Design brief mentions time attack mode.

**Question:** Should I:
- A) **Include in MVP** (build alongside daily challenge)
- B) **Phase 2** (after daily challenge works)

Do it! ---

### 16. Field Guide Feature
"Build as you play" - collect species you've correctly identified.

**Question:** Should I:
- A) **Include in MVP** (simple list of identified birds)
- B) **Phase 2** (after core game works)
- C) **Phase 3** (full featured version with search/filter)

Don't bother with a field guide. Expung this concept from the docs too.


---

### 17. Conservation/Education Info
Species cards show lots of educational content.

**Question:** For MVP, should species cards include:
- A) **Minimal** (name, photo, correct answer feedback)
- B) **Moderate** (+ family, rarity, basic stats)
- C) **Full** (everything in design brief: conservation, audio, photo gallery, etc.)

Moderate

---

### 18. Multiple Choice Options Display
**Question:** How should I display the bird name options?
- A) **Buttons in grid** (2×2 for beginner, 2×3 for intermediate, 2×4 for advanced)
- B) **Vertical list** (simple, scrollable if needed)
- C) **Dropdown select** (compact but less game-like)

**My recommendation:** Option A (buttons in grid, more engaging)

---

### 19. External Links
Design brief mentions "page with canberra birding info and links"

**Question:** Should I:
- A) **Include links page in MVP** (add value for local birders)
- B) **Add later** (focus on core game first)

Do this
- Canberra Ornithologists Group
- Search if there is anything from national parks ACT or the ACT government
- Jerrabombera wetlands
Mulligans flat
- search the web where you need to. 


---

### 20. Mobile Responsiveness
**Question:** Should the game be:
- A) **Mobile-first design** (optimized for phones, works on desktop)
- B) **Desktop-first design** (optimized for computer, works on mobile)
- C) **Responsive design** (works well on both)

**My recommendation:** Option C (responsive design)

