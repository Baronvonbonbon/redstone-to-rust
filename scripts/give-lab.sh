#!/bin/bash
# Put a fresh lab into the learner's home folder. The answers are printed
# here, for the guide, and never stored where the learner can read them.
#
#   ./scripts/give-lab.sh LEARNER cave    # Lesson 1.11: Treasure Cave
#   ./scripts/give-lab.sh LEARNER heist   # Lesson 1.13: The Great Underpants Heist
#   ./scripts/give-lab.sh LEARNER sprites # Lesson 3.13: Sprite Maker (a tool, no answers)
#   ./scripts/give-lab.sh LEARNER redstone # Lesson 4.7: a flat creative Luanti world with Mesecons
set -euo pipefail
cd "$(dirname "$0")/.."

name=${1:?usage: $0 LEARNER cave|heist|sprites|redstone}
lab=${2:?usage: $0 LEARNER cave|heist|sprites|redstone}
home=$(getent passwd "$name" | cut -d: -f6)
[[ -n "$home" ]] || { echo "No account called $name"; exit 1; }

case "$lab" in
  cave)  dest="$home/cave";  script=labs/treasure-cave/make_cave.py ;;
  heist) dest="$home/heist"; script=labs/underpants-heist/make_heist.py ;;
  sprites) dest="$home/lab/sprite-maker"; script= ;;
  redstone) dest="$home/.minetest/worlds/redstone-lab"; script= ;;
  *)     echo "Unknown lab '$lab' (try cave, heist, sprites or redstone)"; exit 1 ;;
esac

if sudo test -e "$dest"; then
  read -rp "$dest already exists. Replace it with a new one? [y/N] " ok
  [[ "$ok" == [yY]* ]] || exit 0
  sudo rm -rf "$dest"
fi
if [[ -n "$script" ]]; then
  sudo python3 "$script" "$dest"
elif [[ "$lab" == sprites ]]; then
  sudo mkdir -p "$dest"
  sudo cp labs/sprite-maker/make_sprite.py labs/sprite-maker/examples/*.txt "$dest/"
else
  # A new world: flat, no trees or caves, creative, no damage, every Mesecons mod on.
  # Luanti builds the land the first time it's played.
  mods=/usr/share/games/minetest/mods/mesecons
  [[ -d "$mods" ]] || { echo "Mesecons isn't installed. Run ./scripts/install-packages.sh first."; exit 1; }
  sudo mkdir -p "$dest"
  {
    echo "gameid = minetest"
    echo "backend = sqlite3"
    echo "creative_mode = true"
    echo "enable_damage = false"
    for m in "$mods"/*/; do echo "load_mod_$(basename "$m") = true"; done
  } | sudo tee "$dest/world.mt" >/dev/null
  printf '%s\n' "mg_name = flat" \
    "mg_flags = nocaves, nodungeons, light, nodecorations, biomes, ores" \
    "mgflat_spflags = nolakes, nohills, nocaverns" "[end_of_params]" | sudo tee "$dest/map_meta.txt" >/dev/null
  dest="$home/.minetest"
fi
sudo chown -R "$name:" "$dest"
