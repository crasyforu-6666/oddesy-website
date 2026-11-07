(() => {
  // Mobile navigation
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.getElementById('primary-nav');
  const mobile = () => window.matchMedia('(max-width: 960px)').matches;
  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    document.body.style.overflow = open ? 'hidden' : '';
  });

  // Services submenu: first tap opens it on mobile, second tap follows the link
  document.querySelectorAll('.has-sub > .sub-trigger').forEach(a => {
    a.addEventListener('click', ev => {
      const li = a.parentElement;
      if (mobile() && !li.classList.contains('open')) {
        ev.preventDefault();
        li.classList.add('open');
      }
    });
  });
  document.addEventListener('keydown', ev => {
    if (ev.key === 'Escape') document.querySelectorAll('.has-sub.open').forEach(li => li.classList.remove('open'));
  });

  // Reveal on scroll
  const els = document.querySelectorAll('.svc-card, .why-card, .timeline li, .ind-grid li, .ind-card, .offer, .model, .check-list li');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(entries => entries.forEach(en => {
      if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
    }), { threshold: 0.1 });
    els.forEach(el => { el.classList.add('reveal'); io.observe(el); });
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
