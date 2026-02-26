# Progress

## Current Session - PWA Conversion (feature/pwa branch)

### Completed

**Phase 1: Basic PWA Setup (Task 16)**
- Installed `vite-plugin-pwa` with `injectManifest` strategy
- Generated PWA icons (192x192, 512x512, apple-touch-icon, maskable) from favicon.svg using sharp
- Created service worker with Workbox: precache app shell, StaleWhileRevalidate for bird data, CacheFirst for Wikimedia/Xeno-canto
- Configured web app manifest (standalone, themed #2c5f2d)
- Added iOS meta tags to index.html
- Created InstallPrompt component with beforeinstallprompt + iOS fallback
- Build verified: dist/ contains manifest.webmanifest, sw.js, all icon PNGs

**Phase 2: Push Notification Backend (Task 17)**
- Created `push-worker/` Cloudflare Worker project
- HTTP endpoints: GET /api/vapid-public-key, POST /api/subscribe, POST /api/unsubscribe
- KV subscription storage keyed by SHA-256 of endpoint URL
- Web Push encryption (RFC 8291) using crypto.subtle: ECDH + HKDF + AES-128-GCM
- VAPID JWT signing (RFC 8292) with ECDSA P-256
- Cron trigger at 22:00 UTC (8 AM AEST) for daily reminders
- Automatic cleanup of expired subscriptions (410 Gone)

**Phase 3: Push Notification Frontend (Task 18)**
- Added push/notificationclick event handlers to service worker
- Created notifications.js utility module (subscribe, unsubscribe, permission check)
- Created NotificationSettings component with toggle switch UI
- Added to MainMenu for natural discovery
- Environment config: .env.development (localhost:8787), .env.production (workers.dev)

### Remaining (requires human testing)
- Test installability on Android Chrome, iOS Safari, desktop
- Verify offline functionality
- Deploy push worker and test end-to-end push notifications
- Set VAPID keys as worker secrets
- Create KV namespace and update wrangler.toml with ID
- Update .env.production with actual worker URL
