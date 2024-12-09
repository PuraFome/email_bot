# Use a imagem base do Python
FROM python:3.9-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de requisitos e instala as dependências
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copia o restante do código para o contêiner
COPY . .

# Criar o diretório para o certificado SSL
RUN mkdir -p /root/.postgresql

# Copia o certificado SSL para o contêiner
RUN sh -c 'echo "$DB_SSL_CERT" > /root/.postgresql/root.crt'

# Verificar o conteúdo do diretório e do arquivo de certificado
RUN ls -l /root/.postgresql

RUN cat /root/.postgresql/root.crt

# Define a variável de ambiente para o Flask
ENV FLASK_APP=app.py

# Expõe a porta que o Flask usará
EXPOSE 8080

# Comando para iniciar a aplicação
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]