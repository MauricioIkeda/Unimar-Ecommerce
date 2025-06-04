
FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt

RUN mkdir /app
WORKDIR /app

COPY . .

COPY entrypoint.sh /tmp/entrypoint.sh
RUN sed -i 's/\r$//' /tmp/entrypoint.sh && \
    chmod +x /tmp/entrypoint.sh && \
    mv /tmp/entrypoint.sh /usr/local/bin/entrypoint.sh

RUN adduser -D appuser
USER appuser
EXPOSE 8000

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
