const API_BASE_URL = "http://127.0.0.1:8000";

// ============================================================
// LOADING + LOGIN
// ============================================================

document.addEventListener("DOMContentLoaded", () => {

    // ============================================================
    // TRANSIÇÃO LOADING
    // ============================================================

    setTimeout(() => {

        const loadingScreen =
            document.getElementById("loading-screen");

        const loginScreen =
            document.getElementById("login-screen");

        loadingScreen.style.opacity = "0";

        setTimeout(() => {

            loadingScreen.style.display = "none";

            loginScreen.style.display = "block";

            document.body.style.overflow = "auto";

        }, 500);

    }, 2500);

    // ============================================================
    // APENAS NÚMEROS NO CPF
    // ============================================================

    const camposNumeros =
        document.querySelectorAll(".apenas-numeros");

    camposNumeros.forEach((campo) => {

        campo.addEventListener("input", (event) => {

            event.target.value =
                event.target.value.replace(/\D/g, "");

        });

    });

    // ============================================================
    // FORMULÁRIO LOGIN
    // ============================================================

    const formulario =
        document.getElementById("form-acesso");

    formulario.addEventListener(
        "submit",
        async function (evento) {

            evento.preventDefault();

            // ============================================================
            // CAPTURA DADOS
            // ============================================================

            const cpf =
                document.getElementById("inputCpf").value;

            const senha =
                document.getElementById("inputSenha").value;

            // ============================================================
            // BOTÃO
            // ============================================================

            const botaoLogin =
                formulario.querySelector("button");

            botaoLogin.disabled = true;

            botaoLogin.innerText = "Entrando...";

            try {

                // ============================================================
                // REQUISIÇÃO PARA O BACKEND
                // ============================================================

                const resposta = await fetch(
                    `${API_BASE_URL}/auth/login`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type": "application/json"
                        },

                        body: JSON.stringify({
                            cpf: cpf,
                            senha: senha
                        })
                    }
                );

                const dados = await resposta.json();

                // ============================================================
                // ERRO LOGIN
                // ============================================================

                if (!resposta.ok) {

                    throw new Error(
                        dados.detail || "Erro ao realizar login"
                    );
                }

                // ============================================================
                // SALVA TOKEN
                // ============================================================

                localStorage.setItem(
                    "token",
                    dados.access_token
                );

                // ============================================================
                // SALVA DADOS USUÁRIO
                // ============================================================

                localStorage.setItem(
                    "usuario",
                    JSON.stringify({
                        nome: dados.nome,
                        perfil: dados.perfil
                    })
                );

                // ============================================================
                // LOGIN SUCESSO
                // ============================================================

                alert("Login realizado com sucesso!");

                // ============================================================
                // REDIRECIONA
                // ============================================================

                window.location.href =
                    "pages/dashboard.html";

            } catch (erro) {

                // ============================================================
                // ERRO
                // ============================================================

                alert(erro.message);

            } finally {

                // ============================================================
                // REATIVA BOTÃO
                // ============================================================

                botaoLogin.disabled = false;

                botaoLogin.innerText = "Acessar";
            }
        }
    );
});