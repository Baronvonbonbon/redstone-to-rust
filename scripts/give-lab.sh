#!/bin/bash
# Put a fresh lab into the learner's home folder. The answers are printed
# here, for the guide, and never stored where the learner can read them.
#
#   ./scripts/give-lab.sh LEARNER cave    # Lesson 1.11: Treasure Cave
#   ./scripts/give-lab.sh LEARNER heist   # Lesson 1.13: The Great Underpants Heist
#   ./scripts/give-lab.sh LEARNER sprites # Lesson 3.13: Sprite Maker (a tool, no answers)
set -euo pipefail
cd "$(dirname "$0")/.."

name=${1:?usage: $0 LEARNER cave|heist|sprites}
lab=${2:?usage: $0 LEARNER cave|heist|sprites}
home=$(getent passwd "$name" | cut -d: -f6)
[[ -n "$home" ]] || { echo "No account called $name"; exit 1; }

case "$lab" in
  cave)  dest="$home/cave";  script=labs/treasure-cave/make_cave.py ;;
  heist) dest="$home/heist"; script=labs/underpants-heist/make_heist.py ;;
  sprites) dest="$home/lab/sprite-maker"; script= ;;
  *)     echo "Unknown lab '$lab' (try cave, heist or sprites)"; exit 1 ;;
esac

if sudo test -e "$dest"; then
  read -rp "$dest already exists. Replace it with a new one? [y/N] " ok
  [[ "$ok" == [yY]* ]] || exit 0
  sudo rm -rf "$dest"
fi
if [[ -n "$script" ]]; then
  sudo python3 "$script" "$dest"
else
  sudo mkdir -p "$dest"
  sudo cp labs/sprite-maker/make_sprite.py labs/sprite-maker/examples/*.txt "$dest/"
fi
sudo chown -R "$name:" "$dest"
