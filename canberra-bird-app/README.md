# Canberra Bird Game 🦜

An educational bird identification game featuring all 297 bird species found in the Australian Capital Territory. Test your knowledge through photos and sounds while learning about local biodiversity!

## Features

### Game Modes

- **📅 Daily Challenge** - One bird per day, build your streak!
- **🎮 Free Play** - Customize difficulty, species filters, and number of questions
- **⏱️ Time Attack** - How many birds can you identify in 60 seconds?

### Difficulty Levels

- **🟢 Beginner** - Very Common + Common birds (164 species, 4 options)
- **🟡 Intermediate** - Add Uncommon + Rare birds (228 species, 6 options)
- **🔴 Advanced** - All birds including Vagrant species (297 species, 8 options)

### Educational Features

- 1,435 high-quality bird photos (4.83 average per species)
- 1,272 audio recordings (4.28 average per species, 91.6% coverage)
- Species information including family, rarity, and conservation status
- Expandable attribution for all media
- Links to Canberra birding resources

### Scoring System

Points awarded based on rarity:
- Very Common: 10 points
- Common: 25 points
- Uncommon: 40 points
- Rare: 50 points
- Vagrant: 100 points
- Extinct: 150 points

**Multipliers:**
- Audio-only identification: 2× (future feature)
- No hints used: 1.5×
- Fast answer (<5 seconds): 1.25×

## Technology Stack

- **Vue 3** - Progressive JavaScript framework
- **Vite 5** - Fast build tool and dev server
- **Vanilla CSS** - Clean, custom styling with CSS variables
- **LocalStorage** - Persistent data for streaks and statistics

## Getting Started

### Prerequisites

- Node.js 18.19.1 or higher
- npm 9.2.0 or higher

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/canberra-bird-game.git
cd canberra-bird-game/canberra-bird-app
```

2. Install dependencies:
```bash
npm install
```

3. Run development server:
```bash
npm run dev
```

4. Open your browser to http://localhost:5173

### Build for Production

```bash
npm run build
```

The built files will be in the `dist/` directory, ready for deployment.

### Preview Production Build

```bash
npm run preview
```

## Deployment

### Cloudflare Pages

1. Connect your GitHub repository to Cloudflare Pages
2. Set build settings:
   - **Build command:** `npm run build`
   - **Build output directory:** `dist`
   - **Root directory:** `canberra-bird-app`
3. Deploy!

### GitHub Pages

1. Build the project: `npm run build`
2. Deploy the `dist/` folder to GitHub Pages
3. Configure base path in `vite.config.js` if needed

### Other Platforms

The app is a static site and can be deployed to:
- Netlify
- Vercel
- AWS S3 + CloudFront
- Any static hosting service

## Project Structure

```
canberra-bird-app/
├── public/
│   └── act_birds.json          # Bird data (297 species)
├── src/
│   ├── components/
│   │   ├── GameScreen.vue      # Main identification interface
│   │   └── ResultsScreen.vue   # Results and bird info display
│   ├── views/
│   │   ├── MainMenu.vue        # Main menu
│   │   ├── DailyChallenge.vue  # Daily challenge mode
│   │   ├── FreePlay.vue        # Free play mode
│   │   ├── TimeAttack.vue      # Time attack mode
│   │   ├── LinksPage.vue       # Birding resources
│   │   └── StatsPage.vue       # Statistics display
│   ├── utils/
│   │   ├── birdData.js         # Data loading and filtering
│   │   ├── scoring.js          # Scoring calculations
│   │   ├── storage.js          # LocalStorage management
│   │   └── dailySeed.js        # Deterministic daily bird selection
│   ├── App.vue                 # Root component
│   └── main.js                 # Application entry point
├── package.json
├── vite.config.js
└── README.md
```

## Data Sources

All media and data is properly licensed and attributed:

- **Photos:** Wikimedia Commons, Atlas of Living Australia, iNaturalist
- **Audio:** Xeno-canto community recordings
- **Species Data:** Atlas of Living Australia, BirdLife Australia

## Development

### Adding New Features

The codebase is modular and easy to extend:

- Add new game modes in `src/views/`
- Add new utility functions in `src/utils/`
- Modify scoring in `src/utils/scoring.js`
- Update bird filtering logic in `src/utils/birdData.js`

### Code Style

- Vue 3 Composition API with `<script setup>`
- CSS custom properties for theming
- Semantic HTML for accessibility
- Mobile-first responsive design

## Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile browsers (iOS Safari, Chrome Mobile)
- Requires JavaScript enabled
- LocalStorage for persistence

## Performance

- Lazy loading images
- External media links (no large file downloads)
- Efficient Vue reactivity
- Minimal bundle size (~103KB JS, ~25KB CSS)

## Accessibility

- Semantic HTML structure
- Keyboard navigation support
- Alt text for all images
- Sufficient color contrast
- Clear focus indicators

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

Game code: [Your chosen license]

Media content:
- Photos: Various CC licenses (see attribution)
- Audio: Various CC licenses (see attribution)
- Bird data: CC BY from ALA and BirdLife Australia

## Acknowledgments

- **Canberra Ornithologists Group** - Bird records and data
- **Atlas of Living Australia** - Species data and photos
- **Xeno-canto** - Audio recordings
- **Wikimedia Commons** - Photos
- **iNaturalist** - Photos and observations
- All photographers and sound recordists who contributed media

## Contact

For questions or feedback, please open an issue on GitHub.

---

**Dataset Stats:**
- 297 bird species
- 1,435 photos (100% coverage)
- 1,272 audio recordings (91.6% coverage)
- All properly licensed and attributed

Built with ❤️ for the Canberra birding community
