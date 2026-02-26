// Web Push (RFC 8291) implementation using crypto.subtle
// VAPID (RFC 8292) JWT signing with ECDSA P-256

function base64UrlDecode(str) {
  const padded = str + '='.repeat((4 - (str.length % 4)) % 4);
  const binary = atob(padded.replace(/-/g, '+').replace(/_/g, '/'));
  return new Uint8Array([...binary].map(c => c.charCodeAt(0)));
}

function base64UrlEncode(buffer) {
  const bytes = buffer instanceof Uint8Array ? buffer : new Uint8Array(buffer);
  let binary = '';
  for (const byte of bytes) {
    binary += String.fromCharCode(byte);
  }
  return btoa(binary).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

function concatBuffers(...buffers) {
  const total = buffers.reduce((sum, b) => sum + b.byteLength, 0);
  const result = new Uint8Array(total);
  let offset = 0;
  for (const buf of buffers) {
    result.set(new Uint8Array(buf), offset);
    offset += buf.byteLength;
  }
  return result;
}

// Create info for HKDF as per RFC 8291
function createInfo(type, clientPublicKey, serverPublicKey) {
  const encoder = new TextEncoder();
  const typeBuffer = encoder.encode(type);

  // "Content-Encoding: <type>\0" + "P-256\0" + client key length (2 bytes) + client key + server key length (2 bytes) + server key
  const header = encoder.encode('Content-Encoding: ');
  const nul = new Uint8Array([0]);
  const keyLabel = encoder.encode('P-256');

  const clientLen = new Uint8Array(2);
  new DataView(clientLen.buffer).setUint16(0, clientPublicKey.byteLength);

  const serverLen = new Uint8Array(2);
  new DataView(serverLen.buffer).setUint16(0, serverPublicKey.byteLength);

  return concatBuffers(
    header, typeBuffer, nul,
    keyLabel, nul,
    clientLen, clientPublicKey,
    serverLen, serverPublicKey
  );
}

async function hkdf(salt, ikm, info, length) {
  const key = await crypto.subtle.importKey('raw', ikm, { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const prk = await crypto.subtle.sign('HMAC', key, salt.byteLength ? salt : new Uint8Array(32));

  const prkKey = await crypto.subtle.importKey('raw', prk, { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const infoWithCounter = concatBuffers(info, new Uint8Array([1]));
  const okm = await crypto.subtle.sign('HMAC', prkKey, infoWithCounter);

  return new Uint8Array(okm).slice(0, length);
}

async function encryptPayload(subscription, payload) {
  const clientPublicKey = base64UrlDecode(subscription.keys.p256dh);
  const authSecret = base64UrlDecode(subscription.keys.auth);

  // Generate server ECDH key pair
  const serverKeys = await crypto.subtle.generateKey({ name: 'ECDH', namedCurve: 'P-256' }, true, ['deriveBits']);
  const serverPublicKeyRaw = await crypto.subtle.exportKey('raw', serverKeys.publicKey);

  // Import client public key
  const clientKey = await crypto.subtle.importKey('raw', clientPublicKey, { name: 'ECDH', namedCurve: 'P-256' }, false, []);

  // ECDH key agreement
  const sharedSecret = await crypto.subtle.deriveBits({ name: 'ECDH', public: clientKey }, serverKeys.privateKey, 256);

  // HKDF for auth info (RFC 8291 Section 3.3)
  const authInfo = new TextEncoder().encode('Content-Encoding: auth\0');
  const ikm = await hkdf(authSecret, new Uint8Array(sharedSecret), authInfo, 32);

  // Derive content encryption key and nonce
  const serverPubBytes = new Uint8Array(serverPublicKeyRaw);
  const keyInfo = createInfo('aesgcm', clientPublicKey, serverPubBytes);
  const nonceInfo = createInfo('nonce', clientPublicKey, serverPubBytes);

  // Generate 16 byte salt
  const salt = crypto.getRandomValues(new Uint8Array(16));

  const contentEncryptionKey = await hkdf(salt, ikm, keyInfo, 16);
  const nonce = await hkdf(salt, ikm, nonceInfo, 12);

  // Pad payload (2 byte padding length + padding)
  const payloadBytes = new TextEncoder().encode(payload);
  const paddingLength = 0;
  const padded = new Uint8Array(2 + paddingLength + payloadBytes.byteLength);
  new DataView(padded.buffer).setUint16(0, paddingLength);
  padded.set(payloadBytes, 2 + paddingLength);

  // AES-128-GCM encryption
  const aesKey = await crypto.subtle.importKey('raw', contentEncryptionKey, { name: 'AES-GCM' }, false, ['encrypt']);
  const encrypted = await crypto.subtle.encrypt({ name: 'AES-GCM', iv: nonce }, aesKey, padded);

  return {
    ciphertext: new Uint8Array(encrypted),
    salt,
    serverPublicKey: serverPubBytes,
  };
}

async function createVapidHeaders(endpoint, env) {
  const url = new URL(endpoint);
  const audience = `${url.protocol}//${url.host}`;

  const header = base64UrlEncode(new TextEncoder().encode(JSON.stringify({ typ: 'JWT', alg: 'ES256' })));

  const now = Math.floor(Date.now() / 1000);
  const claims = base64UrlEncode(new TextEncoder().encode(JSON.stringify({
    aud: audience,
    exp: now + 12 * 60 * 60, // 12 hours
    sub: env.VAPID_SUBJECT,
  })));

  const unsignedToken = `${header}.${claims}`;

  // Import VAPID private key
  const privateKeyBytes = base64UrlDecode(env.VAPID_PRIVATE_KEY);
  const privateKey = await crypto.subtle.importKey(
    'jwk',
    {
      kty: 'EC',
      crv: 'P-256',
      d: env.VAPID_PRIVATE_KEY,
      x: base64UrlEncode(base64UrlDecode(env.VAPID_PUBLIC_KEY).slice(1, 33)),
      y: base64UrlEncode(base64UrlDecode(env.VAPID_PUBLIC_KEY).slice(33, 65)),
    },
    { name: 'ECDSA', namedCurve: 'P-256' },
    false,
    ['sign']
  );

  const signature = await crypto.subtle.sign(
    { name: 'ECDSA', hash: 'SHA-256' },
    privateKey,
    new TextEncoder().encode(unsignedToken)
  );

  // Convert DER signature to raw (r || s) format if needed
  const sigBytes = new Uint8Array(signature);
  const jwt = `${unsignedToken}.${base64UrlEncode(sigBytes)}`;

  const vapidPublicKeyBytes = base64UrlDecode(env.VAPID_PUBLIC_KEY);

  return {
    Authorization: `vapid t=${jwt}, k=${base64UrlEncode(vapidPublicKeyBytes)}`,
  };
}

export async function sendPushNotification(subscription, payload, env) {
  const { ciphertext, salt, serverPublicKey } = await encryptPayload(subscription, payload);
  const vapidHeaders = await createVapidHeaders(subscription.endpoint, env);

  const response = await fetch(subscription.endpoint, {
    method: 'POST',
    headers: {
      ...vapidHeaders,
      'Content-Type': 'application/octet-stream',
      'Content-Encoding': 'aesgcm',
      'Encryption': `salt=${base64UrlEncode(salt)}`,
      'Crypto-Key': `dh=${base64UrlEncode(serverPublicKey)}`,
      TTL: '86400',
    },
    body: ciphertext,
  });

  if (response.status === 410 || response.status === 404) {
    return { ok: false, gone: true };
  }

  if (!response.ok) {
    const text = await response.text();
    console.error(`Push failed (${response.status}): ${text}`);
    return { ok: false, gone: false };
  }

  return { ok: true, gone: false };
}
