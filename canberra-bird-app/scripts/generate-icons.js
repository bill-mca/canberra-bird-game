import sharp from 'sharp';
import { readFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const publicDir = resolve(__dirname, '../public');
const svgBuffer = readFileSync(resolve(publicDir, 'favicon.svg'));

const icons = [
  { name: 'pwa-192x192.png', size: 192 },
  { name: 'pwa-512x512.png', size: 512 },
  { name: 'apple-touch-icon-180x180.png', size: 180 },
];

for (const icon of icons) {
  await sharp(svgBuffer)
    .resize(icon.size, icon.size)
    .png()
    .toFile(resolve(publicDir, icon.name));
  console.log(`Generated ${icon.name}`);
}

// Maskable icon: green background with padding for safe zone
// The SVG already has a green circle background, so we just need to ensure
// the icon fits within the safe zone (80% of the total area)
const paddedSize = 512;
const iconSize = Math.round(paddedSize * 0.8);
const offset = Math.round((paddedSize - iconSize) / 2);

const iconBuffer = await sharp(svgBuffer)
  .resize(iconSize, iconSize)
  .png()
  .toBuffer();

await sharp({
  create: {
    width: paddedSize,
    height: paddedSize,
    channels: 4,
    background: { r: 44, g: 95, b: 45, alpha: 1 }, // #2c5f2d
  },
})
  .composite([{ input: iconBuffer, left: offset, top: offset }])
  .png()
  .toFile(resolve(publicDir, 'maskable-icon-512x512.png'));

console.log('Generated maskable-icon-512x512.png');
console.log('Done!');
