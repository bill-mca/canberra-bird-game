<script setup>
import { ref, onMounted } from 'vue';
import { loadBirdData } from './utils/birdData.js';
import MainMenu from './views/MainMenu.vue';
import DailyChallenge from './views/DailyChallenge.vue';
import FreePlay from './views/FreePlay.vue';
import TimeAttack from './views/TimeAttack.vue';
import LinksPage from './views/LinksPage.vue';
import StatsPage from './views/StatsPage.vue';

const currentView = ref('daily'); // daily, menu, freeplay, timeattack, links, stats
const isLoading = ref(true);
const loadError = ref(null);

onMounted(async () => {
  try {
    await loadBirdData();
    isLoading.value = false;
  } catch (error) {
    console.error('Failed to load bird data:', error);
    loadError.value = 'Failed to load bird data. Please refresh the page.';
    isLoading.value = false;
  }
});

function navigateTo(view) {
  currentView.value = view;
}
</script>

<template>
  <div id="app">
    <header class="app-header">
      <h1 class="app-title" @click="navigateTo('menu')">
        Canberra Bird Game
      </h1>
    </header>

    <main class="app-main">
      <div v-if="isLoading" class="loading">
        <p>Loading birds...</p>
      </div>

      <div v-else-if="loadError" class="error">
        <p>{{ loadError }}</p>
      </div>

      <template v-else>
        <MainMenu v-if="currentView === 'menu'" @navigate="navigateTo" />
        <DailyChallenge v-else-if="currentView === 'daily'" @navigate="navigateTo" />
        <FreePlay v-else-if="currentView === 'freeplay'" @navigate="navigateTo" />
        <TimeAttack v-else-if="currentView === 'timeattack'" @navigate="navigateTo" />
        <LinksPage v-else-if="currentView === 'links'" @navigate="navigateTo" />
        <StatsPage v-else-if="currentView === 'stats'" @navigate="navigateTo" />
      </template>
    </main>

    <footer class="app-footer">
    </footer>
  </div>
</template>

<style>
:root {
  --color-primary: #2c5f2d;
  --color-secondary: #97bc62;
  --color-accent: #ff6b35;
  --color-bg: #f8f9fa;
  --color-surface: #ffffff;
  --color-text: #212529;
  --color-text-light: #6c757d;
  --color-border: #dee2e6;
  --color-success: #28a745;
  --color-error: #dc3545;

  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;

  --border-radius: 8px;
  --transition: 0.2s ease;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background-color: var(--color-bg);
  color: var(--color-text);
  line-height: 1.6;
}

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background-color: var(--color-primary);
  color: white;
  padding: var(--spacing-md);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.app-title {
  font-size: 1.5rem;
  text-align: center;
  cursor: pointer;
  transition: var(--transition);
}

.app-title:hover {
  opacity: 0.9;
}

.app-main {
  flex: 1;
  padding: var(--spacing-lg);
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
}

.app-footer {
  background-color: var(--color-surface);
  border-top: 1px solid var(--color-border);
  padding: var(--spacing-md);
  text-align: center;
  font-size: 0.875rem;
  color: var(--color-text-light);
}

.app-footer a {
  color: var(--color-primary);
  text-decoration: none;
}

.app-footer a:hover {
  text-decoration: underline;
}

.loading,
.error {
  text-align: center;
  padding: var(--spacing-xl);
  font-size: 1.125rem;
}

.error {
  color: var(--color-error);
}

/* Utility classes */
.btn {
  padding: var(--spacing-sm) var(--spacing-lg);
  border: none;
  border-radius: var(--border-radius);
  font-size: 1rem;
  cursor: pointer;
  transition: var(--transition);
  font-weight: 500;
}

.btn-primary {
  background-color: var(--color-primary);
  color: white;
}

.btn-primary:hover {
  background-color: #234d24;
}

.btn-secondary {
  background-color: var(--color-secondary);
  color: var(--color-text);
}

.btn-secondary:hover {
  background-color: #88aa55;
}

.btn-accent {
  background-color: var(--color-accent);
  color: white;
}

.btn-accent:hover {
  background-color: #e55a2b;
}

.card {
  background-color: var(--color-surface);
  border-radius: var(--border-radius);
  padding: var(--spacing-lg);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

@media (max-width: 768px) {
  .app-main {
    padding: var(--spacing-md);
  }

  .app-title {
    font-size: 1.25rem;
  }
}
</style>
