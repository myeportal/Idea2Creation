document.addEventListener('DOMContentLoaded', () => {
  const faqItems = document.querySelectorAll('.faq-item');
  faqItems.forEach((item) => {
    const button = item.querySelector('.faq-question');
    const icon = button?.querySelector('span');
    button?.addEventListener('click', () => {
      item.classList.toggle('active');
      if (icon) icon.textContent = item.classList.contains('active') ? '−' : '+';
    });
  });

  function updateCountdown() {
    const now = new Date();
    const endOfDay = new Date();
    endOfDay.setHours(23, 59, 59, 999);
    const diff = Math.max(0, endOfDay - now);

    const hours = Math.floor(diff / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((diff % (1000 * 60)) / 1000);

    const timer = document.getElementById('countdown-timer');
    if (timer) {
      timer.textContent = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    }
  }

  updateCountdown();
  setInterval(updateCountdown, 1000);

  const progressBar = document.getElementById('progress-bar');
  const backToTop = document.getElementById('back-to-top');

  const updateScrollUI = () => {
    const winScroll = document.documentElement.scrollTop || document.body.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = height > 0 ? (winScroll / height) * 100 : 0;
    if (progressBar) progressBar.style.width = `${scrolled}%`;

    if (backToTop) {
      if (window.scrollY > 500) backToTop.classList.add('visible');
      else backToTop.classList.remove('visible');
    }
  };

  window.addEventListener('scroll', updateScrollUI);
  updateScrollUI();

  backToTop?.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.animate(
            [
              { opacity: 0, transform: 'translateY(20px)' },
              { opacity: 1, transform: 'translateY(0)' },
            ],
            { duration: 500, easing: 'ease-out', fill: 'forwards' }
          );
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
  );

  document.querySelectorAll('.gallery-card, .card, .price-card, .faq-item, .guarantee').forEach((el) => {
    el.style.opacity = '0';
    observer.observe(el);
  });
});
