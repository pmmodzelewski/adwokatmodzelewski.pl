/* =====================================================================
   Adwokat Piotr Modzelewski — main script
   ---------------------------------------------------------------------
   Drobne efekty wizualne:
   - cień pod nawigacją po przewinięciu
   - animacja pojawiania sekcji ('.reveal')
   - zamykanie menu mobilnego po kliknięciu w link
   - dropdown Specjalizacje (klik / klawiatura / klik poza)
   ===================================================================== */

// ----- Sekcja: Cień pod nawigacją po scrollu -----
window.addEventListener('scroll', () => {
  const nav = document.getElementById('nav');
  if (nav) nav.classList.toggle('scrolled', window.scrollY > 10);
});

// ----- Sekcja: Animacja pojawiania ('.reveal') -----
const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.15 });
document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

// ----- Sekcja: Menu mobilne -----
document.querySelectorAll('.nav-links a').forEach(a => {
  a.addEventListener('click', () => {
    const links = document.querySelector('.nav-links');
    if (links) links.classList.remove('open');
  });
});

// ----- Sekcja: Dropdown Specjalizacje -----
// Dziala dla mobilki (gdzie hover-CSS nie wystarcza), dla klawiatury
// (Enter, Escape) oraz dla zamykania klikiem poza menu.
document.querySelectorAll('.dropdown-toggle').forEach(btn => {
  const li = btn.parentElement;
  btn.addEventListener('click', (e) => {
    e.preventDefault();
    const open = li.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  document.addEventListener('click', (e) => {
    if (!li.contains(e.target)) {
      li.classList.remove('open');
      btn.setAttribute('aria-expanded', 'false');
    }
  });
  btn.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      li.classList.remove('open');
      btn.setAttribute('aria-expanded', 'false');
      btn.focus();
    }
  });
});
