/*
 * Paseka eLearning — Spatial 3D/4D Experience
 * Pure Canvas + CSS custom properties. Zero extra dependencies.
 * Modules: Neural Canvas · Card Tilt · 4D Timeline · Fold Reveals · Nav
 */

(function () {
  'use strict';

  const REDUCE = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ─── 1. Neural Network Background Canvas ─────────────────────────────────
  function initNeuralCanvas() {
    const canvas = document.getElementById('neural-canvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const PARTICLE_COUNT = 65;
    const MAX_LINK_DIST = 150;
    const PALETTE = [
      [36, 59, 48],    // ink
      [183, 90, 67],   // accent
      [210, 154, 49],  // warm
    ];

    let W, H, particles = [];
    const mouse = { x: -9999, y: -9999 };

    function resize() {
      W = canvas.width = canvas.offsetWidth;
      H = canvas.height = canvas.offsetHeight;
    }

    function spawn() {
      particles = Array.from({ length: PARTICLE_COUNT }, () => {
        const c = PALETTE[Math.floor(Math.random() * PALETTE.length)];
        return {
          x: Math.random() * W,
          y: Math.random() * H,
          vx: (Math.random() - 0.5) * 0.45,
          vy: (Math.random() - 0.5) * 0.45,
          r: Math.random() * 2.2 + 1.2,
          rgb: c,
          base_alpha: Math.random() * 0.35 + 0.2,
        };
      });
    }

    let rafId;
    let lastTs = 0;
    const FRAME_MS = 1000 / 30; // 30 fps cap for perf

    function frame(ts) {
      rafId = requestAnimationFrame(frame);
      if (ts - lastTs < FRAME_MS) return;
      lastTs = ts;

      ctx.clearRect(0, 0, W, H);

      // Update + draw particles
      for (let i = 0; i < particles.length; i++) {
        const p = particles[i];

        // Soft mouse repulsion
        const mdx = p.x - mouse.x;
        const mdy = p.y - mouse.y;
        const mdist = Math.hypot(mdx, mdy);
        if (mdist < 100) {
          p.vx += (mdx / mdist) * 0.022;
          p.vy += (mdy / mdist) * 0.022;
        }

        // Velocity damping
        p.vx *= 0.986;
        p.vy *= 0.986;
        p.x += p.vx;
        p.y += p.vy;

        // Edge wrap
        if (p.x < -12) p.x = W + 12;
        else if (p.x > W + 12) p.x = -12;
        if (p.y < -12) p.y = H + 12;
        else if (p.y > H + 12) p.y = -12;

        // Draw node
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${p.rgb[0]},${p.rgb[1]},${p.rgb[2]},${p.base_alpha})`;
        ctx.fill();
      }

      // Draw links
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const a = particles[i], b = particles[j];
          const dx = a.x - b.x, dy = a.y - b.y;
          const dist = Math.hypot(dx, dy);
          if (dist < MAX_LINK_DIST) {
            const alpha = (1 - dist / MAX_LINK_DIST) * 0.16;
            const r = (a.rgb[0] + b.rgb[0]) >> 1;
            const g = (a.rgb[1] + b.rgb[1]) >> 1;
            const bl = (a.rgb[2] + b.rgb[2]) >> 1;
            ctx.beginPath();
            ctx.moveTo(a.x, a.y);
            ctx.lineTo(b.x, b.y);
            ctx.strokeStyle = `rgba(${r},${g},${bl},${alpha})`;
            ctx.lineWidth = 1;
            ctx.stroke();
          }
        }
      }
    }

    // Pause when canvas is off-screen (saves CPU)
    const observer = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting) {
        rafId = requestAnimationFrame(frame);
      } else {
        cancelAnimationFrame(rafId);
      }
    });

    resize();
    spawn();
    observer.observe(canvas);

    window.addEventListener('resize', () => { resize(); spawn(); }, { passive: true });

    const hero = canvas.parentElement;
    hero.addEventListener('mousemove', e => {
      const r = canvas.getBoundingClientRect();
      mouse.x = e.clientX - r.left;
      mouse.y = e.clientY - r.top;
    }, { passive: true });
    hero.addEventListener('mouseleave', () => { mouse.x = -9999; mouse.y = -9999; });
  }

  // ─── 2. 3D Perspective Tilt on Cards ─────────────────────────────────────
  function initTiltCards() {
    if (REDUCE) return;

    document.querySelectorAll('[data-tilt]').forEach(card => {
      const MAX = parseFloat(card.dataset.tiltMax || '8');

      // Inject a shine layer (avoids ::after pseudo-element conflicts)
      const shine = document.createElement('div');
      shine.className = 'tilt-shine';
      card.style.position = 'relative';
      card.style.overflow = 'hidden';
      card.appendChild(shine);

      let raf;
      let targetRx = 0, targetRy = 0, currentRx = 0, currentRy = 0;

      function lerpFrame() {
        currentRx += (targetRx - currentRx) * 0.12;
        currentRy += (targetRy - currentRy) * 0.12;
        card.style.transform = `perspective(1100px) rotateX(${currentRx}deg) rotateY(${currentRy}deg)`;
        if (Math.abs(targetRx - currentRx) > 0.01 || Math.abs(targetRy - currentRy) > 0.01) {
          raf = requestAnimationFrame(lerpFrame);
        }
      }

      card.addEventListener('mousemove', e => {
        const rect = card.getBoundingClientRect();
        const cx = rect.left + rect.width / 2;
        const cy = rect.top + rect.height / 2;
        targetRx = ((e.clientY - cy) / (rect.height / 2)) * -MAX;
        targetRy = ((e.clientX - cx) / (rect.width / 2)) * MAX;

        const sx = ((e.clientX - rect.left) / rect.width) * 100;
        const sy = ((e.clientY - rect.top) / rect.height) * 100;
        shine.style.background = `radial-gradient(circle at ${sx}% ${sy}%, rgba(255,255,255,0.14) 0%, transparent 60%)`;
        shine.style.opacity = '1';

        cancelAnimationFrame(raf);
        raf = requestAnimationFrame(lerpFrame);
      }, { passive: true });

      card.addEventListener('mouseleave', () => {
        targetRx = 0;
        targetRy = 0;
        shine.style.opacity = '0';
        cancelAnimationFrame(raf);
        raf = requestAnimationFrame(lerpFrame);
      });
    });
  }

  // ─── 3. 4D Scroll Timeline (the "time axis") ─────────────────────────────
  function initTimeline() {
    const tl = document.getElementById('scroll-timeline');
    if (!tl) return;

    const fill = tl.querySelector('.tl-fill');
    const dots = tl.querySelectorAll('.tl-dot');

    // Map section IDs to dot indices
    const sections = Array.from(document.querySelectorAll('section[id]'));

    let ticking = false;
    function update() {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(() => {
        ticking = false;
        const scrolled = window.scrollY;
        const total = document.documentElement.scrollHeight - window.innerHeight;
        const pct = total > 0 ? Math.min(100, (scrolled / total) * 100) : 0;
        if (fill) fill.style.height = pct + '%';

        sections.forEach((sec, i) => {
          if (!dots[i]) return;
          const active = scrolled >= sec.offsetTop - 120;
          dots[i].classList.toggle('tl-dot-active', active);
        });
      });
    }

    window.addEventListener('scroll', update, { passive: true });
    update();
  }

  // ─── 4. 3D Fold-In Reveal ────────────────────────────────────────────────
  function initFoldReveal() {
    const els = document.querySelectorAll('.reveal-3d');
    if (!els.length) return;

    if (REDUCE) {
      els.forEach(el => el.classList.add('revealed'));
      return;
    }

    const io = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (!e.isIntersecting) return;
        e.target.classList.add('revealed');
        io.unobserve(e.target);
      });
    }, { threshold: 0.07, rootMargin: '0px 0px -32px 0px' });

    els.forEach((el, i) => {
      if (el.getBoundingClientRect().top < window.innerHeight * 0.9) {
        el.classList.add('revealed');
        return;
      }
      el.style.setProperty('--reveal-delay', (i % 5) * 0.08 + 's');
      io.observe(el);
    });
  }

  // ─── 5. Chart Bar Scroll Animation ───────────────────────────────────────
  function initChartBars() {
    const tracks = document.querySelectorAll('.chart-track');
    if (!tracks.length || REDUCE) return;

    const io = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.classList.add('chart-animated');
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.3 });

    tracks.forEach(t => io.observe(t));
  }

  // ─── 6. Nav depth shadow on scroll ───────────────────────────────────────
  function initNav() {
    const nav = document.querySelector('header');
    if (!nav) return;
    let was = false;
    window.addEventListener('scroll', () => {
      const now = window.scrollY > 8;
      if (now !== was) {
        was = now;
        nav.classList.toggle('nav--elevated', now);
      }
    }, { passive: true });
  }

  // ─── 7. Pointer-based Drag Engine (Matching + Sequencing) ────────────────
  // Single mouse+touch+pen code path via Pointer Events. No native HTML5
  // Drag-and-Drop API (unreliable on touchscreens). Each drag-related qtype
  // also exposes an equivalent non-drag control (select dropdown / up-down
  // buttons) wired to the exact same hidden input, so the activity stays
  // fully keyboard/screen-reader operable.
  function makeDraggable(el, { onMove, onDrop } = {}) {
    el.style.touchAction = 'none';
    let dragging = false;
    let startX = 0, startY = 0;

    el.addEventListener('pointerdown', (e) => {
      if (e.button !== undefined && e.button !== 0) return;
      dragging = true;
      startX = e.clientX;
      startY = e.clientY;
      el.setPointerCapture(e.pointerId);
      el.classList.add('is-dragging');
    });

    el.addEventListener('pointermove', (e) => {
      if (!dragging) return;
      const dx = e.clientX - startX;
      const dy = e.clientY - startY;
      el.style.transform = `translate(${dx}px, ${dy}px)`;
      if (onMove) onMove(e);
    });

    function end(e) {
      if (!dragging) return;
      dragging = false;
      el.classList.remove('is-dragging');
      el.style.transform = '';
      if (onDrop) onDrop(e);
    }

    el.addEventListener('pointerup', end);
    el.addEventListener('pointercancel', end);
  }

  function initMatchingActivity(root) {
    const bank = Array.from(root.querySelectorAll('[data-matching-item]'));
    const slots = Array.from(root.querySelectorAll('[data-drop-target]'));
    const pairingInput = root.querySelector('input[name="pairing"]');
    if (!bank.length || !slots.length || !pairingInput) return;

    function syncPairing() {
      const pairing = {};
      slots.forEach(slot => {
        const select = slot.querySelector('[data-slot-select]');
        if (select.value !== '') pairing[slot.dataset.slotIndex] = parseInt(select.value, 10);
      });
      pairingInput.value = JSON.stringify(pairing);

      const usedIndices = new Set(Object.values(pairing));
      bank.forEach(item => {
        item.classList.toggle('matching-item-placed', usedIndices.has(parseInt(item.dataset.itemIndex, 10)));
      });
    }

    slots.forEach(slot => {
      const select = slot.querySelector('[data-slot-select]');
      if (select) select.addEventListener('change', syncPairing);
    });

    function slotUnderPoint(e) {
      return slots.find(slot => {
        const r = slot.getBoundingClientRect();
        return e.clientX >= r.left && e.clientX <= r.right && e.clientY >= r.top && e.clientY <= r.bottom;
      });
    }

    bank.forEach(item => {
      makeDraggable(item, {
        onMove: (e) => {
          const over = slotUnderPoint(e);
          slots.forEach(slot => slot.classList.toggle('drop-target-active', slot === over));
        },
        onDrop: (e) => {
          slots.forEach(slot => slot.classList.remove('drop-target-active'));
          const target = slotUnderPoint(e);
          if (target) {
            const select = target.querySelector('[data-slot-select]');
            select.value = item.dataset.itemIndex;
            syncPairing();
          }
        },
      });
    });

    syncPairing();
  }

  function initSequencingActivity(root) {
    const list = root.querySelector('[data-sequencing-list]');
    const orderInput = root.querySelector('input[name="order"]');
    if (!list || !orderInput) return;

    function items() {
      return Array.from(list.querySelectorAll('[data-sequencing-item]'));
    }

    function syncOrder() {
      orderInput.value = JSON.stringify(items().map(i => i.dataset.stepText));
    }

    function findInsertBefore(item, pointerY) {
      const siblings = items().filter(i => i !== item);
      for (const sib of siblings) {
        const r = sib.getBoundingClientRect();
        if (pointerY < r.top + r.height / 2) return sib;
      }
      return null;
    }

    items().forEach(item => {
      const up = item.querySelector('[data-move-up]');
      const down = item.querySelector('[data-move-down]');
      if (up) up.addEventListener('click', () => {
        const prev = item.previousElementSibling;
        if (prev) { list.insertBefore(item, prev); syncOrder(); }
      });
      if (down) down.addEventListener('click', () => {
        const next = item.nextElementSibling;
        if (next) { list.insertBefore(next, item); syncOrder(); }
      });

      makeDraggable(item, {
        onMove: (e) => {
          const target = findInsertBefore(item, e.clientY);
          items().forEach(i => i.classList.remove('sequencing-target'));
          (target || list.lastElementChild)?.classList.add('sequencing-target');
        },
        onDrop: (e) => {
          items().forEach(i => i.classList.remove('sequencing-target'));
          const target = findInsertBefore(item, e.clientY);
          if (target) list.insertBefore(item, target);
          else list.appendChild(item);
          syncOrder();
        },
      });
    });

    syncOrder();
  }

  function initDragActivities() {
    document.querySelectorAll('[data-matching]').forEach(initMatchingActivity);
    document.querySelectorAll('[data-sequencing]').forEach(initSequencingActivity);
  }

  // ─── Boot ─────────────────────────────────────────────────────────────────
  function boot() {
    if (!REDUCE) initNeuralCanvas();
    initTiltCards();
    initTimeline();
    initFoldReveal();
    initChartBars();
    initNav();
    initDragActivities();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
