<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import {
  getAllBirds,
  filterByDifficulty,
  getRandomBird,
  getRandomPhoto,
  createMultipleChoiceOptions,
  DIFFICULTY_LEVELS
} from '../utils/birdData.js';
import { calculateScore, calculateSessionStats } from '../utils/scoring.js';
import { updateStats } from '../utils/storage.js';

const emit = defineEmits(['navigate']);

const gameState = ref('setup'); // setup, countdown, playing, results
const difficulty = ref('beginner');
const timeLimit = ref(60); // seconds
const timeRemaining = ref(60);
const currentBird = ref(null);
const currentPhoto = ref(null);
const options = ref([]);
const totalScore = ref(0);
const correctCount = ref(0);
const questionCount = ref(0);
const sessionResults = ref([]);

let timerInterval = null;

const difficultyConfig = computed(() => DIFFICULTY_LEVELS[difficulty.value]);

const filteredBirds = computed(() => {
  return filterByDifficulty(getAllBirds(), difficulty.value);
});

function startGame() {
  sessionResults.value = [];
  totalScore.value = 0;
  correctCount.value = 0;
  questionCount.value = 0;
  timeRemaining.value = timeLimit.value;
  gameState.value = 'countdown';

  // Start countdown
  let count = 3;
  const countdownInterval = setInterval(() => {
    count--;
    if (count === 0) {
      clearInterval(countdownInterval);
      gameState.value = 'playing';
      loadNextQuestion();
      startTimer();
    }
  }, 1000);
}

function startTimer() {
  timerInterval = setInterval(() => {
    timeRemaining.value--;

    if (timeRemaining.value <= 0) {
      endGame();
    }
  }, 1000);
}

function loadNextQuestion() {
  questionCount.value++;
  currentBird.value = getRandomBird(filteredBirds.value);
  currentPhoto.value = getRandomPhoto(currentBird.value);
  options.value = createMultipleChoiceOptions(
    filteredBirds.value,
    currentBird.value,
    difficultyConfig.value.optionCount
  );
}

function handleAnswer(selectedOption) {
  const isCorrect = selectedOption.scientificName === currentBird.value.scientificName;

  let questionScore = 0;
  if (isCorrect) {
    correctCount.value++;
    // Faster scoring in time attack mode
    questionScore = calculateScore(currentBird.value, {
      audioOnly: false,
      usedHints: false,
      timeSeconds: 0
    });
    totalScore.value += questionScore;
  }

  sessionResults.value.push({
    bird: currentBird.value,
    selectedBird: selectedOption,
    isCorrect: isCorrect,
    score: questionScore,
    timeSeconds: 0,
    usedHints: false
  });

  // Load next question immediately
  if (timeRemaining.value > 0) {
    loadNextQuestion();
  } else {
    endGame();
  }
}

function endGame() {
  if (timerInterval) {
    clearInterval(timerInterval);
    timerInterval = null;
  }

  const stats = calculateSessionStats(sessionResults.value);
  updateStats({
    ...stats,
    totalScore: totalScore.value,
    isDaily: false
  });

  gameState.value = 'results';
}

function handleShare() {
  const accuracy = questionCount.value > 0
    ? Math.round((correctCount.value / questionCount.value) * 100)
    : 0;

  const text = `Canberra Bird Game - Time Attack\n\n` +
    `⏱️ ${timeLimit.value} seconds\n` +
    `🎯 ${correctCount.value}/${questionCount.value} correct (${accuracy}%)\n` +
    `💯 Score: ${totalScore.value.toLocaleString()}\n\n` +
    `Can you beat my score?\n`;

  if (navigator.share) {
    navigator.share({
      title: 'Canberra Bird Game - Time Attack',
      text: text
    }).catch(err => console.log('Share cancelled'));
  } else {
    navigator.clipboard.writeText(text).then(() => {
      alert('Results copied to clipboard!');
    });
  }
}

function backToSetup() {
  gameState.value = 'setup';
}

function goToMenu() {
  emit('navigate', 'menu');
}

onUnmounted(() => {
  if (timerInterval) {
    clearInterval(timerInterval);
  }
});
</script>

