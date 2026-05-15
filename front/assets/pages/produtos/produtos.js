// ══════════════════════════════════════
// produtos.js — Lógica da página Produtos
// ══════════════════════════════════════

const checkTodos = document.getElementById('check-todos');
const tbody = document.getElementById('tbody-produtos');

// ── Selecionar/desselecionar todos ──
checkTodos.addEventListener('change', () => {
    const checks = tbody.querySelectorAll('input[type="checkbox"]');
    checks.forEach(check => check.checked = checkTodos.checked);
});

// ── Ao mudar um checkbox individual ──
tbody.addEventListener('change', (e) => {
    if (e.target.type !== 'checkbox') return;

    const checks = tbody.querySelectorAll('input[type="checkbox"]');
    const totalChecks = checks.length;
    const totalMarcados = [...checks].filter(c => c.checked).length;

    // Se todos marcados → marca o "todos"
    // Se nenhum ou parcial → desmarca o "todos"
    checkTodos.checked = totalMarcados === totalChecks;
    checkTodos.indeterminate = totalMarcados > 0 && totalMarcados < totalChecks;
});