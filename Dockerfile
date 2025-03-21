FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create user and group - this rarely changes
RUN groupadd --gid 1000 evebot \
    && useradd --uid 1000 --gid evebot --shell /bin/bash --create-home evebot

# Set working directory
WORKDIR /app

# permissions for app dir
RUN chown -R evebot:evebot /app

# Copy only dependency files first to leverage caching
COPY --chown=evebot:evebot pyproject.toml uv.lock ./

# Switch to non-root user for better security
USER evebot

# Install dependencies
RUN uv sync --frozen

# Copy the rest of the application after dependencies are installed
# This way changes to app code won't invalidate dependency cache
COPY --chown=evebot:evebot . .

# Set path to include the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Use exec form for ENTRYPOINT and CMD for better signal handling
ENTRYPOINT ["bash", "/app/start.sh"]
CMD ["server"]
