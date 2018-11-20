var VERSION = '1.4.80'
var CACHE_NAME = 'ubyssey-cache-v' + VERSION;
var urlsToCache = [
  '/static/js/vendors-' + VERSION + '.js',
  '/static/js/main-' + VERSION + '.js',
  '/static/js/article-' + VERSION + '.js',
  '/static/images/ubyssey-logo.svg'
];

self.addEventListener('install', function(event) {
  // Perform install steps
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        // Cache hit - return response
        if (response) {
          return response;
        }
        return fetch(event.request);
      }
    )
  );
});

// Clear old cache
self.addEventListener('activate', function(event) {

  var cacheWhitelist = [CACHE_NAME];

  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.map(function(cacheName) {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});


self.addEventListener('push', function (event) {
  const data = JSON.parse(event.data.text())
  const title = data.headline;

  const options = {
    body: data.snippet,
    data: data.url,
    icon: data.tag === 'breaking' ? '/static/images/ubyssey-breaking-square.png' : '/static/images/ubyssey-logo-square.png',
    badge: 'static/images/ubyssey_icon.png',
    tag: data.tag,
    image: data.image
  };
  event.waitUntil(self.registration.showNotification(title, options));
});

self.addEventListener('notificationclick', function (event) {
  event.notification.close();

  event.waitUntil(
    clients.openWindow(event.notification.data)
  );
});
