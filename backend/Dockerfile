FROM python:3.10-bullseye

WORKDIR /code

COPY ./universal/back-end-py-mongo /code/

RUN set -x \
  && ls /etc/apt \
  && sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list \
  && apt update --fix-missing \
  && apt upgrade -y \
  && apt --reinstall install -y bash \
  libsasl2-dev  \
  python3-dev  \
  libldap2-dev  \
  libssl-dev \
  fastjar \
  gdb \
  && apt clean \
  && apt update -y \
  && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
  && echo "Asia/Shanghai" > /etc/timezone \
  && echo source /code/.gdbinit-gef.py >> ~/.gdbinit \
  && pip install --upgrade pip \
  && pip install --no-cache-dir -r /code/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple \
  && opentelemetry-bootstrap -a install