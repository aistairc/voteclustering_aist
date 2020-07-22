FROM debian:stable
# FROM ubuntu:18.04

RUN touch /etc/apt/apt.conf.d/99fixbadproxy && \
    echo "Acquire::http::Pipeline-Depth 0;" >> /etc/apt/apt.conf.d/99fixbadproxy && \
    echo "Acquire::http::No-Cache true;" >> /etc/apt/apt.conf.d/99fixbadproxy && \
    echo "Acquire::BrokenProxy    true;" >> /etc/apt/apt.conf.d/99fixbadproxy
RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/*
RUN apt-get clean
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -y --fix-missing \
    curl \
    gnupg
ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE = DontWarn
RUN apt-get install -y --fix-missing \
    python3.7 \
    python3-pip \
    default-libmysqlclient-dev \
    # libmysqlclient-dev \
    npm \
    graphviz \
    libgraphviz-dev \
    locales \
    locales-all \
    # language-pack-ja-base \
    # language-pack-ja \
    gettext
RUN apt remove cmdtest
RUN apt remove yarn
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
RUN apt-get update && apt-get install -y --fix-missing yarn
RUN yarn global add npm-run-all cpx
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

ENV PYTHONUNBUFFERED 1
RUN mkdir /src
WORKDIR /src
COPY requirements.txt /src/
RUN pip3 install -r requirements.txt
COPY . /src/
# RUN yarn
CMD ["/startup.sh"]
