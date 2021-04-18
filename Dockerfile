FROM python:3.8

RUN useradd --create-home userapi
WORKDIR /Book-Library

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        build-essential \
        curl \
        git \
        libbz2-dev \
        libncurses5-dev \
        libncursesw5-dev \
        libreadline-dev \
        libsqlite3-dev \
        libssl-dev \
        llvm \
        make \
        tk-dev \
        wget \
        xz-utils \
        zlib1g-dev

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer \
    | bash
ENV PATH=$HOME/.pyenv/bin:$PATH
RUN git clone git://github.com/pyenv/pyenv.git /tmp/pyenv && \
    cd /tmp/pyenv/plugins/python-build && \
    ./install.sh && \
    rm -rf /tmp/pyenv

RUN python-build $PYTHON_VERSION /usr/local/

RUN if command pip >/dev/null 2>&1; then \
        echo "pip already installed. Skipping manual installation."; \
    else \
        echo "Installing pip manually"; \
        curl -o /tmp/get-pip.py https://bootstrap.pypa.io/get-pip.py && \
            chmod 755 /tmp/get-pip.py && \
            /tmp/get-pip.py && \
            rm /tmp/get-pip.py; \
    fi
RUN pip install pipenv
COPY ./ .
RUN /bin/bash -c "/usr/local/bin/python3.8 -m pip install --upgrade pip"
RUN /bin/bash -c "source venv/bin/activate"
RUN pip install -r requirements.txt
RUN chown -R userapi:userapi ./
USER userapi

EXPOSE 5000
CMD ["python", "./wsgi.py"]
