FROM ubuntu:latest

RUN apt-get update \
    && apt-get -y install \
    python3 \
    python3-pip \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists*

RUN pip3 install \
    flask \
    datetime \
    gunicorn \
    matplotlib \
    natsort \
    numpy \
    pandas \
    pillow \
    psycopg2-binary \
    requests \
    scikit-learn \
    scipy

# Create student user and allow access to /data directory
RUN useradd -ms /bin/bash student \
    && mkdir /data \
    && chown student /data

# Set default user
USER student

# Set default directory
WORKDIR /data
