# ============================================
# Stage 1: Builder - Clone pyatlan from GitHub
# ============================================
FROM cgr.dev/atlan.com/pyatlan-golden:3.11 AS builder

# Build arguments
# PYATLAN_VERSION should be passed via --build-arg
# Default to "latest" if not specified (workflow reads from version.txt)
ARG PYATLAN_VERSION=latest
ARG PYATLAN_COMMIT_SHA=""

USER root
WORKDIR /tmp/build

# Install git and build tools
RUN apk add --no-cache git py3.11-build

# Clone pyatlan from GitHub
RUN echo "=== Cloning pyatlan from GitHub ===" && \
    git clone https://github.com/atlanhq/atlan-python.git /tmp/build/atlan-python

# Checkout specific version or commit
RUN cd /tmp/build/atlan-python && \
    if [ -n "$PYATLAN_COMMIT_SHA" ]; then \
        echo "Checking out commit: $PYATLAN_COMMIT_SHA" && \
        git checkout "$PYATLAN_COMMIT_SHA"; \
    elif [ "$PYATLAN_VERSION" = "latest" ]; then \
        echo "Using latest from main branch"; \
    else \
        echo "Checking out version: v$PYATLAN_VERSION" && \
        (git checkout "v$PYATLAN_VERSION" || git checkout "$PYATLAN_VERSION"); \
    fi && \
    echo "Commit: $(git rev-parse HEAD)" && \
    echo "Version: $(cat pyatlan/version.txt)" && \
    # Build wheel in builder stage (smaller than copying full source)
    python3 -m build --wheel --outdir /tmp/wheels . && \
    # Preserve version.txt before removing source
    cp pyatlan/version.txt /tmp/version.txt && \
    # Remove everything except the wheel and version.txt
    cd /tmp && \
    rm -rf /tmp/build/atlan-python && \
    echo "Built wheel: $(ls -lh /tmp/wheels/*.whl)" && \
    echo "Preserved version: $(cat /tmp/version.txt)"

# ============================================
# Stage 2: Final - Runtime image
# ============================================
FROM cgr.dev/atlan.com/pyatlan-golden:3.11

# Build arguments for labels
ARG PYTHON_VERSION=3.11
ARG PYATLAN_COMMIT_SHA=""

# Copy version.txt from builder and set PYATLAN_VERSION if not provided
COPY --from=builder /tmp/version.txt /tmp/version.txt
ARG PYATLAN_VERSION
RUN echo "=== Debug: Version setup ===" && \
    echo "Build arg PYATLAN_VERSION: '$PYATLAN_VERSION'" && \
    echo "Contents of version.txt: '$(cat /tmp/version.txt)'" && \
    if [ -z "$PYATLAN_VERSION" ]; then \
        PYATLAN_VERSION=$(cat /tmp/version.txt | tr -d '\n\r'); \
        echo "Using version from file: $PYATLAN_VERSION"; \
    else \
        echo "Using build arg version: $PYATLAN_VERSION"; \
    fi && \
    echo "Final PYATLAN_VERSION: $PYATLAN_VERSION" && \
    echo "$PYATLAN_VERSION" > /tmp/final_version.txt && \
    echo "Contents of final_version.txt: '$(cat /tmp/final_version.txt)'"

USER root
WORKDIR /app

# Set UV environment variables
ENV UV_NO_MANAGED_PYTHON=true \
    UV_SYSTEM_PYTHON=true

# Install pyatlan dependencies from Chainguard APK (hardened packages)
RUN apk add --no-cache \
    py3.11-pydantic=2.12.5-r0 \
    py3.11-jinja2=3.1.6-r1 \
    py3.11-tenacity=9.1.2-r2 \
    py3.11-pytz=2025.2-r2 \
    py3.11-python-dateutil=2.9.0-r10 \
    py3.11-pyyaml=6.0.3-r0 \
    py3.11-httpx=0.28.1-r2

# Copy only the wheel from builder (much smaller than full source)
COPY --from=builder /tmp/wheels/*.whl /tmp/

# Install dependencies + pyatlan wheel + cleanup in ONE layer
RUN uv pip install --system --no-cache \
        lazy-loader~=0.4 \
        nanoid~=2.0.0 \
        authlib~=1.6.0 \
        httpx-retries~=0.4.0 && \
    # Install pyatlan wheel with --no-deps
    uv pip install --system --no-cache --no-deps /tmp/*.whl && \
    # Cleanup everything EXCEPT version files (needed for verification)
    cd / && rm -rf /tmp/*.whl /root/.cache ~/.cache && \
    find /usr/lib/python3.11 -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true && \
    find /usr/lib/python3.11 -type f -name '*.pyc' -delete 2>/dev/null || true

# Verify installation and version
RUN echo "=== Debug: Checking version files ===" && \
    ls -la /tmp/ && \
    echo "Contents of final_version.txt:" && \
    cat /tmp/final_version.txt && \
    echo "=== Starting verification ===" && \
    EXPECTED_VERSION="$(cat /tmp/final_version.txt)" python3 <<'EOF'
import sys
import os

expected_version = os.environ.get("EXPECTED_VERSION", "unknown")
print("=== Pyatlan Installation Verification ===")
print(f"Expected version from env: {expected_version}")

try:
    import pyatlan
    print(f"✅ PyAtlan imported successfully")
    print(f"Installed version: {pyatlan.__version__}")
    
    # Try importing AtlanClient
    from pyatlan.client.atlan import AtlanClient
    print(f"✅ AtlanClient imported successfully")
    
    # Version validation (skip if 'latest' was requested)
    if expected_version != "latest" and expected_version != "unknown":
        if pyatlan.__version__ != expected_version:
            print(f"❌ ERROR: Version mismatch!")
            print(f"   Expected: {expected_version}")
            print(f"   Got: {pyatlan.__version__}")
            sys.exit(1)
        else:
            print("✅ Version verified")
    else:
        print("✅ Version validation skipped (latest or unknown)")
        
    print("=== Build verification passed ===")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)
EOF

# Final cleanup of temporary version files
RUN rm -rf /tmp/version.txt /tmp/final_version.txt

# Add build metadata as labels
LABEL python.version="${PYTHON_VERSION}"
LABEL pyatlan.commit_sha="${PYATLAN_COMMIT_SHA}"
# Note: pyatlan.version label should be set by passing --build-arg PYATLAN_VERSION=$(cat pyatlan/version.txt) during build
LABEL build.method="git-multistage"
LABEL build.source="github"
LABEL security.approach="apk-first-no-pypi"

# Switch to nonroot user for runtime security
USER nonroot

# Default working directory
WORKDIR /app

# Default command
CMD ["python"]
