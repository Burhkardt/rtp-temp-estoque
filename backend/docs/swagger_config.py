swagger_config = {
    "title": "API RTP Estoque",
    "uiversion": 3,
    "specs": [
        {
            "endpoint": "apispec_1",
            "route": "/apispec_1.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "specs_route": "/docs/"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "API RTP Estoque",
        "description": "Documentação interativa da API do sistema de leitura de código de barra para estoque.",
        "version": "1.0.0"
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "⚠️ **AVISO IMPORTANTE:**\nVocê **DEVE** digitar a palavra `Bearer` seguida de um espaço antes do seu token!\n\n**Exemplo correto:** `Bearer eyJhbGciOiJIUzI1NiIs...`"
        }
    },
}
