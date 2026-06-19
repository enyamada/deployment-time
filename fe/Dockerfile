FROM python:3.11-slim
LABEL maintainer="Edson Yamada <enyamada@gmail.com>"

# Zero APT-GET. Sem pacotes quebrando na nuvem.
RUN pip install --no-cache-dir \
    PyMySQL \
    Flask \
    pyyaml \
    retrying

EXPOSE 5000
WORKDIR /root
COPY config.yml config.yml
COPY *.py /root/

CMD ["python", "steps.py"]
