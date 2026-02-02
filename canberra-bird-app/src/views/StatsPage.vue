<script setup>
import { ref } from 'vue';
import { getStats, getDailyStreak, resetAllData, exportData } from '../utils/storage.js';

const emit = defineEmits(['navigate']);

const stats = ref(getStats());
const streak = ref(getDailyStreak());

function handleReset() {
  if (confirm('Are you sure you want to reset all your statistics? This cannot be undone.')) {
    resetAllData();
    stats.value = getStats();
    streak.value = getDailyStreak();
  }
}

function handleExport() {
  const data = exportData();
  const blob = new Blob([data], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `canberra-birds-stats-${new Date().toISOString().split('T')[0]}.json`;
  a.click();
  URL.revokeObjectURL(url);
}

function goToMenu() {
  emit('navigate', 'menu');
}
</script>

<template>
  <div class="stats-page">
    <div class="page-header">
      <h2>📊 Your Statistics</h2>
      <p>Track your bird identification journey</p>
    </div>

    <div class="stats-container">
      <!-- Daily Challenge Stats -->
      <div class="stat-card card">
        <h3>📅 Daily Challenge</h3>

        <div class="stat-row">
          <div class="stat-item">
            <div class="stat-value">{{ streak }}</div>
            <div class="stat-label">Current Streak</div>
          </div>

          <div class="stat-item">
            <div class="stat-value">{{ stats.bestStreak }}</div>
            <div class="stat-label">Best Streak</div>
          </div>

          <div class="stat-item">
            <div class="stat-value">{{ stats.dailyChallengesCompleted }}</div>
            <div class="stat-label">Completed</div>
          </div>
        </div>
      </div>

      <!-- Overall Stats -->
      <div class="stat-card card">
        <h3>🎮 Overall Performance</h3>

        <div class="stat-row">
          <div class="stat-item">
            <div class="stat-value">{{ stats.totalGames }}</div>
            <div class="stat-label">Games Played</div>
          </div>

          <div class="stat-item">
            <div class="stat-value">{{ stats.totalQuestions }}</div>
            <div class="stat-label">Total Questions</div>
          </div>
        </div>

        <div class="stat-row">
          <div class="stat-item">
            <div class="stat-value">{{ stats.correctAnswers }}</div>
            <div class="stat-label">Correct Answers</div>
          </div>

          <div class="stat-item">
            <div class="stat-value">
              {{ stats.totalQuestions > 0 ? Math.round((stats.correctAnswers / stats.totalQuestions) * 100) : 0 }}%
            </div>
            <div class="stat-label">Accuracy</div>
          </div>
        </div>
      </div>

      <!-- Score Stats -->
      <div class="stat-card card">
        <h3>💯 Scoring</h3>

        <div class="stat-row">
          <div class="stat-item">
            <div class="stat-value">{{ stats.totalScore.toLocaleString() }}</div>
            <div class="stat-label">Total Score</div>
          </div>

          <div class="stat-item">
            <div class="stat-value">
              {{ stats.totalQuestions > 0 ? Math.round(stats.totalScore / stats.totalQuestions) : 0 }}
            </div>
            <div class="stat-label">Avg Per Question</div>
          </div>
        </div>
      </div>

      <!-- Progress Summary -->
      <div class="progress-card card" v-if="stats.totalQuestions > 0">
        <h3>📈 Progress Summary</h3>

        <div class="progress-item">
          <div class="progress-label">Accuracy Rate</div>
          <div class="progress-bar">
            <div
              class="progress-fill"
              :style="{ width: `${(stats.correctAnswers / stats.totalQuestions) * 100}%` }"
            ></div>
          </div>
          <div class="progress-value">
            {{ Math.round((stats.correctAnswers / stats.totalQuestions) * 100) }}%
          </div>
        </div>

        <div class="achievement-text">
          <p v-if="stats.correctAnswers / stats.totalQuestions >= 0.9">
            🌟 Outstanding! You're a bird identification expert!
          </p>
          <p v-else-if="stats.correctAnswers / stats.totalQuestions >= 0.7">
            🎯 Great job! You have strong bird identification skills!
          </p>
          <p v-else-if="stats.correctAnswers / stats.totalQuestions >= 0.5">
            📚 Good progress! Keep practicing to improve!
          </p>
          <p v-else>
            🌱 Just getting started! Every expert was once a beginner!
          </p>
        </div>
      </div>

      <!-- Empty State -->
      <div class="empty-state card" v-else>
        <h3>No statistics yet!</h3>
        <p>Play some games to start tracking your progress.</p>
        <button class="btn btn-primary" @click="emit('navigate', 'menu')">
          Start Playing
        </button>
      </div>
    </div>

    <div class="actions-section">
      <button class="btn btn-secondary" @click="handleExport">
        💾 Export Data
      </button>

      <button class="btn btn-secondary" @click="handleReset" style="background-color: var(--color-error); color: white;">
        🗑️ Reset All Stats
      </button>
    </div>

    <div class="page-actions">
      <button class="btn btn-primary" @click="goToMenu">
        ← Back to Main Menu
      </button>
    </div>
  </div>
</template>

<style scoped>
.stats-page {
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

.stats-container {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
}

.stat-card h3,
.progress-card h3 {
  color: var(--color-primary);
  margin-bottom: var(--spacing-lg);
  font-size: 1.25rem;
}

.stat-row {
  display: flex;
  justify-content: space-around;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.stat-row:last-child {
  margin-bottom: 0;
}

.stat-item {
  text-align: center;
  flex: 1;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: bold;
  color: var(--color-primary);
  line-height: 1;
}

.stat-label {
  font-size: 0.875rem;
  color: var(--color-text-light);
  margin-top: var(--spacing-sm);
}

.progress-item {
  margin-bottom: var(--spacing-lg);
}

.progress-label {
  font-weight: 500;
  margin-bottom: var(--spacing-sm);
  color: var(--color-text);
}

.progress-bar {
  width: 100%;
  height: 24px;
  background-color: var(--color-bg);
  border-radius: var(--border-radius);
  overflow: hidden;
  margin-bottom: var(--spacing-xs);
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--color-primary), var(--color-secondary));
  transition: width 0.3s ease;
}

.progress-value {
  text-align: right;
  font-weight: bold;
  color: var(--color-primary);
}

.achievement-text {
  text-align: center;
  margin-top: var(--spacing-lg);
  padding: var(--spacing-md);
  background-color: #fff3cd;
  border-radius: var(--border-radius);
  font-weight: 500;
}

.empty-state {
  text-align: center;
  padding: var(--spacing-xl);
}

.empty-state h3 {
  color: var(--color-text-light);
  margin-bottom: var(--spacing-md);
}

.empty-state p {
  color: var(--color-text-light);
  margin-bottom: var(--spacing-lg);
}

.actions-section {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
  margin-bottom: var(--spacing-xl);
}

.page-actions {
  text-align: center;
}

@media (max-width: 768px) {
  .stat-row {
    flex-direction: column;
  }

  .actions-section {
    flex-direction: column;
  }
}
</style>
