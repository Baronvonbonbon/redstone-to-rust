#!/bin/bash
# Install the software the course uses, while you're online.
# Tested on Pop!_OS / Ubuntu 24.04. Run from the guide's (admin) account:
#
#   ./scripts/install-packages.sh            # Stages 0-5
#   ./scripts/install-packages.sh --later    # also Stages 6-13 tools
set -euo pipefail

EARLY=(
  # Stage 0: typing, mouse, educational games, drawing
  gcompris-qt tuxtype klavaro gtypist tuxpaint
  # Stage 1: terminal toys and basics
  cowsay sl figlet toilet lolcat tree nano less file
  bsdgames moon-buggy ninvaders
  # Stage 2-3: Python
  python3 python3-tk idle3 thonny python3-pygame python3-pgzero python3-doc
  # Stage 4: hex dumps, logic circuits (Digital needs Java), Luanti + Mesecons
  xxd default-jre minetest minetest-mod-mesecons
  # Stage 5: tools, labs, breakable lab VMs
  git vim sqlite3 unzip openssh-client netcat-openbsd docker.io gnome-boxes
)

LATER=(
  # Stage 8: C
  build-essential gdb valgrind manpages-dev
  # Stage 10: OS
  strace ltrace qemu-system-x86 qemu-utils
  # Stage 11: networking
  tcpdump wireshark dnsutils traceroute nmap
  # Stage 12: Scheme
  mit-scheme
)

pkgs=("${EARLY[@]}")
[[ "${1:-}" == "--later" ]] && pkgs+=("${LATER[@]}")

sudo apt-get update
sudo apt-get install -y "${pkgs[@]}"

# The guide (not the learner) runs the Docker labs.
if ! id -nG "$USER" | grep -qw docker; then
  sudo usermod -aG docker "$USER"
  echo "Added $USER to the docker group. Log out and back in for it to take effect."
fi

echo
echo "Done. Next: ./scripts/setup-learner.sh, then ./scripts/mirror-library.sh"
