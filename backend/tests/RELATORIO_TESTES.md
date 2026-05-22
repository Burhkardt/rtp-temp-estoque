# 🧪 Relatório de Testes E2E — Backend RTP Estoque

> **Tipo:** Testes End-to-End (E2E)  
> **Framework:** pytest  
> **Ambiente:** Docker (Oracle Free + Flask)  
> **Última execução:** 44 testes | ✅ 44 passed | ❌ 0 failed | ⚠️ 0 warnings | ⏱️ ~4.7s

---

## 📋 Índice

1. [Objetivo dos Testes](#1-objetivo-dos-testes)
2. [Como Executar](#2-como-executar)
3. [Estrutura dos Arquivos](#3-estrutura-dos-arquivos)
4. [Mapa de Cobertura](#4-mapa-de-cobertura)
5. [Detalhamento por Módulo](#5-detalhamento-por-módulo)
   - [5.1 Saúde da Aplicação](#51-saúde-da-aplicação)
   - [5.2 Autenticação (JWT)](#52-autenticação-jwt)
   - [5.3 Produtos](#53-produtos)
   - [5.4 Telegram](#54-telegram)
   - [5.5 Upload de Código de Barras](#55-upload-de-código-de-barras)
   - [5.6 Fluxos Completos (Integração)](#56-fluxos-completos-integração)
6. [Testes de Falha (Caminho Negativo)](#6-testes-de-falha-caminho-negativo)
7. [Proteção JWT das Rotas](#7-proteção-jwt-das-rotas)
8. [Melhorias Aplicadas](#8-melhorias-aplicadas)
9. [Dados de Teste](#9-dados-de-teste)

---

## 1. Objetivo dos Testes

Esses testes foram criados para **garantir a confiabilidade do sistema de ponta a ponta**, validando que todos os endpoints do backend funcionam corretamente — tanto nos cenários de sucesso (**caminho feliz**) quanto nos cenários de erro (**caminho negativo**).

A filosofia de QA aplicada aqui segue o princípio:

> **"Um teste que só verifica sucesso não prova nada. A confiança vem de testar o que DEVE quebrar e confirmar que o sistema reage corretamente."**

Por isso, para cada funcionalidade, nós testamos:
- ✅ O que **deve funcionar** (dados corretos, fluxo esperado)
- ❌ O que **deve falhar** (dados inválidos, ausentes, não autorizados)
- 🔒 O que **deve ser bloqueado** (acesso sem autenticação)
- 🔄 **Fluxos completos** que simulam o uso real do sistema

---

## 2. Como Executar

### Pré-requisitos
- Docker rodando com `docker compose up -d`
- Banco Oracle de teste inicializado e saudável
- pytest instalado no container (`docker exec rtp-backend pip install pytest`)

### Comando de execução

```bash
# Rodar todos os testes
docker exec -w /app rtp-backend python -m pytest tests/ -v

# Com relatório resumido
docker exec -w /app rtp-backend python -m pytest tests/ -v --tb=short

# Somente um módulo específico
docker exec -w /app rtp-backend python -m pytest tests/test_e2e_backend.py::TestAuth -v

# Somente testes de segurança (bloqueio sem token)
docker exec -w /app rtp-backend python -m pytest tests/ -v -k "sem_token"
```

---

## 3. Estrutura dos Arquivos

```
backend/tests/
├── __init__.py              # Marca a pasta como pacote Python
├── conftest.py              # Fixtures compartilhadas (app, client, token)
├── test_e2e_backend.py      # Todos os 44 testes E2E
└── RELATORIO_TESTES.md      # Este documento
```

### Fixtures (conftest.py)

| Fixture | Escopo | Descrição |
|---------|--------|-----------|
| `app` | sessão | Cria a aplicação Flask em modo TESTING |
| `client` | sessão | Fornece um client HTTP para disparar requisições |
| `auth_token` | sessão | Faz login e retorna o token JWT válido |
| `auth_headers` | sessão | Retorna headers com `Authorization: Bearer <token>` |

---

## 4. Mapa de Cobertura

| Módulo | Endpoint | Método | Testes ✅ | Testes ❌ | Testes 🔒 | Total |
|--------|----------|--------|-----------|-----------|-----------|-------|
| Saúde | `/`, `/apidocs/`, `/apispec_1.json` | GET | 3 | 0 | 0 | **3** |
| Auth | `/api/auth/login` | POST | 1 | 4 | 0 | **5** |
| Auth | `/api/auth/estoque-vip` | GET | 1 | 2 | 0 | **3** |
| Products | `/products/` | GET | 2 | 0 | 1 | **3** |
| Products | `/products/barcode/<code>` | GET | 2 | 2 | 1 | **5** |
| Products | `/products/<id>/barcode` | GET | 3 | 1 | 1 | **5** |
| Telegram | `/telegram/send` | POST | 2 | 2 | 1 | **5** |
| Telegram | `/telegram/send-product-tag/<id>` | POST | 2 | 1 | 1 | **4** |
| Upload | `/barcodeup/upload` | POST | 1 | 3 | 1 | **5** |
| Integração | Fluxos combinados | Vários | 5 | 0 | 1 | **6** |
| | | | **22** | **15** | **7** | **44** |

> **Proporção:** 50% sucesso / 34% falha / 16% segurança — cobertura robusta alinhada com boas práticas de QA.

### Legenda
- ✅ = Teste de caminho feliz (deve funcionar)
- ❌ = Teste de caminho negativo (deve falhar com erro controlado)
- 🔒 = Teste de segurança (deve bloquear acesso sem autenticação)

---

## 5. Detalhamento por Módulo

### 5.1 Saúde da Aplicação

Verifica se o servidor está respondendo e se a documentação Swagger está acessível.

| # | Teste | O que valida | Esperado |
|---|-------|-------------|----------|
| 1 | `test_root_redirect_to_apidocs` | `GET /` redireciona para Swagger | HTTP 302 + Location `/apidocs/` |
| 2 | `test_apidocs_accessible` | Swagger UI carrega | HTTP 200 |
| 3 | `test_apispec_json_accessible` | JSON da especificação existe e tem título correto | HTTP 200 + `title: "API RTP Estoque"` |

---

### 5.2 Autenticação (JWT)

Testa o ciclo completo de autenticação: login, geração de token e proteção de rotas.

| # | Teste | Cenário | Esperado |
|---|-------|---------|----------|
| 4 | `test_login_sucesso` | ✅ Credenciais corretas | HTTP 200 + token JWT |
| 5 | `test_login_sem_campos` | ❌ JSON vazio `{}` | HTTP 400 |
| 6 | `test_login_senha_errada` | ❌ Senha incorreta | HTTP 401 |
| 7 | `test_login_usuario_inexistente` | ❌ Email não cadastrado | HTTP 401 |
| 8 | `test_login_body_vazio` | ❌ Body completamente vazio | HTTP 400 |
| 9 | `test_rota_protegida_com_token` | ✅ Token válido no header | HTTP 200 + mensagem de boas-vindas |
| 10 | `test_rota_protegida_sem_token` | 🔒 Sem header Authorization | HTTP 401 |
| 11 | `test_rota_protegida_token_invalido` | ❌ Token JWT malformado | HTTP 422 |

> **Por que testar token inválido?** Um invasor pode tentar forjar tokens. O sistema DEVE rejeitar qualquer token que não foi assinado pela nossa chave secreta.

---

### 5.3 Produtos

Testa a listagem de produtos e a geração/consulta de códigos de barras. **Todas as rotas exigem autenticação JWT.**

| # | Teste | Cenário | Esperado |
|---|-------|---------|----------|
| 12 | `test_listar_todos_produtos` | ✅ Lista completa com token | HTTP 200 + `total >= 3` |
| 13 | `test_produtos_possuem_campos_corretos` | ✅ Estrutura do JSON | Campos `cd_produto` e `ds_produto` presentes |
| 14 | `test_listar_produtos_sem_token` | 🔒 Sem token | HTTP 401 |
| 15 | `test_buscar_produto_por_barcode_valido` | ✅ Barcode `1000000001` | HTTP 200 + produto encontrado |
| 16 | `test_buscar_produto_por_barcode_segundo_produto` | ✅ Barcode `1000000002` | HTTP 200 |
| 17 | `test_buscar_produto_barcode_inexistente` | ❌ Barcode `1999999999` | HTTP 404 |
| 18 | `test_buscar_produto_barcode_muito_curto` | ❌ Barcode `1` (1 dígito) | HTTP 400 |
| 19 | `test_buscar_produto_barcode_sem_token` | 🔒 Sem token | HTTP 401 |
| 20 | `test_gerar_imagem_barcode_produto_existente` | ✅ Produto ID 1 | HTTP 200 + `image/png` |
| 21 | `test_gerar_imagem_barcode_segundo_produto` | ✅ Produto ID 2 | HTTP 200 + `image/png` |
| 22 | `test_gerar_imagem_barcode_terceiro_produto` | ✅ Produto ID 3 | HTTP 200 + `image/png` |
| 23 | `test_gerar_imagem_barcode_produto_inexistente` | ❌ Produto ID 99999 | HTTP 404 |
| 24 | `test_gerar_barcode_sem_token` | 🔒 Sem token | HTTP 401 |

---

### 5.4 Telegram

Testa o envio de mensagens de texto e etiquetas com código de barras para o canal do Telegram. **Todas as rotas exigem autenticação JWT.**

| # | Teste | Cenário | Esperado |
|---|-------|---------|----------|
| 25 | `test_enviar_mensagem_texto` | ✅ Mensagem válida com token | HTTP 200 + `success: true` + `message_id` |
| 26 | `test_enviar_mensagem_sem_campo_message` | ❌ Campo errado (`texto` ao invés de `message`) | HTTP 400 |
| 27 | `test_enviar_mensagem_body_vazio` | ❌ Body vazio | HTTP 400 |
| 28 | `test_enviar_mensagem_sem_token` | 🔒 Sem token | HTTP 401 |
| 29 | `test_enviar_etiqueta_produto_existente` | ✅ Produto ID 1 com token | HTTP 200 + etiqueta enviada |
| 30 | `test_enviar_etiqueta_segundo_produto` | ✅ Produto ID 2 com token | HTTP 200 |
| 31 | `test_enviar_etiqueta_produto_inexistente` | ❌ Produto ID 99999 | HTTP 404 + `"Produto não encontrado"` |
| 32 | `test_enviar_etiqueta_sem_token` | 🔒 Sem token | HTTP 401 |
| 33 | `test_enviar_mensagem_com_html_parse_mode` | ✅ Parse mode HTML | HTTP 200 |

---

### 5.5 Upload de Código de Barras

Testa o endpoint que recebe uma imagem, lê o código de barras com OpenCV/pyzbar, e retorna os códigos encontrados. **A rota exige autenticação JWT.**

| # | Teste | Cenário | Esperado |
|---|-------|---------|----------|
| 34 | `test_upload_sem_arquivo` | ❌ Nenhum arquivo enviado | HTTP 400 |
| 35 | `test_upload_arquivo_nome_vazio` | ❌ Filename vazio | HTTP 400 |
| 36 | `test_upload_imagem_sem_barcode` | ❌ Imagem PNG 1x1 (sem barcode) | HTTP 422 + `status: "erro"` |
| 37 | `test_upload_sem_token` | 🔒 Sem token | HTTP 401 |
| 38 | `test_upload_imagem_barcode_gerado` | ✅ **Roundtrip**: gera barcode → upload → lê código | HTTP 200 + código `1000000001` |

> **Por que o teste 38 é tão importante?** Ele valida o ciclo completo do sistema: a geração do código de barras produz uma imagem que o leitor consegue interpretar corretamente. Se esse teste falhar, significa que ou a geração ou a leitura estão com problemas.

---

### 5.6 Fluxos Completos (Integração)

Esses testes simulam cenários reais de uso, combinando múltiplos endpoints em sequência — exatamente como um usuário real usaria o sistema.

| # | Teste | Fluxo | O que valida |
|---|-------|-------|-------------|
| 39 | `test_fluxo_login_e_acesso_protegido` | Login → Obter token → Acessar rota VIP | Autenticação ponta a ponta |
| 40 | `test_fluxo_listar_e_gerar_barcode` | Login → Listar produtos → Pegar ID → Gerar barcode | Integração banco + geração |
| 41 | `test_fluxo_gerar_barcode_e_ler_de_volta` | Gerar imagem → Upload → Verificar código lido | Roundtrip de geração/leitura |
| 42 | `test_fluxo_barcode_para_produto` | Dado barcode `1000000003` → Encontrar "Amoxicilina 500mg" | Mapeamento barcode ↔ produto |
| 43 | `test_fluxo_enviar_etiqueta_telegram` | Listar → Pegar último ID → Enviar etiqueta | Pipeline completo até o Telegram |
| 44 | `test_fluxo_sem_login_bloqueado` | 🔒 Tentar acessar TODAS as rotas sem token | Todas retornam 401 |

> **Teste 44** é um teste de segurança crítico: ele verifica de uma só vez que **nenhuma rota protegida** pode ser acessada sem autenticação.

---

## 6. Testes de Falha (Caminho Negativo)

A tabela abaixo lista **todos os 22 testes de falha e segurança** e explica por que cada um é importante:

### Testes de Validação (❌)

| Teste | O que tenta "quebrar" | Por que é importante |
|-------|----------------------|---------------------|
| Login sem campos | Requisição sem username/password | Previne crash por `NoneType` em campos obrigatórios |
| Login senha errada | Credencial inválida | Garante que o sistema não aceita qualquer senha |
| Login usuário inexistente | Email não cadastrado | Impede acesso indevido por força bruta |
| Login body vazio | Requisição com corpo vazio | Protege contra requisições malformadas |
| Token inválido | Token JWT forjado/adulterado | Impede acesso com tokens falsificados |
| Barcode inexistente | Código que não existe no banco | Garante retorno 404 limpo ao invés de exceção |
| Barcode muito curto | Código com menos de 2 caracteres | Previne erros de parsing no `barcode_to_id()` |
| Produto inexistente (imagem) | Gerar barcode para ID que não existe | Evita gerar imagens para produtos fantasma |
| Telegram sem campo message | JSON com campo errado | Valida que a API exige o campo correto |
| Telegram body vazio | Corpo da requisição vazio | Protege contra requisições acidentais/mal feitas |
| Etiqueta produto inexistente | Enviar etiqueta de produto que não existe | Previne envio de etiquetas em branco para o canal |
| Upload sem arquivo | POST sem multipart file | Garante mensagem de erro clara para o frontend |
| Upload nome vazio | Arquivo com filename vazio | Previne criação de arquivos com nomes inválidos |
| Upload imagem sem barcode | Imagem válida mas sem código | Valida que o sistema não "inventa" códigos inexistentes |

### Testes de Segurança (🔒)

| Teste | Rota bloqueada | Por que é importante |
|-------|---------------|---------------------|
| `test_rota_protegida_sem_token` | `/api/auth/estoque-vip` | Rotas administrativas devem exigir login |
| `test_listar_produtos_sem_token` | `/products/` | Dados de estoque não podem ser públicos |
| `test_buscar_produto_barcode_sem_token` | `/products/barcode/...` | Consulta de produtos exige autenticação |
| `test_gerar_barcode_sem_token` | `/products/<id>/barcode` | Geração de etiquetas não pode ser aberta |
| `test_enviar_mensagem_sem_token` | `/telegram/send` | Impede spam no canal do Telegram |
| `test_enviar_etiqueta_sem_token` | `/telegram/send-product-tag/<id>` | Impede envio não autorizado de etiquetas |
| `test_upload_sem_token` | `/barcodeup/upload` | Impede upload de arquivos sem autenticação |
| `test_fluxo_sem_login_bloqueado` | **Todas as rotas de uma vez** | Teste global de segurança |

---

## 7. Proteção JWT das Rotas

Todas as rotas da API estão protegidas com `@jwt_required()`, exceto as que precisam ser públicas:

| Rota | Método | Protegida? | Justificativa |
|------|--------|-----------|---------------|
| `/api/auth/login` | POST | ❌ Aberta | É a rota de login — precisa ser acessível sem token |
| `/` | GET | ❌ Aberta | Redirect para a documentação |
| `/apidocs/` | GET | ❌ Aberta | Documentação Swagger (consulta) |
| `/apispec_1.json` | GET | ❌ Aberta | Especificação da API |
| `/api/auth/estoque-vip` | GET | ✅ `@jwt_required()` | Rota de demonstração protegida |
| `/products/` | GET | ✅ `@jwt_required()` | Dados de estoque são sensíveis |
| `/products/barcode/<code>` | GET | ✅ `@jwt_required()` | Consulta de produtos |
| `/products/<id>/barcode` | GET | ✅ `@jwt_required()` | Geração de código de barras |
| `/telegram/send` | POST | ✅ `@jwt_required()` | Envio de mensagens ao canal |
| `/telegram/send-product-tag/<id>` | POST | ✅ `@jwt_required()` | Envio de etiquetas ao canal |
| `/barcodeup/upload` | POST | ✅ `@jwt_required()` | Upload e leitura de imagens |

---

## 8. Melhorias Aplicadas

Durante a criação dos testes, foram identificadas e corrigidas as seguintes melhorias:

### ✅ Correção 1: Chave JWT fortalecida

**Antes:** A `JWT_SECRET_KEY` usava o fallback `"fallback-inseguro"` (17 bytes), gerando warnings de segurança.

**Depois:** Gerada uma chave criptográfica de **32 bytes (64 caracteres hex)** via `secrets.token_hex(32)`, eliminando os warnings e tornando os tokens praticamente impossíveis de falsificar.

### ✅ Correção 2: Tratamento de body vazio no Telegram

**Antes:** `request.get_json()` lançava exceção com body vazio → retornava **500** (erro interno).

**Depois:** `request.get_json(silent=True)` retorna `None` silenciosamente → cai no `if not data` → retorna **400** (requisição inválida) com mensagem clara.

### ✅ Correção 3: Proteção JWT em todas as rotas

**Antes:** Apenas `/api/auth/estoque-vip` exigia autenticação. Todas as outras rotas (produtos, telegram, upload) eram abertas.

**Depois:** Todas as rotas sensíveis agora exigem `@jwt_required()`. Apenas login e documentação permanecem públicos.

---

## 9. Dados de Teste

Os testes dependem dos dados inseridos pelo script `teste_init.sql`:

| ID | Produto | Estoque | Barcode Esperado |
|----|---------|---------|-----------------|
| 1 | Dipirona 500g | 200 | `1000000001` |
| 2 | Paracetamol 750mg | 150 | `1000000002` |
| 3 | Amoxicilina 500mg | 80 | `1000000003` |

Se os dados do banco de teste forem alterados, alguns testes podem falhar. Nesse caso, ajuste os valores esperados no arquivo `test_e2e_backend.py`.

---

## Resultado Final

```
======================== 44 passed in 4.67s ========================
```

| Categoria | Quantidade |
|-----------|-----------|
| ✅ Testes de Sucesso | 22 |
| ❌ Testes de Falha | 15 |
| 🔒 Testes de Segurança | 7 |
| **Total** | **44** |
| **Taxa de aprovação** | **100%** |
| **Warnings** | **0** |
