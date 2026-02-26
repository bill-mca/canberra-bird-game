/**
 * LocalStorage management for game data persistence
 */

const STORAGE_KEYS = {
  DAILY_STREAK: 'canberra_birds_daily_streak',
  DAILY_COMPLETED: 'canberra_birds_daily_completed',
  STATS: 'canberra_birds_stats',
  LAST_PLAYED: 'canberra_birds_last_played'
};

/**
 * Get today's date as YYYY-MM-DD string
 * TESTING: rotates every 10 minutes instead of daily — revert before merging to main
 */
export function getTodayString() {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  const hour = String(now.getHours()).padStart(2, '0');
  const chunk = String(Math.floor(now.getMinutes() / 10));
  return `${year}-${month}-${day}-${hour}-${chunk}`;
}

/**
 * Get previous period's string
 * TESTING: previous 10-minute window — revert before merging to main
 */
function getYesterdayString() {
  const prev = new Date(Date.now() - 10 * 60 * 1000);
  const year = prev.getFullYear();
  const month = String(prev.getMonth() + 1).padStart(2, '0');
  const day = String(prev.getDate()).padStart(2, '0');
  const hour = String(prev.getHours()).padStart(2, '0');
  const chunk = String(Math.floor(prev.getMinutes() / 10));
  return `${year}-${month}-${day}-${hour}-${chunk}`;
}

/**
 * Get daily challenge streak
 */
export function getDailyStreak() {
  const streak = localStorage.getItem(STORAGE_KEYS.DAILY_STREAK);
  return streak ? parseInt(streak, 10) : 0;
}

/**
 * Update daily challenge streak
 */
export function updateDailyStreak(isCorrect) {
  const today = getTodayString();
  const lastPlayed = localStorage.getItem(STORAGE_KEYS.LAST_PLAYED);
  const yesterday = getYesterdayString();

  let currentStreak = getDailyStreak();

  if (isCorrect) {
    if (lastPlayed === yesterday) {
      // Continuing streak
      currentStreak += 1;
    } else if (lastPlayed === today) {
      // Already played today, no change
    } else {
      // First time playing or streak broken
      currentStreak = 1;
    }
  } else {
    // Incorrect answer doesn't break streak, but doesn't extend it either
    // Only correct answers extend the streak
  }

  localStorage.setItem(STORAGE_KEYS.DAILY_STREAK, currentStreak.toString());
  localStorage.setItem(STORAGE_KEYS.LAST_PLAYED, today);

  return currentStreak;
}

/**
 * Check if daily challenge has been completed today
 */
export function isDailyCompleted() {
  const completed = localStorage.getItem(STORAGE_KEYS.DAILY_COMPLETED);
  const today = getTodayString();

  if (!completed) return false;

  try {
    const completedData = JSON.parse(completed);
    return completedData.date === today && completedData.answered === true;
  } catch (e) {
    return false;
  }
}

/**
 * Mark daily challenge as completed
 */
export function markDailyCompleted(birdId, isCorrect) {
  const today = getTodayString();
  const data = {
    date: today,
    answered: true,
    birdId,
    isCorrect,
    timestamp: new Date().toISOString()
  };

  localStorage.setItem(STORAGE_KEYS.DAILY_COMPLETED, JSON.stringify(data));
}

/**
 * Get daily challenge result for today (if completed)
 */
export function getDailyResult() {
  const completed = localStorage.getItem(STORAGE_KEYS.DAILY_COMPLETED);
  const today = getTodayString();

  if (!completed) return null;

  try {
    const data = JSON.parse(completed);
    if (data.date === today && data.answered === true) {
      return {
        birdId: data.birdId,
        isCorrect: data.isCorrect,
        timestamp: data.timestamp
      };
    }
  } catch (e) {
    return null;
  }

  return null;
}

/**
 * Get all-time statistics
 */
export function getStats() {
  const stats = localStorage.getItem(STORAGE_KEYS.STATS);

  if (!stats) {
    return {
      totalGames: 0,
      totalQuestions: 0,
      correctAnswers: 0,
      dailyChallengesCompleted: 0,
      bestStreak: 0
    };
  }

  try {
    return JSON.parse(stats);
  } catch (e) {
    return {
      totalGames: 0,
      totalQuestions: 0,
      correctAnswers: 0,
      dailyChallengesCompleted: 0,
      bestStreak: 0
    };
  }
}

/**
 * Update statistics
 */
export function updateStats(sessionData) {
  const stats = getStats();

  stats.totalGames += 1;
  stats.totalQuestions += sessionData.totalQuestions || 0;
  stats.correctAnswers += sessionData.correctAnswers || 0;

  if (sessionData.isDaily) {
    stats.dailyChallengesCompleted += 1;
  }

  const currentStreak = getDailyStreak();
  if (currentStreak > stats.bestStreak) {
    stats.bestStreak = currentStreak;
  }

  localStorage.setItem(STORAGE_KEYS.STATS, JSON.stringify(stats));

  return stats;
}

/**
 * Reset all data (for testing or user request)
 */
export function resetAllData() {
  Object.values(STORAGE_KEYS).forEach(key => {
    localStorage.removeItem(key);
  });
}

/**
 * Export data as JSON (for backup or sharing)
 */
export function exportData() {
  const data = {};
  Object.entries(STORAGE_KEYS).forEach(([name, key]) => {
    const value = localStorage.getItem(key);
    if (value) {
      try {
        data[name] = JSON.parse(value);
      } catch (e) {
        data[name] = value;
      }
    }
  });

  return JSON.stringify(data, null, 2);
}
