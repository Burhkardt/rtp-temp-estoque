"""
test_e2e_backend.py – Testes End-to-End do Backend RTP Estoque.

Testa todas as rotas da API de ponta a ponta, usando o banco de dados
Oracle dockerizado como fonte de dados real.

Endpoints testados:
  - GET  /                              (redirect para /apidocs/)
  - POST /api/auth/login                (autenticação)
  - GET  /api/auth/estoque-vip          (rota protegida por JWT)
  - GET  /products/                     (listar produtos)
  - GET  /products/barcode/<barcode>    (buscar produto por código de barras)
  - GET  /products/<id>/barcode         (gerar imagem do código de barras)
  - POST /telegram/send                 (enviar mensagem de texto)
  - POST /telegram/send-product-tag/<id>(enviar etiqueta com código de barras)
  - POST /barcodeup/upload              (upload de imagem para leitura)
"""

import io
import pytest


# ════════════════════════════════════════════════════════════
# 1. TESTES DE SAÚDE DA APLICAÇÃO
# ════════════════════════════════════════════════════════════

class TestAppHealth:
    """Verifica se a aplicação está de pé e respondendo."""

    def test_root_redirect_to_apidocs(self, client):
        """GET / deve redirecionar (302) para /apidocs/."""
        response = client.get("/")
        assert response.status_code == 302
        assert "/apidocs/" in response.headers["Location"]

    def test_apidocs_accessible(self, client):
        """GET /apidocs/ deve retornar 200 (Swagger UI)."""
        response = client.get("/apidocs/")
        assert response.status_code == 200

    def test_apispec_json_accessible(self, client):
        """GET /apispec_1.json deve retornar a especificação Swagger."""
        response = client.get("/apispec_1.json")
        assert response.status_code == 200
        data = response.get_json()
        assert "info" in data
        assert data["info"]["title"] == "API RTP Estoque"


# ════════════════════════════════════════════════════════════
# 2. TESTES DE AUTENTICAÇÃO (AUTH)
# ════════════════════════════════════════════════════════════

