const CACHE_NAME = 'my-pwa-cache-v1';
const urlsToCache = [
  '/',
  '/offline/',
  '/static/css/main.css',
  '/static/js/main.js',
  '/static/images/icon-160x160.png',
  '/static/images/icon-160x160.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
      .catch(() => caches.match('/offline/'))
  );
});
