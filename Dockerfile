FROM python:3.8

COPY requirements* /tmp/

RUN pip install --upgrade pip && pip install --no-cache-dir -r /tmp/requirements-test.txt


WORKDIR /opt/cms_forms/

COPY cms_forms cms_forms
COPY examples examples
COPY tests tests

ENV DJANGO_SETTINGS_MODULE=installation.settings_test
ENV PYTHONPATH "${PYTHONPATH}:/opt/cms_forms/examples"
