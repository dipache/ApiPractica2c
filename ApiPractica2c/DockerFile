
FROM python:3.9
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["flask", "run", "--host=0.0.0.0"]
FROM python:3.12-slim as build

RUN apt-get update -y \
    && apt-get install -y build-essential libpq-dev git \
    && pip install virtualenv \
    && virtualenv /opt/cn_p2_simple_ws/venv \
    && . /opt/cn_p2_simple_ws/venv/bin/activate \
    && pip install gunicorn

COPY . /cn_p2_simple_ws

WORKDIR /cn_p2_simple_ws

RUN . /opt/cn_p2_simple_ws/venv/bin/activate \
    && pip install .

FROM python:3.12-slim

COPY --from=build /opt/cn_p2_simple_ws /opt/cn_p2_simple_ws
COPY entrypoint.sh /bin/entrypoint.sh

RUN apt-get update -y \
    && apt-get install -y libpq5\
    && apt-get clean \
    && groupadd -g 5000 -r wsuser \
    && useradd -r -M -u 5000 -g wsuser wsuser \
    && chown -R wsuser:wsuser /opt/cn_p2_simple_ws \
    && chmod +x /bin/entrypoint.sh
    

WORKDIR /opt/cn_p2_simple_ws
USER wsuser:wsuser

EXPOSE 8000

ENTRYPOINT ["entrypoint.sh"]


