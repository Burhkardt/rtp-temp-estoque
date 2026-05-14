from fastapi import FastAPI
from routers import auth, messaging, barcode
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Sistema de Leitura e Envio WhatsApp",
    description="API com Fastapi conectando com bancos locais e remotos, gerando/lendo Código de Barras e enviando WhatsApp.",
    version="1.0.0"
)

# Configuração de CORS para permitir que o Frontend se comunique com o Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Para produção, defina o domínio do seu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as Rotas (Módulos)
app.include_router(auth.router)
app.include_router(messaging.router)
app.include_router(barcode.router)

@app.get("/")
def root():
    return {"message": "API rodando com sucesso. Acesse /docs para a documentação interativa."}
