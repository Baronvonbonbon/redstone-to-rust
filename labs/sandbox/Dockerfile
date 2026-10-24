# The Sandbox: a small Linux computer where the learner is the admin.
# Breaking it is allowed; `./sandbox.sh reset` puts it back as new.
# Build once while online; after that it needs no network at all.
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
ARG LEARNER=learner

# Put the manual pages back (the Docker image leaves them out), then the tools.
RUN apt-get update && apt-get install -y --no-install-recommends unminimize \
    && yes | unminimize >/dev/null \
    && apt-get install -y --no-install-recommends \
        openssh-server sudo man-db manpages nano vim less tree file htop \
        procps psmisc iproute2 netcat-openbsd git python3 sqlite3 bash-completion \
        iputils-ping iputils-tracepath dnsutils tcpdump curl ufw openssl \
    && ssh-keygen -A && mkdir -p /run/sshd

# Packages for Lesson 5.3 are downloaded but NOT installed, so that
# `sudo apt install cowsay` works later with no internet. The package lists
# are kept for the same reason, and apt is told to keep the files after
# installing, so `sudo apt install --reinstall cowsay` works offline too.
RUN rm -f /etc/apt/apt.conf.d/docker-clean \
    && echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/10keep-packages \
    && apt-get install -y --download-only --no-install-recommends cowsay figlet sl toilet

COPY sshd-sandbox.conf /etc/ssh/sshd_config.d/sandbox.conf
COPY motd /etc/motd
RUN (userdel -r ubuntu 2>/dev/null || true) \
    && useradd -m -s /bin/bash -G sudo "$LEARNER" \
    && echo "$LEARNER:$LEARNER" | chpasswd \
    && echo "$LEARNER" > /etc/sandbox-learner \
    && rm -f /etc/update-motd.d/*

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D", "-e"]
