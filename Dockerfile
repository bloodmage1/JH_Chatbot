FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu18.04

RUN apt-get update && apt-get install -y \
    python3.8 \
    python3.8-venv \
    python3.8-distutils \
    python3-pip \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1

WORKDIR /app

RUN python3 -m venv chatbot_jh && \
    . chatbot_jh/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["/bin/bash"]