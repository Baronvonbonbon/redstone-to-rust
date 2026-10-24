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
#   ./scripts/give-lab.sh LEARNER rust     # Lesson 9.1: setup-rust.sh, the crate kit and check-hack (no answers)
#   ./scripts/give-lab.sh LEARNER os       # Stage 10: setup-os.sh and the kernel kit (no answers)
#   ./scripts/give-lab.sh LEARNER net      # Stage 11: the secret messages and the dice word list (answers in labs/net/README.md)
#   ./scripts/give-lab.sh LEARNER lang     # Stage 12: check-pickaxe and its tests (the finished interpreter stays in labs/lang)
#   ./scripts/give-lab.sh LEARNER pico     # Stage 13: the Pico kit, reference programs, emulator and setup-pico.sh
set -euo pipefail
cd "$(dirname "$0")/.."

name=${1:?usage: $0 LEARNER cave|heist|sprites|redstone|sql|n2t|algo|stack|rust|os|net|lang|pico}
lab=${2:?usage: $0 LEARNER cave|heist|sprites|redstone|sql|n2t|algo|stack|rust|os|net|lang|pico}
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
  rust)  dest="$home/lab/rust"; script= ;;
  os)    dest="$home/lab/os"; script= ;;
  net)   dest="$home/lab/net"; script= ;;
  lang)  dest="$home/lab/lang"; script= ;;
  pico)  dest="$home/lab/pico"; script= ;;
  *)     echo "Unknown lab '$lab' (try cave, heist, sprites, redstone, sql, n2t, algo, stack, rust, os, net, lang or pico)"; exit 1 ;;
esac

if [[ "$lab" == rust ]]; then
  # ~/lab/rust holds the learner's own Rust projects too, so never replace the
  # whole folder: only refresh this lab's three things.
  sudo mkdir -p "$dest"
  sudo rm -rf "$dest/crate-kit"
  sudo cp -r labs/rust/crate-kit "$dest/crate-kit"
  sudo cp labs/rust/setup-rust.sh labs/rust/check-hack "$dest/"
  sudo chmod +x "$dest/setup-rust.sh" "$dest/check-hack"
  sudo chown -R "$name:" "$dest/crate-kit" "$dest/setup-rust.sh" "$dest/check-hack"
  for d in "$home/lab" "$dest"; do sudo chown "$name:" "$d"; done
  echo "Done. Next, as $name and online: bash ~/lab/rust/setup-rust.sh"
  exit 0
fi

if [[ "$lab" == os ]]; then
  # ~/lab/os holds the learner's own Stage 10 projects (and the Arch VM),
  # so never replace the whole folder: only refresh the kit and the script.
  sudo mkdir -p "$dest"
  sudo rm -rf "$dest/kernel-kit"
  sudo cp -r labs/os/kernel-kit "$dest/kernel-kit"
  sudo cp labs/os/setup-os.sh "$dest/"
  sudo chmod +x "$dest/setup-os.sh"
  sudo chown -R "$name:" "$dest/kernel-kit" "$dest/setup-os.sh"
  for d in "$home/lab" "$dest"; do sudo chown "$name:" "$d"; done
  echo "Done. Next, as $name and online (after setup-rust.sh): bash ~/lab/os/setup-os.sh"
  exit 0
fi

if [[ "$lab" == net ]]; then
  # ~/lab/net holds the learner's own Stage 11 projects, so never replace the
  # whole folder: only refresh the secret messages and the word list.
  sudo mkdir -p "$dest"
  sudo rm -rf "$dest/secrets"
  sudo cp -r labs/net/secrets "$dest/secrets"
  sudo cp labs/net/words.txt "$dest/"
  sudo chown -R "$name:" "$dest/secrets" "$dest/words.txt"
  for d in "$home/lab" "$dest"; do sudo chown "$name:" "$d"; done
  echo "Done. The answers to the secret messages are in labs/net/README.md (for you only)."
  exit 0
fi

if [[ "$lab" == lang ]]; then
  # ~/lab/lang holds the learner's own Stage 12 projects, so never replace the
  # whole folder: only refresh the checker and its tests.
  sudo mkdir -p "$dest"
  sudo rm -rf "$dest/tests"
  sudo cp -r labs/lang/tests "$dest/tests"
  sudo cp labs/lang/check-pickaxe "$dest/"
  sudo chmod +x "$dest/check-pickaxe"
  sudo chown -R "$name:" "$dest/tests" "$dest/check-pickaxe"
  for d in "$home/lab" "$dest"; do sudo chown "$name:" "$d"; done
  echo "Done. The learner runs ~/lab/lang/check-pickaxe 12.5 (and so on) from Lesson 12.5."
  exit 0
fi

if [[ "$lab" == pico ]]; then
  # ~/lab/pico holds the learner's own Pico programs (and the emulator's
  # node_modules), so never replace the whole folder: only refresh the kit,
  # the reference programs, the emulator script and the setup script.
  sudo mkdir -p "$dest/sim"
  sudo rm -rf "$dest/kit" "$dest/reference"
  sudo cp -r labs/pico/kit "$dest/kit"
  sudo cp -r labs/pico/reference "$dest/reference"
  sudo cp labs/pico/sim/package.json labs/pico/sim/pico-sim.mjs "$dest/sim/"
  sudo cp labs/pico/setup-pico.sh "$dest/"
  sudo chmod +x "$dest/setup-pico.sh"
  sudo chown -R "$name:" "$dest/kit" "$dest/reference" "$dest/sim" "$dest/setup-pico.sh"
  for d in "$home/lab" "$dest"; do sudo chown "$name:" "$d"; done
  echo "Done. Next, as $name and online (after setup-rust.sh): bash ~/lab/pico/setup-pico.sh"
  exit 0
fi

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