class TestAuth:
    """Testa o fluxo completo de autenticação JWT."""

    def test_login_sucesso(self, client):
        """Login com credenciais corretas deve retornar 200 + token."""
        response = client.post("/api/auth/login", json={
            "username": "teste@email.com",
            "password": "123456"
        })
        assert response.status_code == 200
        data = response.get_json()
        assert "token" in data
        assert len(data["token"]) > 10  # token JWT tem no mínimo ~100 chars

    def test_login_sem_campos(self, client):
        """Login sem username/password deve retornar 400."""
        response = client.post("/api/auth/login", json={})
        assert response.status_code == 400
        data = response.get_json()
        assert "erro" in data

    def test_login_senha_errada(self, client):
        """Login com senha incorreta deve retornar 401."""
        response = client.post("/api/auth/login", json={
            "username": "teste@email.com",
            "password": "senha_errada"
        })
        assert response.status_code == 401

    def test_login_usuario_inexistente(self, client):
        """Login com e-mail inexistente deve retornar 401."""
        response = client.post("/api/auth/login", json={
            "username": "naoexiste@email.com",
            "password": "123456"
        })
        assert response.status_code == 401

    def test_login_body_vazio(self, client):
        """Login com body vazio deve retornar 400."""
        response = client.post("/api/auth/login",
                               data="",
                               content_type="application/json")
        assert response.status_code == 400

    def test_rota_protegida_com_token(self, client, auth_headers):
        """Acesso à rota VIP com token válido deve retornar 200."""
        response = client.get("/api/auth/estoque-vip", headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert "mensagem" in data
        assert "teste@email.com" in data["mensagem"]

    def test_rota_protegida_sem_token(self, client):
        """Acesso à rota VIP sem token deve retornar 401."""
        response = client.get("/api/auth/estoque-vip")
        assert response.status_code == 401

    def test_rota_protegida_token_invalido(self, client):
        """Acesso à rota VIP com token inválido deve retornar 422."""
        response = client.get("/api/auth/estoque-vip", headers={
            "Authorization": "Bearer token.invalido.aqui"
        })
        assert response.status_code == 422


# ════════════════════════════════════════════════════════════
# 3. TESTES DE PRODUTOS (PRODUCTS)
# ════════════════════════════════════════════════════════════

class TestProducts:
    """Testa os endpoints de consulta e geração de código de barras de produtos."""

    def test_listar_todos_produtos(self, client, auth_headers):
        """GET /products/ deve retornar lista de produtos com status 200."""
        response = client.get("/products/", headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert "data" in data
        assert "total" in data
        assert isinstance(data["data"], list)
        assert data["total"] >= 3  # temos 3 produtos no banco de teste

    def test_produtos_possuem_campos_corretos(self, client, auth_headers):
        """Cada produto deve conter cd_produto e ds_produto."""
        response = client.get("/products/", headers=auth_headers)
        data = response.get_json()
        produtos = data["data"]
        assert len(produtos) > 0

        produto = produtos[0]
        assert "cd_produto" in produto
        assert "ds_produto" in produto

    def test_listar_produtos_sem_token(self, client):
        """GET /products/ sem token deve retornar 401."""
        response = client.get("/products/")
        assert response.status_code == 401

    def test_buscar_produto_por_barcode_valido(self, client, auth_headers):
        """GET /products/barcode/1000000001 deve retornar o produto com ID 1."""
        response = client.get("/products/barcode/1000000001", headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert "data" in data
        assert len(data["data"]) > 0

    def test_buscar_produto_por_barcode_segundo_produto(self, client, auth_headers):
        """GET /products/barcode/1000000002 deve retornar o produto com ID 2."""
        response = client.get("/products/barcode/1000000002", headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert "data" in data

    def test_buscar_produto_barcode_inexistente(self, client, auth_headers):
        """GET /products/barcode/1999999999 deve retornar 404."""
        response = client.get("/products/barcode/1999999999", headers=auth_headers)
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data

    def test_buscar_produto_barcode_muito_curto(self, client, auth_headers):
        """GET /products/barcode/1 deve retornar 400 (código inválido)."""
        response = client.get("/products/barcode/1", headers=auth_headers)
        assert response.status_code == 400

    def test_buscar_produto_barcode_sem_token(self, client):
        """GET /products/barcode/... sem token deve retornar 401."""
        response = client.get("/products/barcode/1000000001")
        assert response.status_code == 401

    def test_gerar_imagem_barcode_produto_existente(self, client, auth_headers):
        """GET /products/1/barcode deve retornar imagem PNG."""
        response = client.get("/products/1/barcode", headers=auth_headers)
        assert response.status_code == 200
        assert response.content_type == "image/png"
        assert len(response.data) > 100  # imagem PNG tem no mínimo ~1KB

    def test_gerar_imagem_barcode_segundo_produto(self, client, auth_headers):
        """GET /products/2/barcode deve retornar imagem PNG."""
        response = client.get("/products/2/barcode", headers=auth_headers)
        assert response.status_code == 200
        assert response.content_type == "image/png"

    def test_gerar_imagem_barcode_terceiro_produto(self, client, auth_headers):
        """GET /products/3/barcode deve retornar imagem PNG."""
        response = client.get("/products/3/barcode", headers=auth_headers)
        assert response.status_code == 200
        assert response.content_type == "image/png"

    def test_gerar_imagem_barcode_produto_inexistente(self, client, auth_headers):
        """GET /products/99999/barcode deve retornar 404."""
        response = client.get("/products/99999/barcode", headers=auth_headers)
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data

    def test_gerar_barcode_sem_token(self, client):
        """GET /products/1/barcode sem token deve retornar 401."""
        response = client.get("/products/1/barcode")
        assert response.status_code == 401


# ════════════════════════════════════════════════════════════
# 4. TESTES DO TELEGRAM
# ════════════════════════════════════════════════════════════

class TestTelegram:
    """Testa os endpoints de envio de mensagens e etiquetas via Telegram."""

    def test_enviar_mensagem_texto(self, client, auth_headers):
        """POST /telegram/send com mensagem válida deve retornar sucesso."""
        response = client.post("/telegram/send", json={
            "message": "🧪 Teste E2E automatizado - pytest"
        }, headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert "message_id" in data

    def test_enviar_mensagem_sem_campo_message(self, client, auth_headers):
        """POST /telegram/send sem campo 'message' deve retornar 400."""
        response = client.post("/telegram/send", json={
            "texto": "isso não é o campo certo"
        }, headers=auth_headers)
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_enviar_mensagem_body_vazio(self, client, auth_headers):
        """POST /telegram/send com body vazio deve retornar 400."""
        response = client.post("/telegram/send",
                               data="",
                               content_type="application/json",
                               headers=auth_headers)
        assert response.status_code == 400

    def test_enviar_mensagem_sem_token(self, client):
        """POST /telegram/send sem token deve retornar 401."""
        response = client.post("/telegram/send", json={
            "message": "Tentativa sem autenticação"
        })
        assert response.status_code == 401

    def test_enviar_etiqueta_produto_existente(self, client, auth_headers):
        """POST /telegram/send-product-tag/1 deve enviar etiqueta com sucesso."""
        response = client.post("/telegram/send-product-tag/1", headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert "message_id" in data
        assert data["message"] == "Etiqueta enviada com sucesso."

    def test_enviar_etiqueta_segundo_produto(self, client, auth_headers):
        """POST /telegram/send-product-tag/2 deve enviar etiqueta com sucesso."""
        response = client.post("/telegram/send-product-tag/2", headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True

    def test_enviar_etiqueta_produto_inexistente(self, client, auth_headers):
        """POST /telegram/send-product-tag/99999 deve retornar 404."""
        response = client.post("/telegram/send-product-tag/99999", headers=auth_headers)
        assert response.status_code == 404
        data = response.get_json()
        assert data["success"] is False
        assert "Produto não encontrado" in data["error"]

    def test_enviar_etiqueta_sem_token(self, client):
        """POST /telegram/send-product-tag/1 sem token deve retornar 401."""
        response = client.post("/telegram/send-product-tag/1")
        assert response.status_code == 401

    def test_enviar_mensagem_com_html_parse_mode(self, client, auth_headers):
        """POST /telegram/send com parse_mode HTML deve funcionar."""
        response = client.post("/telegram/send", json={
            "message": "<b>Teste E2E</b> - parse mode HTML",
            "parse_mode": "HTML"
        }, headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True


# ════════════════════════════════════════════════════════════
# 5. TESTES DE UPLOAD DE CÓDIGO DE BARRAS (BARCODE IMAGE)
# ════════════════════════════════════════════════════════════

class TestBarcodeUpload:
    """Testa o endpoint de upload e leitura de código de barras por imagem."""

    def test_upload_sem_arquivo(self, client, auth_headers):
        """POST /barcodeup/upload sem arquivo deve retornar 400."""
        response = client.post("/barcodeup/upload", headers=auth_headers)
        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data

    def test_upload_arquivo_nome_vazio(self, client, auth_headers):
        """POST /barcodeup/upload com filename vazio deve retornar 400."""
        data = {
            "barcode_image": (io.BytesIO(b"fake"), "")
        }
        response = client.post(
            "/barcodeup/upload",
            data=data,
            content_type="multipart/form-data",
            headers=auth_headers
        )
        assert response.status_code == 400

    def test_upload_imagem_sem_barcode(self, client, auth_headers):
        """POST /barcodeup/upload com imagem sem código de barras deve retornar 422."""
        # Cria uma imagem PNG mínima válida (1x1 pixel branco)
        # PNG header + IHDR + IDAT + IEND
        png_1x1 = (
            b"\x89PNG\r\n\x1a\n"  # PNG signature
            b"\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02"
            b"\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx"
            b"\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x18\xd8N"
            b"\x00\x00\x00\x00IEND\xaeB`\x82"
        )
        data = {
            "barcode_image": (io.BytesIO(png_1x1), "imagem_sem_barcode.png")
        }
        response = client.post(
            "/barcodeup/upload",
            data=data,
            content_type="multipart/form-data",
            headers=auth_headers
        )
        assert response.status_code == 422
        resp_data = response.get_json()
        assert resp_data["status"] == "erro"

    def test_upload_sem_token(self, client):
        """POST /barcodeup/upload sem token deve retornar 401."""
        response = client.post("/barcodeup/upload")
        assert response.status_code == 401

    def test_upload_imagem_barcode_gerado(self, client, auth_headers):
        """
        Fluxo completo: gera o barcode do produto 1 via API,
        faz upload da imagem gerada, e verifica se o código é lido corretamente.
        """
        # 1. Gera a imagem do código de barras do produto 1
        barcode_response = client.get("/products/1/barcode", headers=auth_headers)
        assert barcode_response.status_code == 200
        barcode_image = barcode_response.data

        # 2. Faz upload da imagem gerada para o endpoint de leitura
        data = {
            "barcode_image": (io.BytesIO(barcode_image), "barcode_test.png")
        }
        upload_response = client.post(
            "/barcodeup/upload",
            data=data,
            content_type="multipart/form-data",
            headers=auth_headers
        )
        assert upload_response.status_code == 200
        resp_data = upload_response.get_json()
        assert resp_data["status"] == "sucesso"
        assert isinstance(resp_data["codigos"], list)
        assert len(resp_data["codigos"]) > 0
        # O código lido deve ser '1000000001' (id_to_barcode(1))
        assert "1000000001" in resp_data["codigos"]


# ════════════════════════════════════════════════════════════
# 6. TESTES DE FLUXO COMPLETO (INTEGRAÇÃO E2E)
# ════════════════════════════════════════════════════════════

class TestFluxoCompleto:
    """
    Testa cenários de integração que combinam múltiplos endpoints,
    simulando o fluxo real de uso do sistema.
    """

    def test_fluxo_login_e_acesso_protegido(self, client):
        """
        Fluxo: Login → obter token → acessar rota protegida.
        """
        # 1. Login
        login_resp = client.post("/api/auth/login", json={
            "username": "teste@email.com",
            "password": "123456"
        })
        assert login_resp.status_code == 200
        token = login_resp.get_json()["token"]

        # 2. Acessa rota protegida com o token
        vip_resp = client.get("/api/auth/estoque-vip", headers={
            "Authorization": f"Bearer {token}"
        })
        assert vip_resp.status_code == 200
        assert "teste@email.com" in vip_resp.get_json()["mensagem"]

    def test_fluxo_listar_e_gerar_barcode(self, client, auth_headers):
        """
        Fluxo: Listar produtos → pegar ID do primeiro → gerar código de barras.
        """
        # 1. Lista todos os produtos
        list_resp = client.get("/products/", headers=auth_headers)
        assert list_resp.status_code == 200
        produtos = list_resp.get_json()["data"]
        assert len(produtos) > 0

        # 2. Pega o ID do primeiro produto
        primeiro_id = produtos[0]["cd_produto"]

        # 3. Gera o código de barras para esse produto
        barcode_resp = client.get(f"/products/{primeiro_id}/barcode", headers=auth_headers)
        assert barcode_resp.status_code == 200
        assert barcode_resp.content_type == "image/png"

    def test_fluxo_gerar_barcode_e_ler_de_volta(self, client, auth_headers):
        """
        Fluxo: Gerar imagem do barcode → fazer upload → verificar código lido.
        """
        # 1. Gera imagem do barcode do produto 2
        gen_resp = client.get("/products/2/barcode", headers=auth_headers)
        assert gen_resp.status_code == 200

        # 2. Upload da imagem para leitura
        data = {
            "barcode_image": (io.BytesIO(gen_resp.data), "test_roundtrip.png")
        }
        read_resp = client.post(
            "/barcodeup/upload",
            data=data,
            content_type="multipart/form-data",
            headers=auth_headers
        )
        assert read_resp.status_code == 200
        codigos = read_resp.get_json()["codigos"]

        # 3. Verifica se o código lido bate com o esperado
        assert "1000000002" in codigos  # id_to_barcode(2) = '1000000002'

    def test_fluxo_barcode_para_produto(self, client, auth_headers):
        """
        Fluxo: Dado um código de barras, encontrar o produto correspondente.
        """
        barcode_value = "1000000003"  # Produto ID 3 (Amoxicilina)

        resp = client.get(f"/products/barcode/{barcode_value}", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.get_json()["data"]
        assert len(data) > 0
        # Verifica se o nome do produto corresponde
        assert data[0]["ds_produto"] == "Amoxicilina 500mg"

    def test_fluxo_enviar_etiqueta_telegram(self, client, auth_headers):
        """
        Fluxo: Listar produtos → pegar ID → enviar etiqueta pelo Telegram.
        """
        # 1. Lista produtos
        list_resp = client.get("/products/", headers=auth_headers)
        produtos = list_resp.get_json()["data"]
        ultimo_id = produtos[-1]["cd_produto"]

        # 2. Envia etiqueta do último produto
        tag_resp = client.post(f"/telegram/send-product-tag/{ultimo_id}", headers=auth_headers)
        assert tag_resp.status_code == 200
        assert tag_resp.get_json()["success"] is True

    def test_fluxo_sem_login_bloqueado(self, client):
        """
        Fluxo: Tentar acessar todas as rotas protegidas sem token → tudo 401.
        """
        assert client.get("/products/").status_code == 401
        assert client.get("/products/barcode/1000000001").status_code == 401
        assert client.get("/products/1/barcode").status_code == 401
        assert client.post("/telegram/send", json={"message": "x"}).status_code == 401
        assert client.post("/telegram/send-product-tag/1").status_code == 401
        assert client.post("/barcodeup/upload").status_code == 401
