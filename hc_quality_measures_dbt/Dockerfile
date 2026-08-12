FROM python:3.13-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV DBT_PROFILES_DIR=/workspace/hc_quality_measures_dbt

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace/hc_quality_measures_dbt

COPY . .

RUN pip install --upgrade pip \
    && pip install dbt-duckdb pandas numpy

ENTRYPOINT ["bash"]
