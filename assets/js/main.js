/* =====================================================================
   Adwokat Piotr Modzelewski — main script
   ---------------------------------------------------------------------
   Drobne efekty wizualne:
   - cień pod nawigacją po przewinięciu
   - animacja pojawiania sekcji ('.reveal')
   - zamykanie menu mobilnego po kliknięciu w link
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
