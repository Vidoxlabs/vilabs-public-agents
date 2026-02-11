# Violet Development Container

FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    make \
    curl \
    postgresql-client \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

# Install Docker Compose
RUN curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose \
    && chmod +x /usr/local/bin/docker-compose

# Create non-root user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Set working directory
WORKDIR /workspace

# Switch to non-root user
USER $USERNAME

# Install Python development tools
RUN pip install --user black ruff mypy pytest pytest-cov

# Set PATH
ENV PATH="/home/${USERNAME}/.local/bin:${PATH}"
