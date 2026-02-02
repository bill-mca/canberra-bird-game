/**
 * Deterministic daily bird selection
 * Ensures all players get the same bird on the same day
 */

import { getTodayString } from './storage.js';

/**
 * Simple hash function to convert a string to a number
 */
function hashString(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash; // Convert to 32-bit integer
  }
  return Math.abs(hash);
}

/**
 * Seeded random number generator
 * Based on the Mulberry32 algorithm
 */
function seededRandom(seed) {
  let state = seed;
  return function() {
    state = (state + 0x6D2B79F5) | 0;
    let t = Math.imul(state ^ (state >>> 15), 1 | state);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/**
 * Get daily bird index using deterministic seed
 * @param {number} totalBirds - Total number of birds available
 * @param {string} dateString - Date in YYYY-MM-DD format (defaults to today)
 * @returns {number} Index of the bird for this day
 */
export function getDailyBirdIndex(totalBirds, dateString = null) {
  const today = dateString || getTodayString();

  // Create a seed from the date
  const seed = hashString(`canberra-birds-${today}`);

  // Generate a seeded random number
  const random = seededRandom(seed);
  const randomValue = random();

  // Select bird index
  return Math.floor(randomValue * totalBirds);
}

/**
 * Get the daily bird from a list of birds
 * @param {Array} birds - Array of bird objects
 * @param {string} dateString - Date in YYYY-MM-DD format (defaults to today)
 * @returns {Object} The bird for today
 */
export function getDailyBird(birds, dateString = null) {
  if (!birds || birds.length === 0) return null;

  const index = getDailyBirdIndex(birds.length, dateString);
  return birds[index];
}

/**
 * Get bird for a specific date (for testing)
 */
export function getBirdForDate(birds, dateString) {
  return getDailyBird(birds, dateString);
}

/**
 * Verify that the same date produces the same bird (for testing)
 */
export function verifyDeterminism(birds, dateString) {
  const bird1 = getDailyBird(birds, dateString);
  const bird2 = getDailyBird(birds, dateString);
  const bird3 = getDailyBird(birds, dateString);

  return bird1.scientificName === bird2.scientificName &&
         bird2.scientificName === bird3.scientificName;
}
