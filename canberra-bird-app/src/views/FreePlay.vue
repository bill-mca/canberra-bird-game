<script setup>
import { ref, computed } from 'vue';
import {
  getAllBirds,
  filterByDifficulty,
  filterByFamily,
  filterByRarity,
  filterByConservation,
  filterByOrigin,
  getAllFamilies,
  getRandomBird,
  getRandomPhoto,
  createMultipleChoiceOptions,
  DIFFICULTY_LEVELS
} from '../utils/birdData.js';
import { calculateSessionStats } from '../utils/scoring.js';
import { updateStats } from '../utils/storage.js';
import GameScreen from '../components/GameScreen.vue';
import ResultsScreen from '../components/ResultsScreen.vue';

const emit = defineEmits(['navigate']);

const gameState = ref('setup'); // setup, playing, results, session-complete
const difficulty = ref('beginner');
const selectedFamilies = ref([]);
const selectedRarities = ref([]);
const showConservationOnly = ref(false);
const nativeOnly = ref(false);
const numberOfQuestions = ref(10);

const currentBird = ref(null);
const currentPhoto = ref(null);
const options = ref([]);
const currentQuestionNumber = ref(0);
const sessionResults = ref([]);
const usedHints = ref(false);
const showHints = ref(false);
const selectedBird = ref(null);
const isCorrect = ref(false);
const timeTaken = ref(0);

const allFamilies = computed(() => getAllFamilies(getAllBirds()));

const filteredBirds = computed(() => {
  let birds = getAllBirds();

  // Apply difficulty filter
  birds = filterByDifficulty(birds, difficulty.value);

  // Apply family filter
  if (selectedFamilies.value.length > 0) {
    birds = filterByFamily(birds, selectedFamilies.value);
  }

  // Apply rarity filter
  if (selectedRarities.value.length > 0) {
    birds = filterByRarity(birds, selectedRarities.value);
  }

  // Apply conservation filter
  if (showConservationOnly.value) {
    birds = filterByConservation(birds, true);
  }

  // Apply origin filter
  if (nativeOnly.value) {
    birds = filterByOrigin(birds, true);
  }

  return birds;
});

const difficultyConfig = computed(() => DIFFICULTY_LEVELS[difficulty.value]);

function startGame() {
  if (filteredBirds.value.length < 4) {
    alert('Not enough birds match your filters. Please adjust your settings.');
    return;
  }

  sessionResults.value = [];
  currentQuestionNumber.value = 0;
  gameState.value = 'playing';
  loadNextQuestion();
}

function loadNextQuestion() {
  currentQuestionNumber.value++;

  if (currentQuestionNumber.value > numberOfQuestions.value) {
    completeSession();
    return;
  }

  usedHints.value = false;
  showHints.value = false;

  currentBird.value = getRandomBird(filteredBirds.value);
  currentPhoto.value = getRandomPhoto(currentBird.value);
  options.value = createMultipleChoiceOptions(
    filteredBirds.value,
    currentBird.value,
    difficultyConfig.value.optionCount,
    difficulty.value
  );
}

function handleAnswer(selectedOption, timeSeconds) {
  selectedBird.value = selectedOption;
  timeTaken.value = timeSeconds;

  isCorrect.value = selectedOption.scientificName === currentBird.value.scientificName;

  sessionResults.value.push({
    bird: currentBird.value,
    selectedBird: selectedOption,
    isCorrect: isCorrect.value,
    timeSeconds: timeSeconds,
    usedHints: usedHints.value
  });

  gameState.value = 'results';
}

function handleSkip() {
  selectedBird.value = null;
  isCorrect.value = false;

  sessionResults.value.push({
    bird: currentBird.value,
    selectedBird: null,
    isCorrect: false,
    timeSeconds: 0,
    usedHints: usedHints.value
  });

  gameState.value = 'results';
}

function toggleHints() {
  showHints.value = !showHints.value;
  if (showHints.value) {
    usedHints.value = true;
  }
}

function nextQuestion() {
  gameState.value = 'playing';
  loadNextQuestion();
}

function completeSession() {
  const stats = calculateSessionStats(sessionResults.value);
  updateStats({
    ...stats,
    isDaily: false
  });
  gameState.value = 'session-complete';
}

