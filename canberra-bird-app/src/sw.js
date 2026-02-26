import { precacheAndRoute } from 'workbox-precaching';
import { registerRoute } from 'workbox-routing';
import { StaleWhileRevalidate, CacheFirst } from 'workbox-strategies';
import { ExpirationPlugin } from 'workbox-expiration';

// Precache app shell (injected by vite-plugin-pwa)
precacheAndRoute(self.__WB_MANIFEST);

// Runtime cache: bird data — serve cached, update in background
registerRoute(
  ({ url }) => url.pathname.endsWith('/act_birds.json'),
  new StaleWhileRevalidate({
    cacheName: 'bird-data',
  })
);

// Runtime cache: Wikimedia images
registerRoute(
  ({ url }) => url.hostname === 'upload.wikimedia.org',
  new CacheFirst({
    cacheName: 'wikimedia-images',
    plugins: [
      new ExpirationPlugin({
        maxEntries: 200,
        maxAgeSeconds: 90 * 24 * 60 * 60, // 90 days
      }),
    ],
  })
);

// Runtime cache: Xeno-canto audio
registerRoute(
  ({ url }) => url.hostname.includes('xeno-canto.org'),
  new CacheFirst({
    cacheName: 'xeno-canto-audio',
    plugins: [
      new ExpirationPlugin({
        maxEntries: 50,
        maxAgeSeconds: 90 * 24 * 60 * 60, // 90 days
      }),
    ],
  })
);
