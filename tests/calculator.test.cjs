const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
for (const [cpu, mem, disk, total, usage] of [
  [1, 2, 0, '$40.00', '$40.00'],
  [0.5, 0.8, 0, '$25.00', '$18.00'],
  [0, 0, 0, '$25.00', '$0.00'],
  [1, 2, 10, '$41.50', '$41.50'],
]) {
  const outputs = Object.fromEntries(['total', 'hourly', 'free', 'breakdown'].map(k => [k, {textContent: ''}]));
  const inputs = Object.entries({cpu, mem, disk}).map(([key, value]) => ({dataset: {value: key}, value, addEventListener() {}}));
  const calc = {
    dataset: {mode: 'account', rateCpu: '20', rateMem: '10', rateDisk: '0.15'},
    querySelectorAll: () => inputs,
    querySelector(selector) {
      const match = selector.match(/data-result="(.*?)"/);
      return match ? outputs[match[1]] : {addEventListener() {}};
    },
  };
  vm.runInNewContext(fs.readFileSync('site/calculator.js', 'utf8'), {document: {querySelectorAll: () => [calc]}});
  assert.equal(outputs.total.textContent, total);
  assert.ok(outputs.free.textContent.includes(usage), outputs.free.textContent);
  assert.ok(!outputs.free.textContent.includes('First $5'));
}
console.log('Calculator: 4 Paid billing scenarios passed');
// Campaign copy must not send customers to the retired prepaid wallet.
{
  const nodes = {'offer-message': {textContent: ''}, 'offer-note': {textContent: ''}};
  vm.runInNewContext(fs.readFileSync('site/w2.js', 'utf8'), {
    window: {INFERRA_ANALYTICS: {offerCodes: ['WELCOME']}},
    location: {pathname: '/start/', search: '?offer=WELCOME'}, URLSearchParams,
    document: {getElementById: id => nodes[id]},
  });
  assert.ok(!Object.values(nodes).some(node => /wallet|redeem/i.test(node.textContent)));
  assert.ok(nodes['offer-note'].textContent.includes('support@inferralab.com'));
}
