<script setup>
const emit = defineEmits(['navigate']);
</script>

<template>
  <div class="about-page">
    <div class="about-header">
      <h2>About Bird Guesser</h2>
    </div>

    <div class="about-content card">
      <section class="about-section">
        <h3>What is this?</h3>
        <p>
          Bird Guesser is an educational bird identification game featuring all 297 bird species
          found in the Australian Capital Territory. Test your knowledge through photos and sounds while
          learning about local biodiversity!
        </p>
      </section>

      <section class="about-section">
        <h3>Features</h3>
        <ul>
          <li><strong>Daily Challenge</strong> - One bird per day, build your streak!</li>
          <li><strong>Free Play</strong> - Customize difficulty, species filters, and number of questions</li>
          <li><strong>Time Attack</strong> - How many birds can you identify in 60 seconds?</li>
          <li><strong>Educational Content</strong> - Learn about bird families, rarity, and conservation status</li>
        </ul>
      </section>

      <section class="about-section">
        <h3>Data Sources</h3>
        <p>All media and data is properly licensed and attributed:</p>
        <ul>
          <li><strong>Photos:</strong> Wikimedia Commons, Atlas of Living Australia, iNaturalist (various CC licenses)</li>
          <li><strong>Audio:</strong> Xeno-canto community recordings (CC licenses)</li>
          <li><strong>Species Data:</strong> Canberra Ornithologists Group, Atlas of Living Australia, BirdLife Australia</li>
        </ul>
        <p class="attribution-note">
          Individual photo and audio attributions are displayed on result screens.
          All content is used under Creative Commons licenses.
        </p>
      </section>

      <section class="about-section">
        <h3>Dataset Stats</h3>
        <ul>
          <li>297 bird species</li>
          <li>1,435 photos (100% coverage)</li>
          <li>1,272 audio recordings (91.6% coverage)</li>
        </ul>
      </section>

      <section class="about-section">
        <h3>Contact</h3>
        <p>
          For questions, feedback, or to report issues, please contact the developer.
          <em>(Contact information to be added)</em>
        </p>
      </section>

      <section class="about-section">
        <h3>Technology</h3>
        <p>
          Built with Vue 3 and Vite. This is a static web application with no backend -
          all data is stored locally in your browser.
        </p>
      </section>
    </div>

    <div class="about-actions">
      <button class="btn btn-primary" @click="emit('navigate', 'menu')">
        ← Back to Menu
      </button>
    </div>
  </div>
</template>

<style scoped>
.about-page {
  max-width: 800px;
  margin: 0 auto;
}

.about-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.about-header h2 {
  color: var(--color-primary);
  font-size: 2rem;
}

.about-content {
  margin-bottom: var(--spacing-xl);
}

.about-section {
  margin-bottom: var(--spacing-xl);
}

.about-section:last-child {
  margin-bottom: 0;
}

.about-section h3 {
  color: var(--color-primary);
  margin-bottom: var(--spacing-md);
  font-size: 1.25rem;
}

.about-section p {
  line-height: 1.6;
  margin-bottom: var(--spacing-md);
}

.about-section ul {
  list-style: none;
  margin-left: 0;
  line-height: 1.8;
}

.about-section li {
  margin-bottom: var(--spacing-sm);
}

.attribution-note {
  font-size: 0.875rem;
  color: var(--color-text-light);
  font-style: italic;
}

.about-actions {
  display: flex;
  justify-content: center;
}

@media (max-width: 768px) {
  .about-header h2 {
    font-size: 1.5rem;
  }

  .about-section ul {
    margin-left: var(--spacing-lg);
  }
}
</style>
