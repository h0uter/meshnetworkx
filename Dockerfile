FROM python:3.12


COPY --from=ghcr.io/astral-sh/uv:0.4.20 /uv /bin/uv

WORKDIR /workdir

COPY . .

RUN uv pip install --system .
