FROM python:3.11-slim-bookworm

# Instala dependências do sistema para o Oracle Client e Pillow
RUN apt-get update && apt-get install -y \
    libaio1 \
    libpng-dev \
    libjpeg-dev \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app

# Instala as dependências do Python
# Copiamos o requirements da pasta local para a raiz do WORKDIR no container
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o conteúdo da pasta backend local para /app/backend no container
COPY . ./backend

EXPOSE 5000

# Define o PYTHONPATH para que o Python encontre os módulos na pasta backend
ENV PYTHONPATH=/app/backend

# Roda o main.py de dentro da pasta backend
CMD ["python", "backend/main.py"]
