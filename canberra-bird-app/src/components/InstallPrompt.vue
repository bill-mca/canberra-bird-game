<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue';

const DISMISS_KEY = 'canberra_birds_install_dismissed';

const deferredPrompt = ref(null);
const dismissed = ref(localStorage.getItem(DISMISS_KEY) === 'true');
const isIOS = ref(false);
const isStandalone = ref(false);

const showBanner = computed(() => {
  if (dismissed.value || isStandalone.value) return false;
  return deferredPrompt.value !== null || isIOS.value;
});

function onBeforeInstallPrompt(e) {
  e.preventDefault();
  deferredPrompt.value = e;
}

async function install() {
  if (!deferredPrompt.value) return;
  deferredPrompt.value.prompt();
  const { outcome } = await deferredPrompt.value.userChoice;
  if (outcome === 'accepted') {
    deferredPrompt.value = null;
  }
}

function dismiss() {
  dismissed.value = true;
  localStorage.setItem(DISMISS_KEY, 'true');
}

onMounted(() => {
  isStandalone.value =
    window.matchMedia('(display-mode: standalone)').matches ||
    window.navigator.standalone === true;

  isIOS.value =
    /iPad|iPhone|iPod/.test(navigator.userAgent) &&
    !window.MSStream;

  window.addEventListener('beforeinstallprompt', onBeforeInstallPrompt);
});

onUnmounted(() => {
  window.removeEventListener('beforeinstallprompt', onBeforeInstallPrompt);
});
</script>

<template>
  <div v-if="showBanner" class="install-banner">
    <div class="install-content">
      <div class="install-text" v-if="!isIOS">
        <strong>Install Bird Guesser</strong>
        <span>Add to your home screen for quick access</span>
      </div>
      <div class="install-text" v-else>
        <strong>Install Bird Guesser</strong>
        <span>Tap the share button, then "Add to Home Screen"</span>
      </div>
      <div class="install-actions">
        <button v-if="!isIOS" class="btn btn-primary install-btn" @click="install">
          Install
        </button>
        <button class="dismiss-btn" @click="dismiss" aria-label="Dismiss">
          &times;
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.install-banner {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: var(--color-surface);
  border-top: 2px solid var(--color-primary);
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.1);
  padding: var(--spacing-md);
  z-index: 1000;
}

.install-content {
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--spacing-md);
}

.install-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.install-text strong {
  font-size: 1rem;
  color: var(--color-text);
}

.install-text span {
  font-size: 0.875rem;
  color: var(--color-text-light);
}

.install-actions {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  flex-shrink: 0;
}

.install-btn {
  padding: var(--spacing-xs) var(--spacing-md);
  font-size: 0.875rem;
}

.dismiss-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: var(--color-text-light);
  cursor: pointer;
  padding: 0 var(--spacing-xs);
  line-height: 1;
}

.dismiss-btn:hover {
  color: var(--color-text);
}
</style>
