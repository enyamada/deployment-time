FROM python:2.7-slim
LABEL maintainer="Edson Yamada <enyamada@gmail.com>"

# Instala as ferramentas de compilação e as bibliotecas de desenvolvimento do MySQL (MariaDB no Debian)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
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
