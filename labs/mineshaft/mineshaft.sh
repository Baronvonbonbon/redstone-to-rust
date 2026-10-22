#!/bin/bash
# Guide's control script for the Mineshaft wargame.
# Run it from YOUR account (the one in the docker group), not the learner's.
set -euo pipefail
cd "$(dirname "$0")"
NAME=mineshaft
PORT=2220

case "${1:-help}" in
  build)   docker build -t "$NAME" . ;;
  start)   docker run -d --name "$NAME" --hostname mineshaft --restart unless-stopped \
             -p "127.0.0.1:$PORT:22" "$NAME" >/dev/null
           echo "Mineshaft is open. Learner logs in with:  ssh miner0@localhost -p $PORT   (password: miner0)" ;;
  stop)    docker rm -f "$NAME" >/dev/null && echo "Mineshaft closed." ;;
  reset)   "$0" stop || true; "$0" build; "$0" start
           echo "New passwords were made. Old ones no longer work." ;;
  answers) docker exec "$NAME" cat /root/answers.txt ;;
  status)  docker ps --filter "name=^$NAME$" --format '{{.Names}}: {{.Status}}' ;;
  *)       echo "usage: $0 build | start | stop | reset | answers | status" ;;
esac
