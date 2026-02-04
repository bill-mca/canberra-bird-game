/**
 * Simplified scoring system for the bird game
 * Just tracks correct/incorrect answers
 */

/**
 * Calculate statistics for a game session
 */
export function calculateSessionStats(results) {
  const totalQuestions = results.length;
  const correctAnswers = results.filter(r => r.isCorrect).length;
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
    accuracy,
    averageTime: Math.round(averageTime * 10) / 10
  };
}
