// ============================================================
// Language toggle (EN ⇄ JA)
// ============================================================
(function () {
    var enBtn = document.getElementById('lang-en-btn');
    var jaBtn = document.getElementById('lang-ja-btn');

    function setLang(lang) {
        document.documentElement.lang = lang;
        try { localStorage.setItem('lang', lang); } catch (e) {}
        var isEn = lang === 'en';
        enBtn.classList.toggle('active', isEn);
        jaBtn.classList.toggle('active', !isEn);
        enBtn.setAttribute('aria-pressed', String(isEn));
        jaBtn.setAttribute('aria-pressed', String(!isEn));
    }

    enBtn.addEventListener('click', function () { setLang('en'); });
    jaBtn.addEventListener('click', function () { setLang('ja'); });

    // Sync button state with the language chosen pre-paint in <head>.
    setLang(document.documentElement.lang === 'ja' ? 'ja' : 'en');
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
