#!/bin/bash
# Plays every level as its miner and checks each answer. Guide/maintainer tool.
# Usage: ./test_solutions.sh   (with the mineshaft container running)
set -u
declare -A pw
while read -r u p; do pw[$u]=$p; done < <(docker exec mineshaft cat /root/answers.txt)
as() { docker exec -u "miner$1" -w "/home/miner$1" -e HOME="/home/miner$1" mineshaft bash -c "$2" 2>&1; }
declare -a sol=(
  [0]='cat readme'
  [1]='cd tunnel && cat gem.txt'
  [2]='cat "diamond ore.txt"'
  [3]='cat .secret-chest'
  [4]='cat $(file chests/* | grep text | cut -d: -f1)'
  [5]='cat $(find cave -name diamond)'
  [6]='grep PASSWORD mining-log.txt'
  [7]='sort ores.txt | uniq -u'
  [8]='head -n 7777 long-tunnel.txt | tail -n 1'
  [9]='base64 -d creeper-code.txt'
  [10]="tr 'A-Za-z' 'N-ZA-Mn-za-m' < scrambled.txt"
  [11]='cd "$(mktemp -d)" && tar -xzf ~/buried.tar.gz && zcat treasure/map.txt.gz'
  [12]='cat $(find storage -size 1234c ! -executable)'
  [13]='./door --knock 3 --say please'
  [14]='bash -ic "echo \$MINESHAFT_SECRET" 2>/dev/null'
  [15]='diff old-map.txt new-map.txt | grep "^>"'
  [16]="echo ${pw[miner16]} | nc -q 2 localhost 30016"
  [17]='ps aux | grep gem-keeper | grep -v grep'
  [18]='cd journal && git log -p | grep "password is"'
  [19]='python3 -c "
import socket
f = socket.create_connection((\"localhost\", 30019)).makefile(\"rw\")
f.readline()
for _ in range(20):
    q = f.readline().split()
    f.write(str(int(q[2]) + int(q[4].rstrip(\"?\"))) + \"\n\"); f.flush(); f.readline()
print(f.readline())
"'
)
fail=0
for n in $(seq 0 19); do
  out=$(as "$n" "${sol[$n]}")
  want=${pw[miner$((n+1))]}
  if grep -q -- "$want" <<<"$out"; then echo "ok   level $n"; else echo "FAIL level $n: $out"; fail=1; fi
done
# Each miner must not be able to peek at the next level's home or password.
for n in 0 5 12; do
  if as "$n" "ls /home/miner$((n+1)) || cat /etc/mineshaft/pass/miner$((n+1))" | grep -q -- "${pw[miner$((n+1))]}"; then
    echo "FAIL miner$n can read miner$((n+1))'s secrets"; fail=1
  fi
done
as 0 "touch ~/x" | grep -q 'Permission denied' && echo "ok   homes are read-only" || { echo "FAIL home writable"; fail=1; }
exit $fail
