FROM python:3.10

WORKDIR /code

COPY ./universal/server/requirements.txt /code/requirements.txt
COPY ./universal/server/rbac_model.conf /code/rbac_model.conf
COPY ./universal/server/save_db.py /code/save_db.py
COPY ./universal/server/settings.default.toml /code/settings.default.toml
COPY ./universal/server/app /code/app

ADD ./universal/server/sources.list /etc/apt/sources.list

RUN apt-get clean
RUN apt-get update
RUN apt-get install -y libsasl2-dev python3-dev libldap2-dev libssl-dev
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com



CMD gunicorn app.app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80