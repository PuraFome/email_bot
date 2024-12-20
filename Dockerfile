# Use a imagem base do Python
FROM python:3.9-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de requisitos e instala as dependências
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copia o restante do código para o contêiner
COPY . .
ARG DB_SSL_CERT

# Criar o diretório para o certificado SSL
RUN mkdir -p /root/.postgresql

# Copiar o certificado SSL para o diretório
RUN echo "$DB_SSL_CERT" > /root/.postgresql/root.crt

# Define a variável de ambiente para o Flask
ENV FLASK_APP=app.py

# Expõe a porta que o Flask usará
EXPOSE 8080

# Comando para iniciar a aplicação
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]