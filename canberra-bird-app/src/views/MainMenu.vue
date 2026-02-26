<script setup>
import { getDailyStreak, getStats } from '../utils/storage.js';

const emit = defineEmits(['navigate']);

const streak = getDailyStreak();
const stats = getStats();
</script>

<template>
  <div class="main-menu">
    <div class="welcome-section">
      <h2>Welcome to Bird Guesser!</h2>
      <p>Test your knowledge of the 297 bird species found in the Australian Capital Territory.</p>
    </div>

    <div class="streak-display" v-if="streak > 0">
      <p>🔥 Current streak: <strong>{{ streak }}</strong> day{{ streak !== 1 ? 's' : '' }}</p>
    </div>

    <div class="menu-grid">
      <button class="menu-btn daily-btn" @click="emit('navigate', 'daily')">
        <span class="menu-icon">📅</span>
        <h3>Daily Challenge</h3>
        <p>One bird per day, build your streak!</p>
      </button>

      <button class="menu-btn freeplay-btn" @click="emit('navigate', 'freeplay')">
        <span class="menu-icon">🎮</span>
        <h3>Free Play</h3>
        <p>Customize your practice session</p>
      </button>

      <button class="menu-btn timeattack-btn" @click="emit('navigate', 'timeattack')">
        <span class="menu-icon">⏱️</span>
        <h3>Time Attack</h3>
        <p>How many can you identify in 60 seconds?</p>
      </button>

      <button class="menu-btn stats-btn" @click="emit('navigate', 'stats')">
        <span class="menu-icon">📊</span>
        <h3>Statistics</h3>
        <p>View your progress and achievements</p>
      </button>

      <button class="menu-btn links-btn" @click="emit('navigate', 'links')">
        <span class="menu-icon">🔗</span>
        <h3>Birding Resources</h3>
        <p>Canberra birding links and info</p>
      </button>

      <button class="menu-btn about-btn" @click="emit('navigate', 'about')">
        <span class="menu-icon">ℹ️</span>
        <h3>About</h3>
        <p>Learn more about this game</p>
      </button>
    </div>
  </div>
</template>

<style scoped>
.main-menu {
  max-width: 800px;
  margin: 0 auto;
}

.welcome-section {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.welcome-section h2 {
  color: var(--color-primary);
  margin-bottom: var(--spacing-md);
}

.streak-display {
  background: linear-gradient(135deg, #ff6b35, #ff8555);
  color: white;
  padding: var(--spacing-md);
  border-radius: var(--border-radius);
  text-align: center;
  margin-bottom: var(--spacing-xl);
  font-size: 1.125rem;
}

.menu-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
}

.menu-btn {
  background-color: var(--color-surface);
  border: 2px solid var(--color-border);
  border-radius: var(--border-radius);
  padding: var(--spacing-xl);
  cursor: pointer;
  transition: all var(--transition);
  text-align: center;
  min-height: 180px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.menu-btn:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  border-color: var(--color-primary);
}

.menu-icon {
  font-size: 3rem;
  margin-bottom: var(--spacing-md);
}

.menu-btn h3 {
  color: var(--color-primary);
  margin-bottom: var(--spacing-sm);
  font-size: 1.25rem;
}

.menu-btn p {
  color: var(--color-text-light);
  font-size: 0.875rem;
}

.quick-stats {
  background-color: var(--color-surface);
  border-radius: var(--border-radius);
  padding: var(--spacing-lg);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.quick-stats h3 {
  text-align: center;
  color: var(--color-primary);
  margin-bottom: var(--spacing-md);
}

.stats-row {
  display: flex;
  justify-content: space-around;
  gap: var(--spacing-md);
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--color-primary);
}

.stat-label {
  font-size: 0.875rem;
  color: var(--color-text-light);
}

@media (max-width: 768px) {
  .menu-grid {
    grid-template-columns: 1fr;
  }

  .menu-btn {
    min-height: 150px;
  }

  .stats-row {
    flex-direction: column;
    gap: var(--spacing-sm);
  }
}
</style>
