# base image
FROM python:3.11-slim

# set workdir
WORKDIR /app

# system deps (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# copy and install requirements
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# copy source code
COPY ./app/ /app/

# expose port
EXPOSE 8000

# default env
ENV PYTHONUNBUFFERED=1

# entrypoint: run uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
