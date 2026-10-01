/*
 * Paseka eLearning — first-party analytics
 * Self-hosted, anonymous. Logs one pageview per load, then reports
 * time-on-page once when the visitor leaves. Only runs once cookies have
 * been accepted in the cookie banner (components/cookie_banner.html), which
 * dispatches 'cookie-consent-changed' when the choice is made.
 */
(function () {
  'use strict';

  var viewId = null;
  var startTime = Date.now();
  var durationSent = false;

  function hasConsent() {
    return document.cookie.split('; ').some(function (c) {
      return c.indexOf('cookie_consent=accepted') === 0;
    });
  }

  function visitorId() {
    try {
      var id = localStorage.getItem('pv_visitor_id');
      if (!id) {
        id = 'v-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 10);
        localStorage.setItem('pv_visitor_id', id);
      }
      return id;
    } catch (e) {
      return '';
    }
  }

  function sendPageview() {
    if (viewId !== null) return; // already logged this page load
    var body = new URLSearchParams({
      path: location.pathname,
      referrer: document.referrer || '',
      visitor_id: visitorId(),
    });
    fetch('/api/track/pageview', { method: 'POST', body: body, keepalive: true })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (data) { if (data && data.id) viewId = data.id; })
      .catch(function () {});
  }

  function sendDuration() {
    if (viewId === null || durationSent) return;
    durationSent = true;
    var duration = Math.round((Date.now() - startTime) / 1000);
    var payload = JSON.stringify({ id: viewId, duration: duration });
    try {
      navigator.sendBeacon('/api/track/duration', new Blob([payload], { type: 'application/json' }));
    } catch (e) {}
  }

  document.addEventListener('pagehide', sendDuration);
  document.addEventListener('visibilitychange', function () {
    if (document.visibilityState === 'hidden') sendDuration();
  });

  window.addEventListener('cookie-consent-changed', function (e) {
    if (e.detail === 'accepted') sendPageview();
  });

  if (hasConsent()) sendPageview();
})();
