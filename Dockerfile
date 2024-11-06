FROM python:3.12


COPY --from=ghcr.io/astral-sh/uv:0.4.28 /uv /bin/uv

WORKDIR /workdir

COPY . .

RUN uv sync --extra examples
