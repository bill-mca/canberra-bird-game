<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';

const props = defineProps({
  bird: {
    type: Object,
    required: true
  },
  photo: {
    type: Object,
    required: true
  },
  options: {
    type: Array,
    required: true
  },
  showHints: {
    type: Boolean,
    default: false
  },
  showTimer: {
    type: Boolean,
    default: false
  },
  score: {
    type: Number,
    default: 0
  },
  questionNumber: {
    type: Number,
    default: null
  },
  totalQuestions: {
    type: Number,
    default: null
  }
});

const emit = defineEmits(['answer', 'skip', 'toggle-hints']);

const startTime = ref(Date.now());
const imageLoaded = ref(false);
const imageError = ref(false);
const elapsedTime = ref(0);
let timerInterval = null;

onMounted(() => {
  if (props.showTimer) {
    timerInterval = setInterval(() => {
      elapsedTime.value = Math.floor((Date.now() - startTime.value) / 1000);
    }, 100);
  }
});

onUnmounted(() => {
  if (timerInterval) {
    clearInterval(timerInterval);
  }
});

const timeElapsed = computed(() => {
  return (Date.now() - startTime.value) / 1000;
});

function selectOption(option) {
  const timeTaken = timeElapsed.value;
  emit('answer', option, timeTaken);
}

function handleImageLoad() {
  imageLoaded.value = true;
}

function handleImageError() {
  imageError.value = true;
  imageLoaded.value = true;
}
</script>

<template>
  <div class="game-screen">
    <div class="game-header">
      <div class="score-display" v-if="score !== null">
        Score: {{ score.toLocaleString() }}
      </div>

      <div class="progress-display" v-if="questionNumber !== null && totalQuestions !== null">
        Question {{ questionNumber }} / {{ totalQuestions }}
      </div>

      <div class="timer-display" v-if="showTimer">
        ⏱️ {{ elapsedTime }}s
      </div>
    </div>

    <div class="bird-image-container">
      <div v-if="!imageLoaded" class="image-loading">
        Loading image...
      </div>

      <div v-if="imageError" class="image-error">
        Failed to load image
      </div>

      <img
        v-show="imageLoaded && !imageError"
        :src="photo.url"
        :alt="'Bird photo'"
        class="bird-image"
        @load="handleImageLoad"
        @error="handleImageError"
      />

      <button
        class="attribution-btn"
        v-if="imageLoaded && photo.attribution"
        :title="`Photo by ${photo.attribution}`"
      >
        ℹ️
      </button>
    </div>

    <div class="hints-section" v-if="showHints">
      <div class="hint-box">
        <p><strong>Family:</strong> {{ bird.family }}</p>
        <p><strong>Rarity:</strong> {{ bird.rarity.replace('_', ' ') }}</p>
      </div>
    </div>

    <div class="options-container">
      <div class="options-grid" :class="`options-${options.length}`">
        <button
          v-for="option in options"
          :key="option.scientificName"
          class="option-btn"
          @click="selectOption(option)"
        >
          {{ option.commonName }}
        </button>
      </div>
    </div>

    <div class="game-actions">
      <button
        class="action-btn hint-btn"
        @click="emit('toggle-hints')"
      >
        💡 {{ showHints ? 'Hide' : 'Show' }} Hints
      </button>

      <button
        class="action-btn skip-btn"
        @click="emit('skip')"
      >
        ⏭️ Skip
      </button>
    </div>
  </div>
</template>

<style scoped>
.game-screen {
  max-width: 900px;
  margin: 0 auto;
}

.game-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
  flex-wrap: wrap;
  gap: var(--spacing-md);
}

.score-display,
.progress-display,
.timer-display {
  font-size: 1.125rem;
  font-weight: 500;
  color: var(--color-primary);
}

.bird-image-container {
  position: relative;
  width: 100%;
  max-width: 700px;
  margin: 0 auto var(--spacing-lg);
  background-color: var(--color-surface);
  border-radius: var(--border-radius);
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bird-image {
  width: 100%;
  height: auto;
  display: block;
  max-height: 500px;
  object-fit: contain;
}

.image-loading,
.image-error {
  text-align: center;
  color: var(--color-text-light);
  padding: var(--spacing-xl);
}

.attribution-btn {
  position: absolute;
  bottom: var(--spacing-sm);
  right: var(--spacing-sm);
  background-color: rgba(0, 0, 0, 0.6);
  color: white;
  border: none;
  border-radius: 50%;
  width: 32px;
  height: 32px;
  cursor: pointer;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hints-section {
  margin-bottom: var(--spacing-lg);
}

.hint-box {
  background-color: #fff3cd;
  border: 1px solid #ffc107;
  border-radius: var(--border-radius);
  padding: var(--spacing-md);
}

.hint-box p {
  margin: var(--spacing-xs) 0;
}

.options-container {
  margin-bottom: var(--spacing-lg);
}

.options-grid {
  display: grid;
  gap: var(--spacing-md);
  max-width: 700px;
  margin: 0 auto;
}

.options-4 {
  grid-template-columns: repeat(2, 1fr);
}

.options-6 {
  grid-template-columns: repeat(2, 1fr);
}

.options-8 {
  grid-template-columns: repeat(2, 1fr);
}

.option-btn {
  padding: var(--spacing-lg);
  background-color: var(--color-surface);
  border: 2px solid var(--color-border);
  border-radius: var(--border-radius);
  font-size: 1rem;
  cursor: pointer;
  transition: all var(--transition);
  font-weight: 500;
}

.option-btn:hover {
  background-color: var(--color-secondary);
  border-color: var(--color-primary);
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.option-btn:active {
  transform: translateY(0);
}

.game-actions {
  display: flex;
  justify-content: space-between;
  gap: var(--spacing-md);
  max-width: 700px;
  margin: 0 auto;
}

.action-btn {
  padding: var(--spacing-sm) var(--spacing-lg);
  border: 2px solid var(--color-border);
  border-radius: var(--border-radius);
  background-color: var(--color-surface);
  cursor: pointer;
  font-size: 1rem;
  transition: all var(--transition);
}

.action-btn:hover {
  border-color: var(--color-primary);
  background-color: var(--color-bg);
}

.hint-btn {
  flex: 1;
}

.skip-btn {
  flex: 1;
}

@media (max-width: 768px) {
  .bird-image-container {
    min-height: 300px;
  }

  .options-6,
  .options-8 {
    grid-template-columns: 1fr;
  }

  .game-actions {
    flex-direction: column;
  }
}
</style>
