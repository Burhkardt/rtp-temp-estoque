// ── Mostra a opção conforme o método selecionado ──
const selectMetodo = document.getElementById('select-metodo');
const grupoImagem  = document.getElementById('grupo-imagem');
const grupoScanner = document.getElementById('grupo-scanner');
const hrMetodo     = document.getElementById('hr-metodo');
const inputImagem  = document.getElementById('input-imagem');
const nomeArquivo  = document.getElementById('nome-arquivo');

selectMetodo.addEventListener('change', () => {
    const metodo = selectMetodo.value;

    grupoImagem.style.display  = 'none';
    grupoScanner.style.display = 'none';
    hrMetodo.style.display     = 'none';

    if (metodo === 'imagem') {
        hrMetodo.style.display    = 'block';
        grupoImagem.style.display = 'block';
    } else if (metodo === 'scanner') {
        hrMetodo.style.display     = 'block';
        grupoScanner.style.display = 'block';
    }
});

// ── Mostra o nome do arquivo selecionado ──
inputImagem.addEventListener('change', () => {
    const arquivo = inputImagem.files[0];
    nomeArquivo.textContent = arquivo ? arquivo.name : 'Procurar arquivo';
});




// ── Ativar/desativar botão de busca ── 

// >>>> DEPOIS ADICIONAR LIMITE DE CARACTERES PARA SIMULAR O CÓDIGO DE BARRAS E ATIAR O BOTÃO SE NÃO TIVER O NÚMERO DE CARACTERES CORRETO (EX: 13 PARA EAN-13)

const btnBuscar    = document.getElementById('btn-buscar');
const inputScanner = document.getElementById('input-scanner');

// ── Começa desabilitado ──
btnBuscar.disabled = true;

// ── Habilita quando tiver algo digitado ── 
inputScanner.addEventListener('input', () => {
    btnBuscar.disabled = inputScanner.value.trim() === '';
});