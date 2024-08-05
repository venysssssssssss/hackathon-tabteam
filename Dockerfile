# Use a imagem base oficial do Python
FROM python:3.12.0

# Instale o Poetry
RUN pip install poetry

# Crie o diretório de trabalho e defina-o
WORKDIR /app

# Copie o pyproject.toml e o poetry.lock para o diretório de trabalho
COPY pyproject.toml poetry.lock /app/

# Instale as dependências do projeto usando o Poetry
RUN poetry config virtualenvs.create false && poetry install --no-root

# Copie o restante do código da aplicação para o diretório de trabalho
COPY . .

# Exponha a porta 8000 para acesso à aplicação FastAPI
EXPOSE 8000

# Defina o comando para rodar a aplicação
CMD ["poetry", "run", "uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
