/**
 * Bird data loading and filtering utilities
 */

let birdData = null;

/**
 * Load bird data from JSON file
 */
export async function loadBirdData() {
  if (birdData) return birdData;

  const response = await fetch('/act_birds.json');
  const data = await response.json();
  birdData = data.birds;
  return birdData;
}

/**
 * Get all birds
 */
export function getAllBirds() {
  return birdData || [];
}

/**
 * Difficulty level configurations
 */
export const DIFFICULTY_LEVELS = {
  beginner: {
    name: 'Beginner',
    emoji: '🟢',
    rarities: ['very_common', 'common'],
    optionCount: 4,
    description: 'Very Common + Common birds (164 species)'
  },
  intermediate: {
    name: 'Intermediate',
    emoji: '🟡',
    rarities: ['very_common', 'common', 'uncommon', 'rare'],
    optionCount: 6,
    description: 'Add Uncommon + Some Rare birds (228 species)'
  },
  advanced: {
    name: 'Advanced',
    emoji: '🔴',
    rarities: ['very_common', 'common', 'uncommon', 'rare', 'vagrant', 'extinct'],
    optionCount: 8,
    description: 'All birds including Rare + Vagrant (297 species)'
  }
};

/**
 * Filter birds by difficulty level
 */
export function filterByDifficulty(birds, difficulty) {
  const config = DIFFICULTY_LEVELS[difficulty];
  if (!config) return birds;

  return birds.filter(bird =>
    config.rarities.includes(bird.rarity)
  );
}

/**
 * Filter birds by family
 */
export function filterByFamily(birds, families) {
  if (!families || families.length === 0) return birds;
  return birds.filter(bird => families.includes(bird.family));
}

/**
 * Filter birds by rarity
 */
export function filterByRarity(birds, rarities) {
  if (!rarities || rarities.length === 0) return birds;
  return birds.filter(bird => rarities.includes(bird.rarity));
}

/**
 * Filter birds by conservation status
 */
export function filterByConservation(birds, hasConservationStatus) {
  if (hasConservationStatus === null || hasConservationStatus === undefined) return birds;
  return birds.filter(bird => {
    const hasStatus = bird.conservationStatus && Object.keys(bird.conservationStatus).length > 0;
    return hasConservationStatus ? hasStatus : !hasStatus;
  });
}

/**
 * Filter birds by origin (native vs introduced)
 */
export function filterByOrigin(birds, isNative) {
  if (isNative === null || isNative === undefined) return birds;
  return birds.filter(bird =>
    isNative ? !bird.isIntroduced : bird.isIntroduced
  );
}

/**
 * Filter birds that have audio recordings
 */
export function filterByAudio(birds, hasAudio) {
  if (hasAudio === null || hasAudio === undefined) return birds;
  return birds.filter(bird => {
    const birdHasAudio = bird.audio && bird.audio.length > 0;
    return hasAudio ? birdHasAudio : !birdHasAudio;
  });
}

/**
 * Get a random bird from a list
 */
export function getRandomBird(birds) {
  if (!birds || birds.length === 0) return null;
  const index = Math.floor(Math.random() * birds.length);
  return birds[index];
}

/**
 * Get N random wrong options that are different from the correct answer
 */
export function getWrongOptions(allBirds, correctBird, count) {
  const availableBirds = allBirds.filter(bird =>
    bird.scientificName !== correctBird.scientificName
  );

  // Shuffle and take the first N
  const shuffled = [...availableBirds].sort(() => Math.random() - 0.5);
  return shuffled.slice(0, count);
}

/**
 * Create multiple choice options (correct + wrong answers)
 */
export function createMultipleChoiceOptions(allBirds, correctBird, totalOptions) {
  const wrongCount = totalOptions - 1;
  const wrongOptions = getWrongOptions(allBirds, correctBird, wrongCount);

  // Combine and shuffle
  const allOptions = [correctBird, ...wrongOptions];
  return allOptions.sort(() => Math.random() - 0.5);
}

/**
 * Get all unique families from birds
 */
export function getAllFamilies(birds) {
  const families = new Set(birds.map(bird => bird.family));
  return Array.from(families).sort();
}

/**
 * Get count of birds by rarity
 */
export function getRarityCounts(birds) {
  const counts = {};
  birds.forEach(bird => {
    counts[bird.rarity] = (counts[bird.rarity] || 0) + 1;
  });
  return counts;
}

/**
 * Get a random photo from a bird's photos array
 */
export function getRandomPhoto(bird) {
  if (!bird.photos || bird.photos.length === 0) return null;
  const index = Math.floor(Math.random() * bird.photos.length);
  return bird.photos[index];
}

/**
 * Get a random audio from a bird's audio array
 */
export function getRandomAudio(bird) {
  if (!bird.audio || bird.audio.length === 0) return null;
  const index = Math.floor(Math.random() * bird.audio.length);
  return bird.audio[index];
}
