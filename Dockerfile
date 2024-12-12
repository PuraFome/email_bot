# Use a imagem base do Python
FROM python:3.9-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de requisitos e instala as dependências
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copia o restante do código para o contêiner
COPY . .

# Define a variável de ambiente para o Flask
ENV FLASK_APP=app.py

# Expõe a porta que o Flask usará
EXPOSE 8080

# Comando para iniciar a aplicação
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]