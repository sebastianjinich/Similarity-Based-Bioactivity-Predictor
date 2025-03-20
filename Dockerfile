FROM python:3.12-slim

# Crear usuario y directorio de trabajo
WORKDIR /root/similarity_activity_predictor

RUN apt-get update && apt-get install -y git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/OlivierBeq/jcompoundmapper_pywrapper.git

COPY . .

RUN pip install -r bin/requirements.txt

ENTRYPOINT ["python3","bin/main.py"]