<script setup>
const emit = defineEmits(['navigate']);

const links = [
  {
    category: 'Birding Organizations',
    items: [
      {
        title: 'Canberra Ornithologists Group (COG)',
        url: 'https://canberrabirds.org.au/',
        description: 'Founded in 1970, COG promotes the study and conservation of birds in the Canberra region. Join regular field trips, talks, and citizen science projects.'
      },
      {
        title: 'Woodlands and Wetlands Trust',
        url: 'https://www.woodlandsandwetlands.org.au/',
        description: 'Manages Mulligans Flat Woodland Sanctuary and other conservation reserves in the ACT region.'
      }
    ]
  },
  {
    category: 'Birding Locations',
    items: [
      {
        title: 'Jerrabomberra Wetlands Nature Reserve',
        url: 'https://www.parks.act.gov.au/find-a-nature-park/jerrabomberra-wetlands-nature-reserve',
        description: 'Over 170 species of birds recorded. Features multiple bird hides and walking tracks. Eight species of international migratory birds visit seasonally.'
      },
      {
        title: 'Mulligans Flat Nature Reserve',
        url: 'https://www.parks.act.gov.au/find-a-nature-park/canberra-nature-park/mulligans-flat-nature-reserve',
        description: 'Woodland sanctuary with self-guided bird walk. Home to honeyeaters, robins, thornbills, and six threatened woodland bird species.'
      },
      {
        title: 'Tidbinbilla Nature Reserve',
        url: 'https://www.parks.act.gov.au/find-a-nature-park/tidbinbilla-nature-reserve',
        description: 'Large nature reserve with diverse habitats supporting a wide variety of bird species from wetland to mountain birds.'
      },
      {
        title: 'Australian National Botanic Gardens',
        url: 'https://www.anbg.gov.au/',
        description: 'Excellent urban birding location with regular bird walks and diverse native vegetation attracting many species.'
      }
    ]
  },
  {
    category: 'Parks & Conservation',
    items: [
      {
        title: 'Parks ACT - Birdwatching',
        url: 'https://www.parks.act.gov.au/things-to-do/birdwatching',
        description: 'Official ACT Parks guide to birdwatching locations, bird hides, and guided tours across the territory.'
      },
      {
        title: 'ACT Wildlife',
        url: 'https://www.act.gov.au/our-canberra/latest-news/2025/2026/where-to-spot-wildlife-in-canberra',
        description: 'Guide to spotting wildlife including birds across Canberra parks and reserves.'
      }
    ]
  },
  {
    category: 'Citizen Science & Recording',
    items: [
      {
        title: 'eBird Australia',
        url: 'https://ebird.org/australia/home',
        description: 'Submit your bird sightings and explore what others have seen in the Canberra region. The world\'s largest biodiversity-related citizen science project.'
      },
      {
        title: 'Atlas of Living Australia',
        url: 'https://www.ala.org.au/',
        description: 'Explore occurrence records, photos, and sounds of Australian birds. Contribute your own observations.'
      },
      {
        title: 'Birdata (BirdLife Australia)',
        url: 'https://birdata.birdlife.org.au/',
        description: 'BirdLife Australia\'s bird survey platform. Participate in surveys and contribute to bird conservation research.'
      }
    ]
  },
  {
    category: 'Field Guides & Identification',
    items: [
      {
        title: 'Birds in Backyards',
        url: 'https://www.birdsinbackyards.net/',
        description: 'Excellent resource for identifying common Australian birds with photos, calls, and habitat information.'
      },
      {
        title: 'BirdLife Australia',
        url: 'https://www.birdlife.org.au/',
        description: 'National bird conservation organization with comprehensive species information and conservation status.'
      },
      {
        title: 'Xeno-canto',
        url: 'https://xeno-canto.org/',
        description: 'Sharing bird sounds from around the world. Listen to thousands of Australian bird calls and songs.'
      }
    ]
  }
];

function goToMenu() {
  emit('navigate', 'menu');
}
</script>

<template>
  <div class="links-page">
    <div class="page-header">
      <h2>🔗 Canberra Birding Resources</h2>
      <p>Explore local birding locations, organizations, and tools</p>
    </div>

    <div class="links-container">
      <div
        v-for="section in links"
        :key="section.category"
        class="link-section card"
      >
        <h3 class="section-title">{{ section.category }}</h3>

        <div class="link-list">
          <div
            v-for="item in section.items"
            :key="item.title"
            class="link-item"
          >
            <h4 class="link-title">
              <a :href="item.url" target="_blank" rel="noopener noreferrer">
                {{ item.title }} ↗
              </a>
            </h4>
            <p class="link-description">{{ item.description }}</p>
          </div>
        </div>
      </div>

      <div class="info-card card">
        <h3>About This Game</h3>
        <p>
          This game features all 297 bird species recorded in the Australian Capital Territory.
          Data sourced from:
        </p>
        <ul>
          <li><strong>Photos:</strong> Wikimedia Commons, Atlas of Living Australia, iNaturalist</li>
          <li><strong>Audio:</strong> Xeno-canto community recordings</li>
          <li><strong>Species data:</strong> Atlas of Living Australia, BirdLife Australia</li>
        </ul>
        <p class="attribution-note">
          All media is properly licensed under Creative Commons licenses and attributed to their creators.
        </p>
      </div>
    </div>

    <div class="page-actions">
      <button class="btn btn-primary" @click="goToMenu">
        ← Back to Main Menu
      </button>
    </div>
  </div>
</template>

<style scoped>
.links-page {
  max-width: 900px;
  margin: 0 auto;
}

.page-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.page-header h2 {
  font-size: 2rem;
  color: var(--color-primary);
  margin-bottom: var(--spacing-sm);
}

.links-container {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
}

.link-section {
  padding: var(--spacing-lg);
}

.section-title {
  color: var(--color-primary);
  font-size: 1.5rem;
  margin-bottom: var(--spacing-md);
  padding-bottom: var(--spacing-sm);
  border-bottom: 2px solid var(--color-border);
}

.link-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.link-item {
  padding: var(--spacing-md);
  background-color: var(--color-bg);
  border-radius: var(--border-radius);
  transition: var(--transition);
}

.link-item:hover {
  background-color: #e8f5e8;
}

.link-title {
  margin-bottom: var(--spacing-xs);
}

.link-title a {
  color: var(--color-primary);
  text-decoration: none;
  font-size: 1.125rem;
  font-weight: 500;
}

.link-title a:hover {
  text-decoration: underline;
}

.link-description {
  color: var(--color-text);
  font-size: 0.9375rem;
  line-height: 1.6;
}

.info-card {
  background-color: #fff3cd;
  border: 1px solid #ffc107;
}

.info-card h3 {
  color: var(--color-primary);
  margin-bottom: var(--spacing-md);
}

.info-card p {
  margin-bottom: var(--spacing-md);
  line-height: 1.6;
}

.info-card ul {
  margin-left: var(--spacing-lg);
  margin-bottom: var(--spacing-md);
}

.info-card li {
  margin-bottom: var(--spacing-xs);
}

.attribution-note {
  font-size: 0.875rem;
  color: var(--color-text-light);
  font-style: italic;
}

.page-actions {
  text-align: center;
}
</style>
