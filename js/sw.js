self.addEventListener('install', function (event) {
  event.waitUntil(self.skipWaiting());
});

self.addEventListener('activate', function (event) {
  event.waitUntil(self.clients.claim());
});




// Register event listener for the 'push' event.
self.addEventListener('push', function (event) {
    // Retrieve the textual payload from event.data (a PushMessageData object).
    // Other formats are supported (ArrayBuffer, Blob, JSON), check out the documentation
    // on https://developer.mozilla.org/en-US/docs/Web/API/PushMessageData.

    const eventInfo = event.data.text();
    const data = JSON.parse(eventInfo);
    const head = data.head || 'New Notification 🕺🕺';
    const body = data.body || 'This is default content. Your notification didn\'t have one 🙄🙄';
    const icon = data.icon || 'https://i.imgur.com/dRDxiCQ.png';
    const url = data.url || ''
    const vibrate = data.vibrate || [200, 100, 200, 100, 200, 100, 200];
    
    // Keep the service worker alive until the notification is created.
    event.waitUntil(
        // Show a notification with title 'ServiceWorker Cookbook' and use the payload
        // as the body.
        self.registration.showNotification(head, {
            body: body,
            icon: icon,
            vibrate: vibrate,
            data: {url: url},
        })
    );
});

self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    
    const target = event.notification.data.url

    event.waitUntil(self.clients.matchAll().then(function(clientList) {
        console.log(clientList)
        if (clientList.length > 0) {
            clientList[0].focus();
            return clientList[0].navigate(target);
        }
        console.log(self.clients)
        return self.clients.openWindow(target);
    }));
});
