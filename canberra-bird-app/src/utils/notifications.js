const PUSH_WORKER_URL = import.meta.env.VITE_PUSH_WORKER_URL || '';
const SUBSCRIBED_KEY = 'canberra_birds_push_subscribed';

export function isNotificationSupported() {
  return (
    'Notification' in window &&
    'serviceWorker' in navigator &&
    'PushManager' in window
  );
}

export function getSubscriptionState() {
  return localStorage.getItem(SUBSCRIBED_KEY) === 'true';
}

function setSubscriptionState(subscribed) {
  if (subscribed) {
    localStorage.setItem(SUBSCRIBED_KEY, 'true');
  } else {
    localStorage.removeItem(SUBSCRIBED_KEY);
  }
}

async function getVapidPublicKey() {
  const response = await fetch(`${PUSH_WORKER_URL}/api/vapid-public-key`);
  const data = await response.json();
  return data.key;
}

function urlBase64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - (base64String.length % 4)) % 4);
  const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/');
  const rawData = atob(base64);
  return Uint8Array.from([...rawData].map(char => char.charCodeAt(0)));
}

export async function subscribeToPush() {
  const permission = await Notification.requestPermission();
  if (permission !== 'granted') {
    throw new Error('permission_denied');
  }

  const registration = await navigator.serviceWorker.ready;
  const vapidPublicKey = await getVapidPublicKey();

  const subscription = await registration.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: urlBase64ToUint8Array(vapidPublicKey),
  });

  const response = await fetch(`${PUSH_WORKER_URL}/api/subscribe`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(subscription.toJSON()),
  });

  if (!response.ok) {
    throw new Error('subscribe_failed');
  }

  setSubscriptionState(true);
}

export async function unsubscribeFromPush() {
  const registration = await navigator.serviceWorker.ready;
  const subscription = await registration.pushManager.getSubscription();

  if (subscription) {
    const endpoint = subscription.endpoint;
    await subscription.unsubscribe();

    await fetch(`${PUSH_WORKER_URL}/api/unsubscribe`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ endpoint }),
    });
  }

  setSubscriptionState(false);
}

export async function isPushSubscribed() {
  if (!isNotificationSupported()) return false;

  try {
    const registration = await navigator.serviceWorker.ready;
    const subscription = await registration.pushManager.getSubscription();
    const subscribed = subscription !== null;
    // Sync localStorage with actual state
    setSubscriptionState(subscribed);
    return subscribed;
  } catch {
    return false;
  }
}
