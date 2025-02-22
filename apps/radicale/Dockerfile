FROM ghcr.io/onedr0p/alpine:rolling@sha256:974f5883eb9b838792f1b27b812d8b9f80375ba9ac1f8b038fda27a53f6cd763

ARG VERSION
ARG TARGETPLATFORM
ARG TARGETARCH
ARG TARGETOS

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_ROOT_USER_ACTION=ignore \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    CRYPTOGRAPHY_DONT_BUILD_RUST=1

ENV \
    RADICALE_CONFIG_FILE=/config/config

LABEL dev.rafaribe.image.target_platform=$TARGETPLATFORM
LABEL dev.rafaribe.image.target_architecture=$TARGETARCH
LABEL dev.rafaribe.image.target_os=$TARGETOS
LABEL org.opencontainers.image.source="https://github.com/Kozea/Radicale"

COPY ./config /app/config.default

#hadolint ignore=DL3018,DL3013
RUN \
    apk add --no-cache --virtual=build-dependencies \
        gcc \
        musl-dev \
        libffi-dev \
        python3-dev \
    && apk add --no-cache \
        ca-certificates \
        python3 \
        py3-pip \
        py3-tz \
        tzdata \
    && python3 -m pip install --upgrade pip \
    && python3 -m pip install radicale==$VERSION passlib[bcrypt] \
    && chown -R 1000:1000 /app \
    && chmod -R 755 /app \
    && mkdir -p /data \
    && chown -R rafaribe:rafaribe /data \
    && chmod -R 775 /data \
    && apk del --purge build-dependencies \
    && rm -rf \
        /root/.cache \
        /root/.cargo \
        /tmp/*

USER rafaribe
COPY ./entrypoint.sh /entrypoint.sh
CMD ["/entrypoint.sh"]
