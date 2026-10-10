(() => {
  const money = (value, digits = 2) => {
    const scale = 10 ** digits;
    return '$' + (Math.round((value + Number.EPSILON * Math.max(1, value)) * scale) / scale).toFixed(digits);
  };
  document.querySelectorAll('.calc').forEach(calc => {
    const rates = { cpu: Number(calc.dataset.rateCpu), mem: Number(calc.dataset.rateMem), disk: Number(calc.dataset.rateDisk) };
    const inputs = [...calc.querySelectorAll('[data-value]')];
    const result = name => calc.querySelector(`[data-result="${name}"]`);
    function update() {
      const values = Object.fromEntries(inputs.map(input => [input.dataset.value, Number(input.value) || 0]));
      const count = calc.dataset.mode === 'apps' ? values.apps * values.instances : 1;
      const cpu = count * values.cpu * rates.cpu;
      const mem = count * values.mem * rates.mem;
      const disk = values.disk * rates.disk;
      const monthly = cpu + mem + disk;
      result('total').textContent = money(monthly);
      result('hourly').textContent = money(monthly / 730, 4) + ' per hour (before free usage)';
      result('free').textContent = `First $5 free each month per account: covers ${money(Math.min(5, monthly))}; ${money(Math.max(0, monthly - 5))} after free usage.`;
      result('breakdown').textContent = `CPU ${money(cpu)} + memory ${money(mem)} + storage ${money(disk)} / month`;
    }
    inputs.forEach(input => {
      const range = calc.querySelector(`[data-range="${input.dataset.value}"]`);
      function sync(source, target) {
        if (source.value === '' || !Number.isFinite(Number(source.value))) return;
        const min = Number(source.min), max = Number(source.max), step = Number(source.step);
        const value = Math.min(max, Math.max(min, Math.round(Number(source.value) / step) * step));
        source.value = target.value = String(Number(value.toFixed(4)));
        update();
      }
      input.addEventListener('input', () => sync(input, range));
      input.addEventListener('change', () => {
        if (input.value === '') input.value = '0';
        sync(input, range);
      });
      range.addEventListener('input', () => sync(range, input));
    });
    update();
  });
})();
