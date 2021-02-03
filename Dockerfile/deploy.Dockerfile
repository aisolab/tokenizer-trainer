
FROM ubuntu:18.04
MAINTAINER boseop.kim@gmail.com

RUN apt-get update && \
      apt-get install -y sudo apt-utils make build-essential \
      libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
      libsqlite3-dev wget curl git libffi-dev liblzma-dev locales \
      g++ libpcre3-dev

RUN locale-gen en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8

ARG UID
RUN adduser --disabled-password --gecos "" user --uid ${UID:-1000}
RUN adduser user sudo
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER user
WORKDIR /home/user

# pyenv 설치/ 설정
ENV HOME /home/user
ENV PYENV_ROOT $HOME/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH
RUN git clone https://github.com/pyenv/pyenv.git .pyenv

# python 설치
RUN pyenv install 3.7.9 && \
    pyenv global 3.7.9 && \
    pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir cython && \
    pip install --no-cache-dir tokenizers kss==1.3.1 black isort

# WORKDIR 설정
WORKDIR /home/user/workspace

# pyenv 추가 설정
RUN echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
RUN echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
RUN echo 'eval "$(pyenv init -)"' >> ~/.bashrc