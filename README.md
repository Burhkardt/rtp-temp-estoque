# Sistema de Leitura e Envio WhatsApp - Softex

Este projeto implementa uma arquitetura modular com Frontend e Backend separados, utilizando Docker para orquestração.

## Arquitetura

- **Frontend**: React + Vite + TypeScript (Porta 3000)
- **Backend**: Python + FastAPI (Porta 8000)
- **Banco de Dados**: 2 instâncias PostgreSQL (Local para Auth, Remoto para Consultas)

## Módulos Implementados

1.  **Conexão com Banco**: 
    - `backend/database/local_db.py`: Conexão com o banco de autenticação (escrita/leitura).
    - `backend/database/remote_db.py`: Conexão com o banco de dados de produção (apenas consulta).
2.  **QR Code**:
    - `backend/modules/qrcode/generator.py`: Geração de QR Code a partir de dados do banco remoto.
    - `backend/modules/qrcode/reader.py`: Leitura de imagens de QR Code via Upload.
3.  **Mensageria**:
    - `backend/modules/messaging/whatsapp.py`: Interface para envio de mensagens via WhatsApp (Mock/Twilio).

## Como Executar

Certifique-se de ter o Docker e Docker Compose instalados.

1. Clone o repositório.
2. Na raiz do projeto, execute:
   ```bash
   docker-compose up --build
   ```
3. Acesse o Frontend em: `http://localhost:3000`
4. Acesse a documentação da API em: `http://localhost:8000/docs`

## Design Premium
O frontend foi desenvolvido com foco em estética moderna (Glassmorphism, Dark Mode, Typography Outfit).
