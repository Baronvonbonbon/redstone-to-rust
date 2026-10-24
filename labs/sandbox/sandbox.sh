#!/bin/bash
# Guide's control script for the Sandbox (Stage 5's breakable computer).
# Run it from YOUR account (the one in the docker group), not the learner's.
#
#   ./sandbox.sh build LEARNER   once, while online (a few minutes)
#   ./sandbox.sh start           learner logs in with: ssh LEARNER@localhost -p 2222
#   ./sandbox.sh stop            switch it off (everything inside is kept)
#   ./sandbox.sh reset           throw it away and start a brand-new one (seconds)
#   ./sandbox.sh status
set -euo pipefail
cd "$(dirname "$0")"
NAME=sandbox
PORT=2222

learner() { docker run --rm "$NAME" cat /etc/sandbox-learner; }

case "${1:-help}" in
  build)   who=${2:?usage: $0 build LEARNER}
           docker build --build-arg "LEARNER=$who" -t "$NAME" .
           echo "Built. If you rebuild later, the Sandbox gets a new identity, and the learner's"
           echo "ssh will warn about it once. They fix that with:  ssh-keygen -R '[localhost]:$PORT'" ;;
  start)   if docker container inspect "$NAME" >/dev/null 2>&1; then
             docker start "$NAME" >/dev/null
           else
             # NET_ADMIN lets the learner run a firewall inside it (Lesson 11.15).
             docker run -d --name "$NAME" --hostname sandbox --restart unless-stopped \
               --cap-add NET_ADMIN -p "127.0.0.1:$PORT:22" "$NAME" >/dev/null
           fi
           who=$(learner)
           echo "The Sandbox is on. Learner logs in with:  ssh $who@localhost -p $PORT"
           echo "(The first password is '$who', until the learner changes it in Lesson 5.1.)" ;;
  stop)    docker stop "$NAME" >/dev/null && echo "The Sandbox is off. Everything inside it is kept for next time." ;;
  reset)   docker rm -f "$NAME" >/dev/null 2>&1 || true
           "$0" start
           echo "It's brand new again. Everything changed inside it is gone, and the password is back to the first one." ;;
  status)  docker ps -a --filter "name=^$NAME$" --format '{{.Names}}: {{.Status}}' ;;
  *)       echo "usage: $0 build LEARNER | start | stop | reset | status" ;;
esac
