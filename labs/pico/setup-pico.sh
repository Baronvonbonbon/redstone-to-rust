#!/bin/bash
# Stage 13 Pico setup. Run it ONCE, in the LEARNER's account, while online,
# after Stage 9's setup-rust.sh:
#   bash ~/lab/pico/setup-pico.sh
# It installs what the Pico lessons (13.5 to 13.7) need: Rust's target for
# the Pico's ARM Cortex-M0+ chip, and elf2uf2-rs, which turns a program into
# a .uf2 file and copies it to the Pico. Then it builds the kit once, so that
# its crates are downloaded and everything works offline afterwards.
# If Node.js is installed, it also sets up the Pico emulator in ~/lab/pico/sim.
set -euo pipefail

if [[ ! -x ~/.cargo/bin/rustup ]]; then
  echo "Rust isn't installed in this account yet: run ~/lab/rust/setup-rust.sh first (Stage 9)."
  exit 1
fi
source ~/.cargo/env
export CARGO_NET_OFFLINE=false   # setup-rust.sh switched Cargo to offline mode

echo "== The Pico's target: thumbv6m-none-eabi"
rustup target add thumbv6m-none-eabi

if ! command -v elf2uf2-rs >/dev/null; then
  echo "== Installing elf2uf2-rs (it needs the guide's install-packages.sh --later first)"
  cargo install elf2uf2-rs --version 2.2.0 --locked
fi

echo
echo "== Building the kit once, to download what it needs"
(cd ~/lab/pico/kit && cargo build --release)

if command -v npm >/dev/null; then
  echo
  echo "== The Pico emulator (optional)"
  cd ~/lab/pico/sim
  npm install --no-audit --no-fund
  # The RP2040's own start-up program (its "bootrom", from Raspberry Pi, BSD
  # licence), as packaged by the rp2040js project.
  curl -fsSL -o bootrom.mjs https://raw.githubusercontent.com/wokwi/rp2040js/v1.4.1/demo/bootrom.ts
else
  echo
  echo "(Node.js isn't installed, so the Pico emulator was skipped. That's fine with a real Pico.)"
fi

echo
echo "Done. Next, Lesson 13.5: cp -r ~/lab/pico/kit ~/lab/pico/blink"
