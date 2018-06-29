self.addEventListener('push', function (event) {
  console.log('[Service Worker] Push Received.');

  const data = JSON.parse(event.data.text())
  const title = data.headline;
  const options = {
    body: data.snippet,
    data: data.url,
    icon: '/static/images/ubyssey-logo-square.png',
    image: data.image
  };

  event.waitUntil(self.registration.showNotification(title, options));
});

self.addEventListener('notificationclick', function (event) {
  console.log('[Service Worker] Notification click Received.');

  event.notification.close();

  event.waitUntil(
    clients.openWindow(event.notification.data)
  );
});