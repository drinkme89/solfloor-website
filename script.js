document.addEventListener('DOMContentLoaded', () => {
  const header = document.querySelector('.site-header');
  const onScroll = () => {
    header.classList.toggle('scrolled', window.scrollY > 40);
  };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  const toggle = document.querySelector('.nav-toggle');
  const closeBtn = document.querySelector('.mobile-nav-close');
  const mobileNav = document.querySelector('.mobile-nav');
  const openNav = () => mobileNav.classList.add('open');
  const closeNav = () => mobileNav.classList.remove('open');
  toggle?.addEventListener('click', openNav);
  closeBtn?.addEventListener('click', closeNav);
  mobileNav?.querySelectorAll('a').forEach(a => a.addEventListener('click', closeNav));

  const revealEls = document.querySelectorAll('.reveal');
  const io = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('in');
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });
  revealEls.forEach(el => io.observe(el));

  const yearEl = document.querySelector('[data-year]');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  document.querySelectorAll('.service-tile-head').forEach(btn => {
    btn.addEventListener('click', () => {
      const tile = btn.closest('.service-tile');
      const isOpen = tile.classList.toggle('is-open');
      btn.setAttribute('aria-expanded', String(isOpen));
    });
  });
});
