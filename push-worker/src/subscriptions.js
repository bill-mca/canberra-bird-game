async function hashEndpoint(endpoint) {
  const encoded = new TextEncoder().encode(endpoint);
  const hashBuffer = await crypto.subtle.digest('SHA-256', encoded);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

export async function subscribe(kv, subscription) {
  if (!subscription?.endpoint || !subscription?.keys?.p256dh || !subscription?.keys?.auth) {
    throw new Error('Invalid subscription: endpoint, keys.p256dh, and keys.auth are required');
  }

  const key = await hashEndpoint(subscription.endpoint);
  const value = JSON.stringify({
    subscription,
    subscribedAt: new Date().toISOString(),
  });

  await kv.put(key, value);
}

export async function unsubscribe(kv, endpoint) {
  if (!endpoint) {
    throw new Error('endpoint is required');
  }

  const key = await hashEndpoint(endpoint);
  await kv.delete(key);
}

export async function deleteSubscription(kv, key) {
  await kv.delete(key);
}

export async function listSubscriptions(kv) {
  const subscriptions = [];
  let cursor = undefined;

  do {
    const result = await kv.list({ cursor });
    for (const key of result.keys) {
      const value = await kv.get(key.name, 'json');
      if (value?.subscription) {
        subscriptions.push({ key: key.name, subscription: value.subscription });
      }
    }
    cursor = result.list_complete ? undefined : result.cursor;
  } while (cursor);

  return subscriptions;
}
