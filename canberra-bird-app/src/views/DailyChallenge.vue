<script setup>
import { ref, computed, onMounted } from 'vue';
import { getAllBirds, getRandomPhoto, createMultipleChoiceOptions } from '../utils/birdData.js';
import { getDailyBird } from '../utils/dailySeed.js';
import { isDailyCompleted, getDailyResult, markDailyCompleted, updateDailyStreak, getDailyStreak } from '../utils/storage.js';
import GameScreen from '../components/GameScreen.vue';
import ResultsScreen from '../components/ResultsScreen.vue';

const emit = defineEmits(['navigate']);

const gameState = ref('loading'); // loading, already-completed, playing, results
const dailyBird = ref(null);
const currentPhoto = ref(null);
const options = ref([]);
const selectedBird = ref(null);
const isCorrect = ref(false);
const streak = ref(0);
const usedHints = ref(false);
const showHints = ref(false);
const timeTaken = ref(0);

onMounted(() => {
  initializeDaily();
});

async function initializeDaily() {
  const birds = getAllBirds();

  // Check if already completed today
  if (isDailyCompleted()) {
    const result = getDailyResult();
    dailyBird.value = birds.find(b => b.scientificName === result.birdId);

    if (dailyBird.value) {
      currentPhoto.value = getRandomPhoto(dailyBird.value);
      isCorrect.value = result.isCorrect;
      streak.value = getDailyStreak();
      gameState.value = 'already-completed';
    } else {
      gameState.value = 'loading';
    }
    return;
  }

  // Get today's bird
  dailyBird.value = getDailyBird(birds);

  if (!dailyBird.value) {
    gameState.value = 'error';
    return;
  }

  currentPhoto.value = getRandomPhoto(dailyBird.value);
  options.value = createMultipleChoiceOptions(birds, dailyBird.value, 4, 'beginner');
  gameState.value = 'playing';
}

function handleAnswer(selectedOption, timeSeconds) {
  selectedBird.value = selectedOption;
  timeTaken.value = timeSeconds;

  isCorrect.value = selectedOption.scientificName === dailyBird.value.scientificName;

  // Update streak and mark as completed
  streak.value = updateDailyStreak(isCorrect.value);
  markDailyCompleted(dailyBird.value.scientificName, isCorrect.value);

  gameState.value = 'results';
}

function handleSkip() {
  // Skipping counts as incorrect
  selectedBird.value = null;
  isCorrect.value = false;
  streak.value = updateDailyStreak(false);
  markDailyCompleted(dailyBird.value.scientificName, false);
  gameState.value = 'results';
}

function toggleHints() {
  showHints.value = !showHints.value;
  if (showHints.value) {
    usedHints.value = true;
  }
}

function handleShare() {
  const today = new Date().toLocaleDateString();
  const emoji = isCorrect.value ? '✅' : '❌';
  const text = `Canberra Bird Game - Daily Challenge ${today}\n\n${emoji} ${isCorrect.value ? 'Correct!' : 'Incorrect'}\n🔥 Streak: ${streak.value}\n\nCan you identify today's bird?\n`;

  if (navigator.share) {
    navigator.share({
      title: 'Canberra Bird Game',
      text: text
    }).catch(err => console.log('Share cancelled'));
  } else {
    // Fallback: copy to clipboard
    navigator.clipboard.writeText(text).then(() => {
      alert('Results copied to clipboard!');
    });
  }
}

function goToMenu() {
  emit('navigate', 'menu');
}
</script>

<template>
  <div class="daily-challenge">
    <div class="page-header">
      <h2>📅 Daily Challenge</h2>
      <p>One bird per day. Build your streak!</p>
    </div>

    <div v-if="gameState === 'loading'" class="loading">
      <p>Loading today's challenge...</p>
    </div>

    <div v-else-if="gameState === 'already-completed'" class="already-completed">
      <div class="completed-message card">
        <h3>✅ Today's Challenge Complete!</h3>
        <p>You {{ isCorrect ? 'correctly identified' : 'attempted' }} today's bird:</p>
        <h4>{{ dailyBird.commonName }}</h4>
        <img v-if="currentPhoto" :src="currentPhoto.url" :alt="dailyBird.commonName" class="completed-bird-image" />
        <p class="streak-info">🔥 Current Streak: {{ streak }} day{{ streak !== 1 ? 's' : '' }}</p>
        <p class="comeback-text">Come back tomorrow for a new challenge!</p>
        <button class="btn btn-primary" @click="goToMenu">Go to Main Menu</button>
      </div>
    </div>

    <GameScreen
      v-else-if="gameState === 'playing'"
      :bird="dailyBird"
      :photo="currentPhoto"
      :options="options"
      :show-hints="showHints"
      :show-timer="true"
      @answer="handleAnswer"
      @skip="handleSkip"
      @toggle-hints="toggleHints"
    />

    <div v-else-if="gameState === 'results'">
      <ResultsScreen
        :bird="dailyBird"
        :photo="currentPhoto"
        :selected-bird="selectedBird"
        :is-correct="isCorrect"
        :show-next-button="false"
        @share="handleShare"
      />

      <div class="streak-card card">
        <h3>🔥 Daily Streak</h3>
        <p class="streak-number">{{ streak }}</p>
        <p class="streak-label">day{{ streak !== 1 ? 's' : '' }}</p>
        <p class="comeback-text">Come back tomorrow to continue your streak!</p>
      </div>

      <div class="daily-actions">
        <button class="btn btn-primary btn-large" @click="goToMenu">← Back to Main Menu</button>
        <button class="btn btn-secondary" @click="handleShare">📤 Share Results</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.daily-challenge {
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

.loading {
  text-align: center;
  padding: var(--spacing-xl);
  font-size: 1.125rem;
}

.already-completed {
  max-width: 600px;
  margin: 0 auto;
}

.completed-message {
  text-align: center;
}

.completed-message h3 {
  color: var(--color-success);
  margin-bottom: var(--spacing-md);
  font-size: 1.5rem;
}

.completed-message h4 {
  color: var(--color-primary);
  font-size: 1.25rem;
  margin: var(--spacing-md) 0;
}

.completed-bird-image {
  width: 100%;
  max-width: 400px;
  height: auto;
  border-radius: var(--border-radius);
  margin: var(--spacing-lg) 0;
}

.streak-info {
  font-size: 1.25rem;
  font-weight: bold;
  color: var(--color-accent);
  margin: var(--spacing-md) 0;
}

.comeback-text {
  color: var(--color-text-light);
  margin: var(--spacing-lg) 0;
}

.streak-card {
  text-align: center;
  margin: var(--spacing-xl) auto;
  max-width: 400px;
  background: linear-gradient(135deg, #ff6b35, #ff8555);
  color: white;
}

.streak-card h3 {
  font-size: 1.5rem;
  margin-bottom: var(--spacing-md);
}

.streak-number {
  font-size: 4rem;
  font-weight: bold;
  line-height: 1;
  margin: var(--spacing-md) 0;
}

.streak-label {
  font-size: 1.25rem;
  margin-bottom: var(--spacing-lg);
}

.daily-actions {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
  margin-top: var(--spacing-xl);
}

.btn-large {
  font-size: 1.125rem;
  padding: 0.75rem 2rem;
}

@media (max-width: 768px) {
  .daily-actions {
    flex-direction: column;
  }
}
</style>
