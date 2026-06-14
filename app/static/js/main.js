// Tiny progressive enhancement. Alpine and HTMX handle the rest.
// Adds a gentle reveal to cards as they scroll into view.

(function () {
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce || !("IntersectionObserver" in window)) return;

  const targets = document.querySelectorAll("section > div");
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) {
        e.target.style.transition = "opacity .5s ease, transform .5s ease";
        e.target.style.opacity = "1";
        e.target.style.transform = "none";
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.08 });

  // Only animate below the fold so the hero stays instant.
  targets.forEach((el, i) => {
    if (el.getBoundingClientRect().top < window.innerHeight) return;
    el.style.opacity = "0";
    el.style.transform = "translateY(12px)";
    io.observe(el);
  });
})();
