FROM python:3.12-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends iputils-ping \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY pingmot.py .

ENV PYTHONUNBUFFERED=1

CMD ["python", "-u", "pingmot.py"]
