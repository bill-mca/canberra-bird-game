<script setup>
import { ref } from 'vue';
import { getScoreBreakdown } from '../utils/scoring.js';

const props = defineProps({
  bird: {
    type: Object,
    required: true
  },
  photo: {
    type: Object,
    required: true
  },
  selectedBird: {
    type: Object,
    default: null
  },
  isCorrect: {
    type: Boolean,
    required: true
  },
  score: {
    type: Number,
    default: 0
  },
  scoringOptions: {
    type: Object,
    default: () => ({})
  },
  showNextButton: {
    type: Boolean,
    default: true
  }
});

const emit = defineEmits(['next', 'share']);

const showAttribution = ref(false);
const currentAudioIndex = ref(0);

function toggleAttribution() {
  showAttribution.value = !showAttribution.value;
}

function playAudio(index) {
  currentAudioIndex.value = index;
}

const scoreBreakdown = getScoreBreakdown(props.bird, props.scoringOptions);
</script>

<template>
  <div class="results-screen">
    <div class="result-header" :class="{ correct: isCorrect, incorrect: !isCorrect }">
      <div class="result-icon">{{ isCorrect ? '✅' : '❌' }}</div>
      <h2 class="result-title">{{ isCorrect ? 'Correct!' : 'Incorrect' }}</h2>
      <p class="result-score" v-if="isCorrect && score > 0">+{{ score.toLocaleString() }} points</p>
    </div>

    <div class="selected-answer" v-if="!isCorrect && selectedBird">
      <p>You selected: <strong>{{ selectedBird.commonName }}</strong></p>
    </div>

    <div class="bird-info-card card">
      <div class="bird-main-info">
        <img :src="photo.url" :alt="bird.commonName" class="result-bird-image" />

        <div class="bird-details">
          <h3 class="bird-name">{{ bird.commonName }}</h3>
          <p class="bird-scientific"><em>{{ bird.scientificName }}</em></p>

          <div class="bird-meta">
            <div class="meta-item">
              <span class="meta-label">Family:</span>
              <span class="meta-value">{{ bird.family }}</span>
            </div>

            <div class="meta-item">
              <span class="meta-label">Rarity:</span>
              <span class="meta-value">{{ bird.rarity.replace('_', ' ') }}</span>
            </div>

            <div class="meta-item" v-if="bird.isIntroduced">
              <span class="meta-label">Origin:</span>
              <span class="meta-value">Introduced species</span>
            </div>

            <div class="meta-item" v-if="bird.conservationStatus && Object.keys(bird.conservationStatus).length > 0">
              <span class="meta-label">Conservation:</span>
              <span class="meta-value conservation-status">
                {{ Object.values(bird.conservationStatus)[0] }}
              </span>
            </div>
          </div>

          <button class="attribution-toggle-btn" @click="toggleAttribution">
            ℹ️ {{ showAttribution ? 'Hide' : 'Show' }} Attribution
          </button>

          <div v-if="showAttribution" class="attribution-info">
            <p><strong>Photo:</strong></p>
            <p>{{ photo.source }}</p>
            <p v-if="photo.attribution">By: {{ photo.attribution }}</p>
            <p><a :href="photo.pageUrl" target="_blank" rel="noopener">View original</a></p>
            <p>License: {{ photo.licence }}</p>
          </div>
        </div>
      </div>

      <div class="audio-section" v-if="bird.audio && bird.audio.length > 0">
        <h4>Calls & Songs</h4>
        <div class="audio-list">
          <div
            v-for="(audio, index) in bird.audio.slice(0, 3)"
            :key="index"
            class="audio-item"
          >
            <audio :src="audio.url" controls preload="none" class="audio-player">
              Your browser does not support audio playback.
            </audio>
            <div class="audio-meta">
              <span v-if="audio.type">{{ audio.type }}</span>
              <span v-if="audio.quality" class="audio-quality">Quality: {{ audio.quality }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="photo-gallery" v-if="bird.photos && bird.photos.length > 1">
        <h4>More Photos</h4>
        <div class="gallery-grid">
          <img
            v-for="(p, index) in bird.photos.slice(1, 4)"
            :key="index"
            :src="p.url"
            :alt="`${bird.commonName} photo ${index + 1}`"
            class="gallery-thumbnail"
            @click="window.open(p.pageUrl, '_blank')"
          />
        </div>
      </div>

      <div class="score-breakdown" v-if="isCorrect && scoreBreakdown">
        <h4>Score Breakdown</h4>
        <pre class="breakdown-text">{{ scoreBreakdown }}</pre>
      </div>
    </div>

    <div class="result-actions">
      <button v-if="showNextButton" class="btn btn-primary" @click="emit('next')">
        Next Bird →
      </button>

      <button class="btn btn-secondary" @click="emit('share')">
        📤 Share
      </button>
    </div>
  </div>
</template>

<style scoped>
.results-screen {
  max-width: 800px;
  margin: 0 auto;
}

.result-header {
  text-align: center;
  padding: var(--spacing-xl);
  border-radius: var(--border-radius);
  margin-bottom: var(--spacing-lg);
}

.result-header.correct {
  background-color: #d4edda;
  border: 2px solid var(--color-success);
}

.result-header.incorrect {
  background-color: #f8d7da;
  border: 2px solid var(--color-error);
}

.result-icon {
  font-size: 3rem;
  margin-bottom: var(--spacing-sm);
}

.result-title {
  font-size: 2rem;
  margin-bottom: var(--spacing-sm);
}

.result-score {
  font-size: 1.25rem;
  font-weight: bold;
  color: var(--color-success);
}

.selected-answer {
  text-align: center;
  margin-bottom: var(--spacing-lg);
  color: var(--color-error);
}

.bird-info-card {
  margin-bottom: var(--spacing-lg);
}

.bird-main-info {
  display: flex;
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-lg);
}

