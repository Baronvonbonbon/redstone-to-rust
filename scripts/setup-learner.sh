#!/bin/bash
# Create the learner's own account, with no admin (sudo) and no docker powers.
#
#   ./scripts/setup-learner.sh LEARNER_NAME
#
# You'll be asked to choose the learner's password. Pick it together.
set -euo pipefail

name=${1:?usage: $0 LEARNER_NAME   (lowercase, no spaces, e.g. sam)}

if id "$name" &>/dev/null; then
  echo "Account '$name' already exists."
else
  sudo adduser --gecos "" "$name"
fi

for g in sudo adm docker lxd; do
  if id -nG "$name" | grep -qw "$g"; then
    sudo gpasswd -d "$name" "$g"
    echo "Removed $name from the $g group (it gives admin-level power)."
  fi
done

sudo -u "$name" mkdir -p "/home/$name/lab"
echo
echo "Account '$name' is ready. Log out and log in as $name to check it works."
echo "Labs go in place with:  ./scripts/give-lab.sh $name cave|heist|sprites|redstone|sql|n2t|algo|stack|rust|os"
