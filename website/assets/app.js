'use strict';
const header = document.querySelector('.site-header');
const toggle = document.querySelector('.menu-toggle');
if (header && toggle) {
  header.classList.add('js-menu');
  header.dataset.open = 'false';
  const closeMenu = () => {
    header.dataset.open = 'false';
    toggle.setAttribute('aria-expanded', 'false');
  };
  toggle.addEventListener('click', () => {
    const open = header.dataset.open !== 'true';
    header.dataset.open = String(open);
    toggle.setAttribute('aria-expanded', String(open));
  });
  header.querySelectorAll('nav a').forEach(link => link.addEventListener('click', closeMenu));
  header.addEventListener('keydown', event => {
    if (event.key === 'Escape' && header.dataset.open === 'true') {
      closeMenu();
      toggle.focus();
    }
  });
  window.matchMedia('(min-width: 801px)').addEventListener('change', closeMenu);
}
document.querySelectorAll('[data-copy]').forEach(button => {
  button.addEventListener('click', async () => {
    const content = button.closest('.code-block').querySelector('code');
    const status = document.querySelector('#copy-status');
    try {
      if (!navigator.clipboard) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(content.textContent);
      button.textContent = button.dataset.copiedLabel + ' ✓';
      status.textContent = button.dataset.copiedLabel;
      setTimeout(() => { button.textContent = button.dataset.copyLabel + ' ↗'; }, 2200);
    } catch {
      const selection = window.getSelection();
      const range = document.createRange();
      range.selectNodeContents(content);
      selection.removeAllRanges();
      selection.addRange(range);
      button.textContent = button.dataset.manualLabel;
      status.textContent = button.dataset.copyFail;
    }
  });
});
document.querySelectorAll('[data-demo]').forEach(demo => {
  demo.querySelectorAll('[data-demo-mode]').forEach(button => {
    button.addEventListener('click', () => {
      const good = button.dataset.demoMode === 'after';
      demo.dataset.good = String(good);
      demo.querySelectorAll('[data-demo-mode]').forEach(control => {
        control.setAttribute('aria-pressed', String(control === button));
      });
      demo.querySelector('[data-font-value]').textContent = good ? '24px / 600' : '32px / 600';
      demo.querySelector('[data-radius-value]').textContent = good ? 'radius 8px' : 'radius 16px';
      const status = demo.querySelector('[data-demo-status]');
      status.textContent = good ? status.dataset.after : status.dataset.before;
    });
  });
});
