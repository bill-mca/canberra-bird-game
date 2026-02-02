/**
 * Scoring system for the bird game
 */

/**
 * Base points by rarity
 */
const RARITY_POINTS = {
  very_common: 10,
  common: 25,
  uncommon: 40,
  rare: 50,
  vagrant: 100,
  extinct: 150
};

/**
 * Multipliers
 */
const MULTIPLIERS = {
  audioOnly: 2.0,
  noHints: 1.5,
  fastAnswer: 1.25  // < 5 seconds
};

/**
 * Calculate score for a correct answer
 *
 * @param {Object} bird - The bird object
 * @param {Object} options - Scoring options
 * @param {boolean} options.audioOnly - Was this audio-only identification?
 * @param {boolean} options.usedHints - Did the player use hints?
 * @param {number} options.timeSeconds - Time taken in seconds
 * @returns {number} Final score
 */
export function calculateScore(bird, options = {}) {
  const {
    audioOnly = false,
    usedHints = false,
    timeSeconds = null
  } = options;

  // Base points from rarity
  let score = RARITY_POINTS[bird.rarity] || 10;

  // Apply multipliers
  if (audioOnly) {
    score *= MULTIPLIERS.audioOnly;
  }

  if (!usedHints) {
    score *= MULTIPLIERS.noHints;
  }

  if (timeSeconds !== null && timeSeconds < 5) {
    score *= MULTIPLIERS.fastAnswer;
  }

  return Math.round(score);
}

/**
 * Get base points for a bird (no multipliers)
 */
export function getBasePoints(bird) {
  return RARITY_POINTS[bird.rarity] || 10;
}

/**
 * Calculate statistics for a game session
 */
export function calculateSessionStats(results) {
  const totalQuestions = results.length;
  const correctAnswers = results.filter(r => r.isCorrect).length;
  const totalScore = results.reduce((sum, r) => sum + (r.score || 0), 0);
  const averageTime = results.length > 0
    ? results.reduce((sum, r) => sum + (r.timeSeconds || 0), 0) / results.length
    : 0;

  const accuracy = totalQuestions > 0
    ? Math.round((correctAnswers / totalQuestions) * 100)
    : 0;

  return {
    totalQuestions,
    correctAnswers,
    incorrectAnswers: totalQuestions - correctAnswers,
    totalScore,
    accuracy,
    averageTime: Math.round(averageTime * 10) / 10
  };
}

/**
 * Format score for display
 */
export function formatScore(score) {
  return score.toLocaleString();
}

/**
 * Get score breakdown text
 */
export function getScoreBreakdown(bird, options = {}) {
  const basePoints = getBasePoints(bird);
  const breakdown = [`Base: ${basePoints} pts (${bird.rarity})`];

  if (options.audioOnly) {
    breakdown.push(`× ${MULTIPLIERS.audioOnly} (Audio only)`);
  }

  if (!options.usedHints) {
    breakdown.push(`× ${MULTIPLIERS.noHints} (No hints)`);
  }

  if (options.timeSeconds !== null && options.timeSeconds < 5) {
    breakdown.push(`× ${MULTIPLIERS.fastAnswer} (Fast answer)`);
  }

  const finalScore = calculateScore(bird, options);
  breakdown.push(`= ${finalScore} pts`);

  return breakdown.join('\n');
}
