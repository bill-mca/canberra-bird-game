import { subscribe, unsubscribe, listSubscriptions, deleteSubscription } from './subscriptions.js';
import { sendPushNotification } from './push.js';

function getAllowedOrigin(request, env) {
  const origin = request.headers.get('Origin') || '';
  const allowed = [env.FRONTEND_ORIGIN];

  // Allow preview deployment origins (*.workers.dev subdomains)
  if (env.PREVIEW_ORIGINS) {
    allowed.push(...env.PREVIEW_ORIGINS.split(',').map(s => s.trim()));
  }

  if (allowed.includes(origin) || origin.endsWith('.workers.dev')) {
    return origin;
  }
  return env.FRONTEND_ORIGIN || '';
}

function corsHeaders(request, env) {
  return {
    'Access-Control-Allow-Origin': getAllowedOrigin(request, env),
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };
}

function jsonResponse(data, status, request, env) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json',
      ...corsHeaders(request, env),
    },
  });
}

async function handleRequest(request, env) {
  const url = new URL(request.url);

  // CORS preflight
  if (request.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: corsHeaders(request, env) });
  }

  // GET /api/vapid-public-key
  if (url.pathname === '/api/vapid-public-key' && request.method === 'GET') {
    return jsonResponse({ key: env.VAPID_PUBLIC_KEY }, 200, request, env);
  }

  // POST /api/subscribe
  if (url.pathname === '/api/subscribe' && request.method === 'POST') {
    try {
      const body = await request.json();
      await subscribe(env.PUSH_SUBSCRIPTIONS, body);
      return jsonResponse({ ok: true }, 201, request, env);
    } catch (err) {
      return jsonResponse({ error: err.message }, 400, request, env);
    }
  }

  // POST /api/unsubscribe
  if (url.pathname === '/api/unsubscribe' && request.method === 'POST') {
    try {
      const body = await request.json();
      await unsubscribe(env.PUSH_SUBSCRIPTIONS, body.endpoint);
      return jsonResponse({ ok: true }, 200, request, env);
    } catch (err) {
      return jsonResponse({ error: err.message }, 400, request, env);
    }
  }

  return jsonResponse({ error: 'Not found' }, 404, request, env);
}

async function handleCron(env) {
  const payload = JSON.stringify({
    title: 'Bird Guesser',
    body: "Today's bird challenge is ready!",
    icon: '/pwa-192x192.png',
  });

  const subscriptions = await listSubscriptions(env.PUSH_SUBSCRIPTIONS);
  const results = await Promise.allSettled(
    subscriptions.map(async ({ key, subscription }) => {
      const result = await sendPushNotification(subscription, payload, env);
      if (result.gone) {
        await deleteSubscription(env.PUSH_SUBSCRIPTIONS, key);
      }
      return result;
    })
  );

  const sent = results.filter(r => r.status === 'fulfilled' && r.value.ok).length;
  const removed = results.filter(r => r.status === 'fulfilled' && r.value.gone).length;
  const failed = results.filter(r => r.status === 'rejected').length;

  console.log(`Push cron: sent=${sent}, removed=${removed}, failed=${failed}`);
}

export default {
  async fetch(request, env) {
    return handleRequest(request, env);
  },

  async scheduled(event, env, ctx) {
    ctx.waitUntil(handleCron(env));
  },
};
