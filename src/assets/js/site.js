(() => {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isMobile = () => window.matchMedia('(max-width: 960px)').matches;

  // Header state on scroll
  const header = document.querySelector('.site-header');
  const onScroll = () => header.classList.toggle('scrolled', window.scrollY > 20);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  // Mobile menu
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.getElementById('primary-nav');
  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  });
  document.querySelectorAll('.has-sub > .sub-trigger').forEach(a => {
    a.addEventListener('click', ev => {
      const li = a.parentElement;
      if (isMobile() && !li.classList.contains('open')) { ev.preventDefault(); li.classList.add('open'); }
    });
  });
  document.addEventListener('keydown', ev => {
    if (ev.key !== 'Escape') return;
    document.querySelectorAll('.has-sub.open').forEach(li => li.classList.remove('open'));
    if (nav.classList.contains('open')) toggle.click();
  });

  // Reveal on scroll, with stagger inside each group
  const items = document.querySelectorAll('.reveal, .dash-wrap');
  if ('IntersectionObserver' in window && !reduce) {
    const groups = new Map();
    items.forEach(el => {
      const p = el.parentElement;
      const i = groups.get(p) || 0;
      groups.set(p, i + 1);
      el.style.setProperty('--d', `${Math.min(i, 6) * 0.07}s`);
    });
    const io = new IntersectionObserver(entries => entries.forEach(en => {
      if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
    }), { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    items.forEach(el => io.observe(el));
  } else {
    items.forEach(el => el.classList.add('in'));
  }

  // Cursor spotlight on cards
  document.querySelectorAll('.spot').forEach(card => {
    card.addEventListener('pointermove', ev => {
      const r = card.getBoundingClientRect();
      card.style.setProperty('--mx', `${ev.clientX - r.left}px`);
      card.style.setProperty('--my', `${ev.clientY - r.top}px`);
    });
  });

  // Process timeline progress
  const steps = document.querySelector('.steps');
  if (steps) {
    const list = [...steps.querySelectorAll('.step')];
    const update = () => {
      const r = steps.getBoundingClientRect();
      const mid = window.innerHeight * 0.6;
      const prog = Math.max(0, Math.min(1, (mid - r.top) / r.height));
      steps.style.setProperty('--prog', `${prog * 100}%`);
      list.forEach(s => s.classList.toggle('active', s.getBoundingClientRect().top < mid));
    };
    update();
    window.addEventListener('scroll', update, { passive: true });
  }

  // ECC countdown
  const cd = document.querySelector('.countdown');
  if (cd) {
    const end = new Date(cd.dataset.deadline).getTime();
    const out = u => cd.querySelector(`[data-u="${u}"]`);
    const tick = () => {
      let s = Math.max(0, Math.floor((end - Date.now()) / 1000));
      const d = Math.floor(s / 86400); s -= d * 86400;
      const h = Math.floor(s / 3600); s -= h * 3600;
      const m = Math.floor(s / 60); s -= m * 60;
      out('d').textContent = d.toLocaleString();
      out('h').textContent = String(h).padStart(2, '0');
      out('m').textContent = String(m).padStart(2, '0');
      out('s').textContent = String(s).padStart(2, '0');
    };
    tick();
    setInterval(tick, 1000);
  }

  // Contact form
  const form = document.getElementById('contact-form');
  if (!form) return;
  const cfg = window.ODDESY || {};
  const status = form.querySelector('.form-status');
  form.addEventListener('submit', async ev => {
    ev.preventDefault();
    status.className = 'form-status';
    let ok = true;
    form.querySelectorAll('[required]').forEach(f => {
      const bad = !f.value.trim() || (f.type === 'email' && !/^\S+@\S+\.\S+$/.test(f.value));
      f.classList.toggle('invalid', bad);
      f.setAttribute('aria-invalid', String(bad));
      if (bad) ok = false;
    });
    if (!ok) { status.textContent = 'Please complete the required fields with a valid email.'; status.classList.add('err'); return; }
    const data = Object.fromEntries(new FormData(form));
    if (cfg.formEndpoint) {
      try {
        const res = await fetch(cfg.formEndpoint, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(data) });
        if (!res.ok) throw new Error(res.status);
        form.reset();
        status.textContent = 'Thank you. A consultant will be in touch within one business day.';
        status.classList.add('ok');
      } catch {
        status.textContent = `Sorry, the message could not be sent. Please email ${cfg.email}.`;
        status.classList.add('err');
      }
      return;
    }
    const body = `Name: ${data.name}\nEmail: ${data.email}\nCompany: ${data.company || '-'}\nPhone: ${data.phone || '-'}\nService: ${data.interest}\n\n${data.message}`;
    location.href = `mailto:${cfg.email}?subject=${encodeURIComponent('Website enquiry: ' + data.interest)}&body=${encodeURIComponent(body)}`;
    status.textContent = 'Opening your email app...';
    status.classList.add('ok');
  });
})();
