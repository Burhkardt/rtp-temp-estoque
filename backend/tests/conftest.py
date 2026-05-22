"""
conftest.py – Configuração compartilhada para todos os testes E2E.

Cria o app Flask em modo de teste e fornece um client HTTP
que dispara requisições reais contra o backend (com banco Oracle dockerizado).
"""

import pytest
import sys
import os

# Garante que o diretório do backend está no path para imports funcionarem
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from main import create_app


@pytest.fixture(scope="session")
def app():
    """Cria a aplicação Flask uma única vez para toda a sessão de testes."""
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture(scope="session")
def client(app):
    """Fornece um test client HTTP do Flask reutilizável."""
    return app.test_client()


@pytest.fixture(scope="session")
def auth_token(client):
    """
    Realiza login com o usuário mock e retorna o token JWT.
    Esse token é reutilizado em todos os testes da sessão.
    """
    response = client.post("/api/auth/login", json={
        "username": "teste@email.com",
        "password": "123456"
    })
    assert response.status_code == 200, f"Login falhou: {response.get_json()}"
    data = response.get_json()
    return data["token"]


@pytest.fixture(scope="session")
def auth_headers(auth_token):
    """Retorna os headers com o Bearer token para rotas protegidas."""
    return {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json"
    }
