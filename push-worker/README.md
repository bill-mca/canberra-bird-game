# Bird Guesser Push Worker

Cloudflare Worker that manages Web Push subscriptions and sends daily reminders for the Bird Guesser app.

## Setup

### 1. Install Wrangler

```bash
npm install -g wrangler
wrangler login
```

### 2. Create KV namespace

```bash
wrangler kv:namespace create PUSH_SUBSCRIPTIONS
```

Copy the returned `id` into `wrangler.toml`.

### 3. Generate VAPID keys

```bash
npx web-push generate-vapid-keys --json
```

### 4. Set secrets

```bash
wrangler secret put VAPID_PUBLIC_KEY
wrangler secret put VAPID_PRIVATE_KEY
wrangler secret put VAPID_SUBJECT
```

For `VAPID_SUBJECT`, use a `mailto:` URL (e.g., `mailto:admin@bird-guesser.pages.dev`).

The `VAPID_PUBLIC_KEY` must also be set as `VITE_PUSH_WORKER_URL` in the frontend `.env.production`.

### 5. Update FRONTEND_ORIGIN

Edit `wrangler.toml` to set `FRONTEND_ORIGIN` to your deployed frontend URL.

### 6. Deploy

```bash
wrangler deploy
```

## Endpoints

- `GET /api/vapid-public-key` — Returns the public VAPID key for client subscription
- `POST /api/subscribe` — Store a push subscription (body: `{ endpoint, keys: { p256dh, auth } }`)
- `POST /api/unsubscribe` — Remove a subscription (body: `{ endpoint }`)

## Cron

Runs daily at `0 22 * * *` UTC (8 AM AEST / 9 AM AEDT) to send push notifications to all subscribers.

## Local Development

```bash
wrangler dev
```

Test the cron handler:
```bash
curl "http://localhost:8787/__scheduled?cron=0+22+*+*+*"
```
