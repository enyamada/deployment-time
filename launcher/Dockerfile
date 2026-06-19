FROM python:3.11-slim
LABEL maintainer="Edson Yamada <enyamada@gmail.com>"

# O debian-slim não vem com curl/bash por padrão se os seus scripts .sh precisarem,
# mas o gcc e o pip já estão resolvidos nativamente pelo Python base.
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Instala o boto3 direto usando o pip nativo da imagem
RUN pip install --no-cache-dir boto3

WORKDIR /root

# Copia os arquivos necessários
COPY aws/ /root/.aws/
COPY *.py /root/
COPY *.sh /root/

# Garante permissão de execução nos scripts shell (boa prática para o container)
RUN chmod +x /root/*.sh
