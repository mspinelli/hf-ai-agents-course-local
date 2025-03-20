# Extends the code at:
# https://huggingface.co/docs/smolagents/tutorials/secure_code_execution#setting-up-the-docker-sandbox
# to use Python 3.13 and the additional dependencies that needs (e.g. rust/cargo).
# Also installs the optional dependencies for Litellm, docker, and telemetry for smolagents

FROM python:3.13-bullseye

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        libclang-dev \
        python3-dev && \
    curl https://sh.rustup.rs -sSf | sh -s -- -y && \
    export PATH="$HOME/.cargo/bin:$PATH" && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir 'smolagents[litellm, docker, telemetry]' && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Run with limited privileges
USER nobody

# Default command
# CMD ["sh", "start.sh"]
CMD ["python", "-c", "print('Container ready')"]