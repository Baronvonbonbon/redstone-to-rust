#!/bin/bash
# Put a fresh lab into the learner's home folder. The answers are printed
# here, for the guide, and never stored where the learner can read them.
#
#   ./scripts/give-lab.sh LEARNER cave    # Lesson 1.11: Treasure Cave
#   ./scripts/give-lab.sh LEARNER heist   # Lesson 1.13: The Great Underpants Heist
#   ./scripts/give-lab.sh LEARNER sprites # Lesson 3.13: Sprite Maker (a tool, no answers)
#   ./scripts/give-lab.sh LEARNER redstone # Lesson 4.7: a flat creative Luanti world with Mesecons
#   ./scripts/give-lab.sh LEARNER sql      # Lesson 5.14: the Minecraft database (a file, no answers)
#   ./scripts/give-lab.sh LEARNER n2t      # Lesson 6.1: Nand to Tetris projects + practice chips (no answers)
#   ./scripts/give-lab.sh LEARNER algo     # Lesson 7.1: the Stage 7 checker and mazes (answers stay in labs/algo/answers)
#   ./scripts/give-lab.sh LEARNER stack    # Lesson 8.6: Stage 8 check scripts, compiler tests, Diamond Dash (no answers)
set -euo pipefail
cd "$(dirname "$0")/.."

name=${1:?usage: $0 LEARNER cave|heist|sprites|redstone|sql|n2t|algo|stack}
lab=${2:?usage: $0 LEARNER cave|heist|sprites|redstone|sql|n2t|algo|stack}
home=$(getent passwd "$name" | cut -d: -f6)
[[ -n "$home" ]] || { echo "No account called $name"; exit 1; }

case "$lab" in
  cave)  dest="$home/cave";  script=labs/treasure-cave/make_cave.py ;;
  heist) dest="$home/heist"; script=labs/underpants-heist/make_heist.py ;;
  sprites) dest="$home/lab/sprite-maker"; script= ;;
  redstone) dest="$home/.minetest/worlds/redstone-lab"; script= ;;
  sql)   dest="$home/lab/sql"; script= ;;
  n2t)   dest="$home/lab/n2t"; script= ;;
  algo)  dest="$home/lab/algo"; script= ;;
  stack) dest="$home/lab/n2t/stack"; script= ;;
  *)     echo "Unknown lab '$lab' (try cave, heist, sprites, redstone, sql, n2t, algo or stack)"; exit 1 ;;
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
elif [[ "$lab" == sql ]]; then
  sudo mkdir -p "$dest"
  sudo cp labs/sql/minecraft.sql "$dest/"
elif [[ "$lab" == n2t ]]; then
  # The project files come from the Nand to Tetris download in the offline library.
  n2t=${N2T:-/srv/redstone-library/tools/nand2tetris}
  [[ -d "$n2t/projects" ]] || { echo "No $n2t/projects. Run ./scripts/mirror-library.sh first."; exit 1; }
  sudo mkdir -p "$dest"
  sudo cp -r "$n2t/projects" "$dest/projects"
  sudo cp -r labs/n2t/practice "$dest/practice"
elif [[ "$lab" == algo ]]; then
  sudo mkdir -p "$dest"
  sudo cp labs/algo/check.py "$dest/"
  sudo cp -r labs/algo/mazes "$dest/mazes"
elif [[ "$lab" == stack ]]; then
  sudo mkdir -p "$dest"
  sudo cp -r labs/n2t/stack/. "$dest/"
  sudo chmod +x "$dest"/check-*
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
# If this script made ~/lab (or ~/lab/n2t) on the way, give those to the learner too.
for d in "$home/lab" "$home/lab/n2t"; do
  if sudo test -d "$d"; then sudo chown "$name:" "$d"; fi
done
