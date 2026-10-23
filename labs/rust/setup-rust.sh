#!/bin/bash
# Stage 9 setup. Run it ONCE, in the LEARNER's account, while online:
#   bash ~/lab/rust/setup-rust.sh
# It installs Rust (no admin needed), the offline Rust books, Rustlings,
# and the crates for Stage 9. Then it switches Cargo to offline mode.
set -euo pipefail

if [[ ! -x ~/.cargo/bin/rustup ]]; then
  echo "== Installing Rust (rustup)"
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
fi
source ~/.cargo/env

echo "== The offline books and the standard library's source"
rustup component add rust-docs rust-src

if ! command -v rustlings >/dev/null; then
  echo "== Installing Rustlings"
  cargo install rustlings
fi
if [[ ! -d ~/lab/rust/rustlings ]]; then
  (cd ~/lab/rust && echo | rustlings init)   # echo answers its "Press ENTER"
fi

echo
echo "== Downloading the crate kit"
(cd ~/lab/rust/crate-kit && cargo fetch && cargo build -q)

echo "== Switching Cargo to offline mode"
mkdir -p ~/.cargo
if ! grep -q "offline" ~/.cargo/config.toml 2>/dev/null; then
  printf '[net]\noffline = true\n' >> ~/.cargo/config.toml
fi

echo
echo "Done. Open a NEW terminal, then try: cargo --version"
