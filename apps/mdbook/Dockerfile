ARG VERSION

FROM rust:1.99.0-slim@sha256:2752b332db73fdbb7dc576f06c82ed1f312005784ef913d7e04a28f5f55dc581 AS build

ENV CARGO_INSTALL_ROOT /usr/local/
ENV CARGO_TARGET_DIR /tmp/target/

ARG VERSION

RUN \
    apt-get -qq update \
    && \
    apt-get install -y \
        libssl-dev \
        pkg-config \
        ca-certificates \
        build-essential \
        make \
        perl \
        gcc \
        libc6-dev

RUN \
    cargo install --verbose \
        "mdbook@${VERSION}" \
        "mdbook-linkcheck" \
        "mdbook-admonish" \
        "mdbook-mermaid" \
        "mdbook-toc" \
        "mdbook-open-on-gh" \
        "mdbook-emojicodes" \
        "mdbook-regex"

FROM ghcr.io/onedr0p/ubuntu:rolling@sha256:5bf9f96c104ba37f7cbe95396ab20439ca9f4c9456aaf81abfa9bc65b80d63b9

ARG TARGETPLATFORM
ARG TARGETARCH
ARG TARGETOS

LABEL dev.rafaribe.image.target_platform=$TARGETPLATFORM
LABEL dev.rafaribe.image.target_architecture=$TARGETARCH
LABEL dev.rafaribe.image.target_os=$TARGETOS
LABEL org.opencontainers.image.source="https://github.com/rust-lang/mdBook"

ENV \
    RUST_LOG=info

COPY --from=build /usr/local/bin/mdbook* /bin/

# hadolint ignore=DL3008,DL3015,SC2086
RUN \
    apt-get -qq update \
    && \
    apt-get -qq install --no-install-recommends -y \
        ca-certificates \
    && \
    rm -rf \
        /tmp/* \
        /var/lib/apt/lists/* \
        /var/tmp/

# Used when serving
EXPOSE 3000

WORKDIR /data
VOLUME [ "/data" ]