.result-bird-image {
  width: 200px;
  height: 200px;
  object-fit: cover;
  border-radius: var(--border-radius);
  flex-shrink: 0;
}

.bird-details {
  flex: 1;
}

.bird-name {
  font-size: 1.5rem;
  color: var(--color-primary);
  margin-bottom: var(--spacing-xs);
}

.bird-scientific {
  color: var(--color-text-light);
  margin-bottom: var(--spacing-md);
}

.bird-meta {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-md);
}

.meta-item {
  display: flex;
  gap: var(--spacing-sm);
}

.meta-label {
  font-weight: 500;
  min-width: 100px;
}

.meta-value {
  color: var(--color-text);
  text-transform: capitalize;
}

.conservation-status {
  color: var(--color-error);
  font-weight: 500;
}

.attribution-toggle-btn {
  padding: var(--spacing-sm) var(--spacing-md);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius);
  background-color: var(--color-bg);
  cursor: pointer;
  font-size: 0.875rem;
  margin-bottom: var(--spacing-sm);
}

.attribution-toggle-btn:hover {
  background-color: var(--color-surface);
}

.attribution-info {
  background-color: var(--color-bg);
  padding: var(--spacing-md);
  border-radius: var(--border-radius);
  font-size: 0.875rem;
  line-height: 1.6;
}

.attribution-info p {
  margin: var(--spacing-xs) 0;
}

.attribution-info a {
  color: var(--color-primary);
}

.audio-section,
.photo-gallery,
.score-breakdown {
  margin-top: var(--spacing-lg);
  padding-top: var(--spacing-lg);
  border-top: 1px solid var(--color-border);
}

.audio-section h4,
.photo-gallery h4,
.score-breakdown h4 {
  color: var(--color-primary);
  margin-bottom: var(--spacing-md);
}

.audio-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.audio-item {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.audio-player {
  width: 100%;
  max-width: 400px;
}

.audio-meta {
  font-size: 0.875rem;
  color: var(--color-text-light);
  display: flex;
  gap: var(--spacing-md);
}

.audio-quality {
  font-weight: 500;
}

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: var(--spacing-md);
}

.gallery-thumbnail {
  width: 100%;
  height: 150px;
  object-fit: cover;
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: transform var(--transition);
}

.gallery-thumbnail:hover {
  transform: scale(1.05);
}

.breakdown-text {
  font-family: monospace;
  white-space: pre-wrap;
  background-color: var(--color-bg);
  padding: var(--spacing-md);
  border-radius: var(--border-radius);
  font-size: 0.875rem;
}

.result-actions {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
}

@media (max-width: 768px) {
  .bird-main-info {
    flex-direction: column;
  }

  .result-bird-image {
    width: 100%;
    height: auto;
  }

  .result-actions {
    flex-direction: column;
  }
}
</style>
