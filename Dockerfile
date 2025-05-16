FROM python:3.13.3-slim

# Set working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    gnupg2 \
    xz-utils \
    bzip2 \
    libgtk-3-0 \
    libdbus-glib-1-2 \
    libxtst6 \
    libx11-xcb-dev \
    libpci-dev \
    libatomic1 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Add Mozilla’s APT repo for latest Firefox
RUN mkdir -p /etc/apt/keyrings \
    && wget -q -O /etc/apt/keyrings/mozilla.asc https://packages.mozilla.org/apt/repo-signing-key.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/mozilla.asc] https://packages.mozilla.org/apt mozilla main" > /etc/apt/sources.list.d/mozilla.list \
    && echo "Package: *\nPin: release o=packages.mozilla.org\nPin-Priority: 1000" > /etc/apt/preferences.d/mozilla.pref

# Install Firefox
RUN apt-get update && apt-get install -y --no-install-recommends firefox \
    && rm -rf /var/lib/apt/lists/*

# Install latest ARM64 Geckodriver
ARG GECKODRIVER_VERSION=0.36.0
RUN wget -qO geckodriver.tar.gz \
    https://github.com/mozilla/geckodriver/releases/download/v${GECKODRIVER_VERSION}/geckodriver-v${GECKODRIVER_VERSION}-linux-aarch64.tar.gz \
    && tar -xzf geckodriver.tar.gz -C /usr/local/bin \
    && chmod +x /usr/local/bin/geckodriver \
    && rm geckodriver.tar.gz

# Install Ollama using the official install script
RUN curl -fsSL https://ollama.com/install.sh | sh \
    && if [ ! -x /usr/local/bin/ollama ]; then \
         echo "Error: Ollama installation failed"; exit 1; \
       fi \
    && mkdir -p /root/.ollama

# Verify installations (skip Ollama to avoid sandbox issues)
RUN firefox --version && geckodriver --version

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Set permissions
RUN chmod -R 755 /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PATH="/usr/local/bin:${PATH}"
ENV OLLAMA_HOST=http://0.0.0.0:11434

# Create non-root user
RUN useradd -ms /bin/bash selenium
USER selenium