# Mineshaft: an offline, Bandit-style terminal wargame.
# Build once while online; after that it runs with no network at all.

FROM ubuntu:24.04 AS door
RUN apt-get update && apt-get install -y --no-install-recommends gcc libc6-dev \
    && rm -rf /var/lib/apt/lists/*
COPY door.c /src/door.c
RUN gcc -O2 -o /src/door /src/door.c

FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
        openssh-server python3 git file nano vim-tiny less netcat-openbsd \
        procps diffutils gzip tar coreutils bsdextrautils \
    && rm -rf /var/lib/apt/lists/* \
    && ssh-keygen -A && mkdir -p /run/sshd \
    && git config --system --add safe.directory '*'

COPY sshd-mineshaft.conf /etc/ssh/sshd_config.d/mineshaft.conf
COPY --from=door /src/door /opt/mineshaft/door
COPY build_levels.py services.py entrypoint.sh /opt/mineshaft/
RUN python3 /opt/mineshaft/build_levels.py && chmod 755 /opt/mineshaft/entrypoint.sh

EXPOSE 22
CMD ["/opt/mineshaft/entrypoint.sh"]
