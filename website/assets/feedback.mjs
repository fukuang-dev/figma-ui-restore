const FEEDBACK_ENDPOINT = 'https://api.web3forms.com/submit';

export class FeedbackError extends Error {
  constructor(kind) {
    super(kind);
    this.kind = kind;
  }
}

// The Form ID is public. Only the provider controls its recipient and quotas.
export async function sendFeedback(payload, { fetchImpl = globalThis.fetch, timeoutMs = 20000 } = {}) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await fetchImpl(FEEDBACK_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      credentials: 'omit',
      referrerPolicy: 'strict-origin-when-cross-origin',
      body: JSON.stringify(payload),
      signal: controller.signal,
    });
    if (response.status === 429) throw new FeedbackError('rate');
    let data;
    try { data = await response.json(); }
    catch { throw new FeedbackError('uncertain'); }
    if (!response.ok || data?.success !== true) {
      throw new FeedbackError(response.status >= 500 ? 'uncertain' : 'invalid');
    }
    return data;
  } catch (error) {
    if (error instanceof FeedbackError) throw error;
    // A timeout can happen after delivery. Preserve the message; never retry automatically.
    throw new FeedbackError('uncertain');
  } finally {
    clearTimeout(timer);
  }
}

export function initFeedback() {
  const dialog = document.querySelector('#feedback-dialog');
  if (!dialog || typeof dialog.showModal !== 'function') return;
  const form = dialog.querySelector('#feedback-form');
  const fields = form.querySelector('.feedback-fields');
  const message = form.elements.message;
  const email = form.elements.email;
  const submit = form.querySelector('[type="submit"]');
  const status = form.querySelector('[data-feedback-status]');
  const compose = dialog.querySelector('[data-feedback-compose]');
  const success = dialog.querySelector('[data-feedback-success]');
  const key = form.dataset.formKey;
  let opener;
  let pending = false;
  let accepted = false;
  let successViewed = false;

  const labelSubmit = text => {
    submit.replaceChildren(document.createTextNode(text));
    const arrow = document.createElement('span');
    arrow.setAttribute('aria-hidden', 'true');
    arrow.textContent = '↗';
    submit.append(arrow);
  };
  const updateCount = () => {
    dialog.querySelector('[data-feedback-count]').textContent = String(message.value.length);
    message.setCustomValidity('');
  };
  const showStatus = (kind, text) => {
    status.dataset.state = kind;
    status.textContent = text;
  };
  if (!key) {
    submit.disabled = true;
    showStatus('error', form.dataset.unavailable);
  }
  document.querySelectorAll('[data-feedback-open]').forEach(link => {
    link.addEventListener('click', event => {
      event.preventDefault();
      if (dialog.open) return;
      opener = link;
      if (accepted && successViewed) {
        compose.hidden = false;
        success.hidden = true;
        accepted = false;
        successViewed = false;
        showStatus('', '');
        labelSubmit(form.dataset.submit);
      }
      dialog.showModal();
      document.documentElement.classList.add('feedback-open');
      if (accepted) {
        successViewed = true;
        success.querySelector('h3').focus();
      }
    });
  });
  dialog.querySelectorAll('[data-feedback-close]').forEach(button => {
    button.addEventListener('click', () => dialog.close());
  });
  // Close only a genuine backdrop click, not padding inside the dialog or a drag from the form.
  let backdropDown = false;
  dialog.addEventListener('pointerdown', event => { backdropDown = event.target === dialog; });
  dialog.addEventListener('click', event => {
    if (backdropDown && event.target === dialog) {
      const rect = dialog.getBoundingClientRect();
      if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
    }
    backdropDown = false;
  });
  dialog.addEventListener('keydown', event => {
    if (event.key !== 'Tab') return;
    const controls = [...dialog.querySelectorAll('button, a[href], input, textarea')]
      .filter(control => !control.disabled && control.tabIndex >= 0 && control.getClientRects().length);
    const first = controls[0];
    const last = controls.at(-1);
    if (!first || !last) return;
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });
  dialog.addEventListener('close', () => {
    document.documentElement.classList.remove('feedback-open');
    opener?.focus({ preventScroll: true });
  });
  message.addEventListener('input', updateCount);
  form.addEventListener('submit', async event => {
    event.preventDefault();
    if (pending || !key || accepted) return;
    message.setCustomValidity(message.value.replace(/\s/g, '').length < 5 ? form.dataset.short : '');
    if (!form.reportValidity()) return;
    if (form.elements.botcheck.checked) {
      showStatus('error', form.dataset.invalid);
      return;
    }
    // Explicit allowlist: no query string, private URL fragments, browser logs or credentials.
    const payload = {
      access_key: key,
      subject: '[Figma UI Restore] Website feedback',
      from_name: 'Figma UI Restore',
      category: form.elements.category.value,
      message: message.value.trim(),
      page: location.origin + location.pathname,
      language: document.documentElement.lang,
      botcheck: false,
    };
    if (email.value.trim()) payload.email = email.value.trim();
    pending = true;
    fields.disabled = true;
    submit.disabled = true;
    form.setAttribute('aria-busy', 'true');
    labelSubmit(form.dataset.sending);
    showStatus('pending', form.dataset.sending);
    try {
      await sendFeedback(payload);
      accepted = true;
      showStatus('', '');
      form.reset();
      updateCount();
      compose.hidden = true;
      success.hidden = false;
      if (dialog.open) {
        successViewed = true;
        success.querySelector('h3').focus();
      }
    } catch (error) {
      showStatus('error', form.dataset[error.kind] || form.dataset.uncertain);
      labelSubmit(form.dataset.retry);
    } finally {
      pending = false;
      fields.disabled = false;
      submit.disabled = false;
      form.removeAttribute('aria-busy');
      if (accepted) labelSubmit(form.dataset.submit);
    }
  });
}

if (typeof document !== 'undefined') initFeedback();