<template>
  <div class="time-attack">
    <div class="page-header">
      <h2>⏱️ Time Attack</h2>
      <p>How many birds can you identify in {{ timeLimit }} seconds?</p>
    </div>

    <!-- Setup Screen -->
    <div v-if="gameState === 'setup'" class="setup-screen">
      <div class="setup-card card">
        <h3>Game Settings</h3>

        <div class="setting-group">
          <label>Difficulty Level</label>
          <div class="difficulty-buttons">
            <button
              v-for="(config, key) in DIFFICULTY_LEVELS"
              :key="key"
              class="difficulty-btn"
              :class="{ active: difficulty === key }"
              @click="difficulty = key"
            >
              {{ config.emoji }} {{ config.name }}
            </button>
          </div>
        </div>

        <div class="setting-group">
          <label>Time Limit</label>
          <select v-model.number="timeLimit" class="select-input">
            <option :value="30">30 seconds</option>
            <option :value="60">60 seconds</option>
            <option :value="120">2 minutes</option>
            <option :value="180">3 minutes</option>
          </select>
        </div>

        <button class="btn btn-primary btn-large" @click="startGame">
          Start Game
        </button>

        <button class="btn btn-secondary" @click="goToMenu">
          Back to Menu
        </button>
      </div>
    </div>

    <!-- Countdown Screen -->
    <div v-else-if="gameState === 'countdown'" class="countdown-screen">
      <div class="countdown-number">
        {{ Math.ceil(timeRemaining - (timeLimit - 3)) }}
      </div>
      <p>Get ready!</p>
    </div>

    <!-- Playing Screen -->
    <div v-else-if="gameState === 'playing'" class="playing-screen">
      <div class="game-header">
        <div class="timer-display" :class="{ warning: timeRemaining <= 10 }">
          ⏱️ {{ timeRemaining }}s
        </div>

        <div class="score-display">
          Score: {{ totalScore.toLocaleString() }}
        </div>

        <div class="count-display">
          Identified: {{ correctCount }}
        </div>
      </div>

      <div class="bird-image-container">
        <img
          v-if="currentPhoto"
          :src="currentPhoto.url"
          :alt="'Bird photo'"
          class="bird-image"
        />
      </div>

      <div class="options-container">
        <div class="options-grid" :class="`options-${options.length}`">
          <button
            v-for="option in options"
            :key="option.scientificName"
            class="option-btn"
            @click="handleAnswer(option)"
          >
            {{ option.commonName }}
          </button>
        </div>
      </div>
    </div>

    <!-- Results Screen -->
    <div v-else-if="gameState === 'results'" class="results-screen">
      <div class="results-card card">
        <h2>⏱️ Time's Up!</h2>

        <div class="final-stats">
          <div class="stat-big">
            <div class="stat-value">{{ correctCount }}</div>
            <div class="stat-label">Birds Identified</div>
          </div>

          <div class="stat-big">
            <div class="stat-value">{{ questionCount }}</div>
            <div class="stat-label">Total Attempts</div>
          </div>

          <div class="stat-big">
            <div class="stat-value">{{ totalScore.toLocaleString() }}</div>
            <div class="stat-label">Total Score</div>
          </div>

          <div class="stat-big">
            <div class="stat-value">
              {{ questionCount > 0 ? Math.round((correctCount / questionCount) * 100) : 0 }}%
            </div>
            <div class="stat-label">Accuracy</div>
          </div>
        </div>

        <div class="results-actions">
          <button class="btn btn-primary" @click="backToSetup">Play Again</button>
          <button class="btn btn-secondary" @click="handleShare">📤 Share Results</button>
          <button class="btn btn-secondary" @click="goToMenu">Main Menu</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.time-attack {
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

.setup-screen {
  max-width: 600px;
  margin: 0 auto;
}

.setup-card h3 {
  color: var(--color-primary);
  margin-bottom: var(--spacing-lg);
  text-align: center;
}

.setting-group {
  margin-bottom: var(--spacing-lg);
}

.setting-group label {
  display: block;
  font-weight: 500;
  margin-bottom: var(--spacing-sm);
}

.difficulty-buttons {
  display: flex;
  gap: var(--spacing-sm);
}

.difficulty-btn {
  flex: 1;
  padding: var(--spacing-md);
  border: 2px solid var(--color-border);
  border-radius: var(--border-radius);
  background-color: var(--color-surface);
  cursor: pointer;
  transition: all var(--transition);
}

.difficulty-btn.active {
  border-color: var(--color-primary);
  background-color: var(--color-secondary);
}

.difficulty-btn:hover {
  border-color: var(--color-primary);
}

.select-input {
  width: 100%;
  padding: var(--spacing-sm);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius);
  font-size: 1rem;
}

.btn-large {
  width: 100%;
  padding: var(--spacing-md) var(--spacing-lg);
  font-size: 1.125rem;
  margin-bottom: var(--spacing-md);
}

.countdown-screen {
  text-align: center;
  padding: var(--spacing-xl);
}

.countdown-number {
  font-size: 8rem;
  font-weight: bold;
  color: var(--color-accent);
  line-height: 1;
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

.playing-screen {
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

.timer-display {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--color-primary);
  padding: var(--spacing-sm) var(--spacing-md);
  background-color: var(--color-surface);
  border-radius: var(--border-radius);
  border: 2px solid var(--color-border);
}

.timer-display.warning {
  color: var(--color-error);
  border-color: var(--color-error);
  animation: blink 0.5s infinite;
}

@keyframes blink {
  50% {
    opacity: 0.5;
  }
}

.score-display,
.count-display {
  font-size: 1.125rem;
  font-weight: 500;
  color: var(--color-text);
}

.bird-image-container {
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
}

.option-btn:active {
  transform: translateY(0);
}

.results-screen {
  max-width: 700px;
  margin: 0 auto;
}

.results-card h2 {
  text-align: center;
  color: var(--color-primary);
  margin-bottom: var(--spacing-xl);
  font-size: 2rem;
}

.final-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
}

.stat-big {
  text-align: center;
  padding: var(--spacing-lg);
  background-color: var(--color-bg);
  border-radius: var(--border-radius);
}

.stat-big .stat-value {
  font-size: 2.5rem;
  font-weight: bold;
  color: var(--color-primary);
  line-height: 1;
}

.stat-big .stat-label {
  font-size: 0.875rem;
  color: var(--color-text-light);
  margin-top: var(--spacing-sm);
}

.results-actions {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

@media (max-width: 768px) {
  .bird-image-container {
    min-height: 300px;
  }

  .options-6,
  .options-8 {
    grid-template-columns: 1fr;
  }

  .final-stats {
    grid-template-columns: 1fr;
  }
}
</style>