function handleShare() {
  const stats = calculateSessionStats(sessionResults.value);
  const text = `Bird Guesser - Free Play\n\n` +
    `✅ ${stats.correctAnswers}/${stats.totalQuestions} correct (${stats.accuracy}%)\n` +
    `⏱️ Avg time: ${stats.averageTime}s\n\n` +
    `Can you beat your score?\n`;

  if (navigator.share) {
    navigator.share({
      title: 'Bird Guesser',
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
</script>

<template>
  <div class="free-play">
    <div class="page-header">
      <h2>🎮 Free Play</h2>
      <p>Customize your practice session</p>
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
              <span class="difficulty-desc">{{ config.description }}</span>
            </button>
          </div>
        </div>

        <div class="setting-group">
          <label>Number of Questions</label>
          <select v-model.number="numberOfQuestions" class="select-input">
            <option :value="5">5 questions</option>
            <option :value="10">10 questions</option>
            <option :value="20">20 questions</option>
            <option :value="50">50 questions</option>
          </select>
        </div>

        <div class="setting-group">
          <label>
            <input type="checkbox" v-model="nativeOnly" />
            Native species only
          </label>
        </div>

        <div class="setting-group">
          <label>
            <input type="checkbox" v-model="showConservationOnly" />
            Threatened species only
          </label>
        </div>

        <div class="birds-count">
          Available birds: <strong>{{ filteredBirds.length }}</strong>
        </div>

        <button class="btn btn-primary btn-large" @click="startGame" :disabled="filteredBirds.length < 4">
          Start Game
        </button>

        <button class="btn btn-secondary" @click="goToMenu">
          Back to Menu
        </button>
      </div>
    </div>

    <!-- Playing Screen -->
    <GameScreen
      v-else-if="gameState === 'playing'"
      :bird="currentBird"
      :photo="currentPhoto"
      :options="options"
      :show-hints="showHints"
      :show-timer="true"
      :question-number="currentQuestionNumber"
      :total-questions="numberOfQuestions"
      @answer="handleAnswer"
      @skip="handleSkip"
      @toggle-hints="toggleHints"
    />

    <!-- Results Screen -->
    <div v-else-if="gameState === 'results'">
      <ResultsScreen
        :bird="currentBird"
        :photo="currentPhoto"
        :selected-bird="selectedBird"
        :is-correct="isCorrect"
        @next="nextQuestion"
      />
    </div>

    <!-- Session Complete Screen -->
    <div v-else-if="gameState === 'session-complete'" class="session-complete">
      <div class="complete-card card">
        <h2>🎉 Session Complete!</h2>

        <div class="final-stats">
          <div class="stat-big">
            <div class="stat-value">{{ calculateSessionStats(sessionResults).correctAnswers }}/{{ numberOfQuestions }}</div>
            <div class="stat-label">Correct Answers</div>
          </div>

          <div class="stat-big">
            <div class="stat-value">{{ calculateSessionStats(sessionResults).accuracy }}%</div>
            <div class="stat-label">Accuracy</div>
          </div>

          <div class="stat-big">
            <div class="stat-value">{{ calculateSessionStats(sessionResults).averageTime }}s</div>
            <div class="stat-label">Avg Time</div>
          </div>
        </div>

        <div class="complete-actions">
          <button class="btn btn-primary" @click="backToSetup">Play Again</button>
          <button class="btn btn-secondary" @click="handleShare">📤 Share Results</button>
          <button class="btn btn-secondary" @click="goToMenu">Main Menu</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.free-play {
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
  flex-direction: column;
  gap: var(--spacing-sm);
}

.difficulty-btn {
  padding: var(--spacing-md);
  border: 2px solid var(--color-border);
  border-radius: var(--border-radius);
  background-color: var(--color-surface);
  cursor: pointer;
  transition: all var(--transition);
  text-align: left;
}

.difficulty-btn.active {
  border-color: var(--color-primary);
  background-color: var(--color-secondary);
}

.difficulty-btn:hover {
  border-color: var(--color-primary);
}

.difficulty-desc {
  display: block;
  font-size: 0.875rem;
  color: var(--color-text-light);
  margin-top: var(--spacing-xs);
}

.select-input {
  width: 100%;
  padding: var(--spacing-sm);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius);
  font-size: 1rem;
}

.birds-count {
  text-align: center;
  margin: var(--spacing-lg) 0;
  font-size: 1.125rem;
  color: var(--color-primary);
}

.btn-large {
  width: 100%;
  padding: var(--spacing-md) var(--spacing-lg);
  font-size: 1.125rem;
  margin-bottom: var(--spacing-md);
}

.session-complete {
  max-width: 700px;
  margin: 0 auto;
}

.complete-card h2 {
  text-align: center;
  color: var(--color-success);
  margin-bottom: var(--spacing-xl);
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

.complete-actions {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

@media (max-width: 768px) {
  .final-stats {
    grid-template-columns: 1fr;
  }
}
</style>
