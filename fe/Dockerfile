FROM python:2.7-slim
LABEL maintainer="Edson Yamada <enyamada@gmail.com>"

# Configura o apt para tentar até 3 vezes em caso de falha de rede e roda o update de forma limpa
RUN apt-get clean && \
    apt-get update --fix-missing -o Acquire::Retries=3 && \
    apt-get install -y --no-install-recommends \
        gcc \
        default-libmysqlclient-dev \
        pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Instala as dependências do Python. O pip vai compilar o MySQL-python usando o gcc local
RUN pip install --no-cache-dir \
    MySQL-python \
    Flask \
    pyyaml \
    retrying

EXPOSE 5000

WORKDIR /root
COPY config.yml config.yml
COPY *.py /root/

CMD ["python", "steps.py"]
