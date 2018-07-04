self.addEventListener('push', function (event) {
  console.log('[Service Worker] Push Received.');

  const data = JSON.parse(event.data.text())
  const title = data.headline;
  const options = {
    body: data.snippet,
    data: data.url,
    icon: '/static/images/ubyssey-logo-square.png',
    badge: '/static/images/ubyssey-logo.png',
    image: data.image,
    vibrate: [200, 100, 200]
  };

  event.waitUntil(self.registration.showNotification(title, options).then(
    // function(event) {
    //   console.log(event);
    //   setTimeout(function() {
    //     event.notification.close()
    //   }, 2000);
    // } 
  ));
});

self.addEventListener('notificationclick', function (event) {
  console.log('[Service Worker] Notification click Received.');

  event.notification.close();

  event.waitUntil(
    clients.openWindow(event.notification.data)
  );
});