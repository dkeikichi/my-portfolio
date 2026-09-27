// ============================================================
// Language links (/ ⇄ /ja/): remember the visitor's choice so a
// later visit to "/" can go straight to /ja/ (see <head> in index.html)
// ============================================================
(function () {
    document.querySelectorAll('.lang-toggle a[hreflang]').forEach(function (link) {
        link.addEventListener('click', function () {
            try { localStorage.setItem('lang', link.getAttribute('hreflang')); } catch (e) {}
        });
    });
})();

// ============================================================
// Fade-in-on-scroll for .reveal elements
// ============================================================
(function () {
    var items = document.querySelectorAll('.reveal');
    if (!('IntersectionObserver' in window)) {
        items.forEach(function (el) { el.classList.add('visible'); });
        return;
    }
    var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.12 });
    items.forEach(function (el) { observer.observe(el); });
})();
