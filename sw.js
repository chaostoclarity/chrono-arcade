// Offline support: app files are cached; the page and data refresh from the network when online.
const CACHE = "chrono-v2";
const CORE = ["./", "index.html", "data/events.json", "data/world.json", "manifest.webmanifest", "icons/icon-192.png",
  "https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"];
self.addEventListener("install", e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting())); });
self.addEventListener("activate", e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  const url = new URL(e.request.url), local = url.origin === location.origin;
  if (local) {
    e.respondWith(fetch(e.request).then(r => { const copy = r.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); return r; }).catch(() => caches.match(e.request).then(m => m || caches.match("index.html"))));
  } else {
    e.respondWith(caches.match(e.request).then(m => m || fetch(e.request).then(r => { const copy = r.clone(); caches.open(CACHE).then(c => c.put(e.request, copy)); return r; })));
  }
});
