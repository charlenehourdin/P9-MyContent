if ('serviceWorker' in navigator) {   
    // we are checking here to see if the browser supports the  service worker api
 window.addEventListener('load', function() {
     navigator.serviceWorker.register('../sw.js').then(function(registration) {
       // Registration was successful
       console.log('Service Worker registration was successful with scope: ', registration.scope);
     }, function(err) {
       // registration failed :(
       console.log('ServiceWorker registration failed: ', err);
     });
   });
 }

var CACHE_NAME = 'offline-calculator';
var urlsToCache = [
  '/'
];

self.addEventListener('install', function(event) {
  // install files needed offline
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', function(event) {
    // every request from our site, passes through the fetch handler
    // I have proof
    console.log('I am a request with url:', event.request.clone().url)
    event.respondWith(
      // check all the caches in the browser and find
      // out whether our request is in any of them
      caches.match(event.request)
        .then(function(response) {
          if (response) {
            // if we are here, that means there's a match
            //return the response stored in browser
            return response;
          }
          // no match in cache, use the network instead
          return fetch(event.request);
        }
      )
    );
  });