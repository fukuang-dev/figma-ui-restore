import test from 'node:test';
import assert from 'node:assert/strict';
import { sendFeedback, FeedbackError } from '../website/assets/feedback.mjs';

const payload = { access_key: 'test-form-id', message: 'A harmless test', category: 'bug' };
const response = (status, data) => ({ status, ok: status >= 200 && status < 300, json: async () => data });
const kind = expected => error => error instanceof FeedbackError && error.kind === expected;

test('sends only the supplied payload to the fixed HTTPS endpoint without cookies', async () => {
  let calls = 0;
  await sendFeedback(payload, { fetchImpl: async (url, options) => {
    calls++;
    assert.equal(url, 'https://api.web3forms.com/submit');
    assert.equal(options.method, 'POST');
    assert.equal(options.credentials, 'omit');
    assert.deepEqual(JSON.parse(options.body), payload);
    assert.equal(options.headers.Accept, 'application/json');
    return response(200, { success: true });
  } });
  assert.equal(calls, 1);
});

test('requires both a successful HTTP status and explicit boolean acceptance', async t => {
  for (const [status, data] of [[200, { success: false }], [200, { success: 'true' }], [200, {}], [400, { success: true }]]) {
    await t.test(JSON.stringify([status, data]), async () => {
      await assert.rejects(sendFeedback(payload, { fetchImpl: async () => response(status, data) }), kind('invalid'));
    });
  }
});

test('quota and rate limits produce retryable rate feedback', async () => {
  await assert.rejects(sendFeedback(payload, { fetchImpl: async () => response(429, {}) }), kind('rate'));
});

test('server errors and malformed responses never report success', async () => {
  await assert.rejects(sendFeedback(payload, { fetchImpl: async () => response(503, { success: true }) }), kind('uncertain'));
  await assert.rejects(sendFeedback(payload, { fetchImpl: async () => ({ status: 200, ok: true, json: async () => { throw new SyntaxError(); } }) }), kind('uncertain'));
});

test('network errors preserve uncertainty and do not automatically resend', async () => {
  let calls = 0;
  await assert.rejects(sendFeedback(payload, { fetchImpl: async () => { calls++; throw new TypeError('offline'); } }), kind('uncertain'));
  assert.equal(calls, 1);
});

test('timeout aborts the in-flight request without starting another', async () => {
  let calls = 0;
  await assert.rejects(sendFeedback(payload, { timeoutMs: 5, fetchImpl: (_url, { signal }) => {
    calls++;
    return new Promise((_resolve, reject) => signal.addEventListener('abort', () => reject(new Error('aborted')), { once: true }));
  } }), kind('uncertain'));
  assert.equal(calls, 1);
});
