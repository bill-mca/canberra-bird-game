import { subscribe, unsubscribe, listSubscriptions, deleteSubscription } from './subscriptions.js';
import { sendPushNotification } from './push.js';

function corsHeaders(env) {
  return {
    'Access-Control-Allow-Origin': env.FRONTEND_ORIGIN || '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
  };
}

function jsonResponse(data, status, env) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json',
      ...corsHeaders(env),
    },
  });
}

async function handleRequest(request, env) {
  const url = new URL(request.url);

  // CORS preflight
  if (request.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers: corsHeaders(env) });
  }

  // GET /api/vapid-public-key
  if (url.pathname === '/api/vapid-public-key' && request.method === 'GET') {
    return jsonResponse({ key: env.VAPID_PUBLIC_KEY }, 200, env);
  }

  // POST /api/subscribe
  if (url.pathname === '/api/subscribe' && request.method === 'POST') {
    try {
      const body = await request.json();
      await subscribe(env.PUSH_SUBSCRIPTIONS, body);
      return jsonResponse({ ok: true }, 201, env);
    } catch (err) {
      return jsonResponse({ error: err.message }, 400, env);
    }
  }

  // POST /api/unsubscribe
  if (url.pathname === '/api/unsubscribe' && request.method === 'POST') {
    try {
      const body = await request.json();
      await unsubscribe(env.PUSH_SUBSCRIPTIONS, body.endpoint);
      return jsonResponse({ ok: true }, 200, env);
    } catch (err) {
      return jsonResponse({ error: err.message }, 400, env);
    }
  }

  return jsonResponse({ error: 'Not found' }, 404, env);
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
