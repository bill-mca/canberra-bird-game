<script setup>
import { ref, onMounted } from 'vue';
import {
  isNotificationSupported,
  isPushSubscribed,
  subscribeToPush,
  unsubscribeFromPush,
} from '../utils/notifications.js';

const supported = ref(false);
const subscribed = ref(false);
const loading = ref(false);
const error = ref(null);

onMounted(async () => {
  supported.value = isNotificationSupported();
  if (supported.value) {
    subscribed.value = await isPushSubscribed();
  }
});

async function toggle() {
  loading.value = true;
  error.value = null;

  try {
    if (subscribed.value) {
      await unsubscribeFromPush();
      subscribed.value = false;
    } else {
      await subscribeToPush();
      subscribed.value = true;
    }
  } catch (err) {
    if (err.message === 'permission_denied') {
      error.value = 'Notification permission was denied. You can enable it in your browser settings.';
    } else {
      error.value = 'Something went wrong. Please try again.';
    }
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div v-if="supported" class="notification-settings card">
    <div class="notification-header">
      <div class="notification-info">
        <h3>Daily Reminders</h3>
        <p>Get a daily reminder when the new bird challenge is ready</p>
      </div>
      <button
        class="toggle-btn"
        :class="{ active: subscribed }"
        :disabled="loading"
        @click="toggle"
        :aria-label="subscribed ? 'Disable daily reminders' : 'Enable daily reminders'"
      >
        <span class="toggle-track">
          <span class="toggle-thumb"></span>
        </span>
      </button>
    </div>
    <p v-if="error" class="notification-error">{{ error }}</p>
  </div>
</template>

<style scoped>
.notification-settings {
  margin-top: var(--spacing-lg);
}

.notification-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--spacing-md);
}

.notification-info h3 {
  color: var(--color-primary);
  font-size: 1.1rem;
  margin-bottom: 2px;
}

.notification-info p {
  color: var(--color-text-light);
  font-size: 0.875rem;
}

.toggle-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  flex-shrink: 0;
}

.toggle-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.toggle-track {
  display: block;
  width: 48px;
  height: 28px;
  background-color: var(--color-border);
  border-radius: 14px;
  position: relative;
  transition: background-color var(--transition);
}

.toggle-btn.active .toggle-track {
  background-color: var(--color-primary);
}

.toggle-thumb {
  display: block;
  width: 22px;
  height: 22px;
  background-color: white;
  border-radius: 50%;
  position: absolute;
  top: 3px;
  left: 3px;
  transition: transform var(--transition);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
}

.toggle-btn.active .toggle-thumb {
  transform: translateX(20px);
}

.notification-error {
  color: var(--color-error);
  font-size: 0.875rem;
  margin-top: var(--spacing-sm);
}
</style>
