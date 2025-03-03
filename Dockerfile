FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN groupadd --gid 1000 evebot \
    && useradd --uid 1000 --gid evebot --shell /bin/bash --create-home evebot

COPY --chown=evebot:evebot . /app

WORKDIR /app

RUN chown -R evebot:evebot /app

USER evebot

RUN uv sync --frozen \
    && mv /app/scripts/start.sh /app/start.sh \
    && rm -fr /app/scripts

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT [ "bash", "/app/start.sh" ]
CMD ["server"]
