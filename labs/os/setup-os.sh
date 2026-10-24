#!/bin/bash
# Stage 10 setup. Run it ONCE, in the LEARNER's account, while online,
# after Stage 9's setup-rust.sh:
#   bash ~/lab/os/setup-os.sh
# It installs what the kernel lessons (10.13, 10.14) and the PID 1
# lesson (10.12) need: a pinned nightly Rust, bootimage, and the musl
# target. Then it builds the kernel kit once, so that its crates are
# downloaded and everything works offline afterwards.
set -euo pipefail

NIGHTLY=nightly-2026-10-15
if [[ ! -x ~/.cargo/bin/rustup ]]; then
  echo "Rust isn't installed in this account yet: run ~/lab/rust/setup-rust.sh first (Stage 9)."
  exit 1
fi
source ~/.cargo/env
export CARGO_NET_OFFLINE=false   # setup-rust.sh switched Cargo to offline mode

echo "== The nightly compiler, for the kernel ($NIGHTLY)"
rustup toolchain install "$NIGHTLY" --profile minimal \
  --component rust-src,llvm-tools-preview,rustfmt,clippy

echo "== The musl target, for programs with no libraries (Lesson 10.12)"
rustup target add x86_64-unknown-linux-musl

if ! command -v bootimage >/dev/null; then
  echo "== Installing bootimage, which makes a kernel into a disk image"
  cargo install bootimage --version 0.10.5 --locked
fi

echo
echo "== Building the kernel kit once, to download what it needs"
(cd ~/lab/os/kernel-kit && cargo bootimage)

echo
echo "Done. Next, try: cd ~/lab/os/kernel-kit && cargo run"
echo "(QEMU must be installed: the guide's ./scripts/install-packages.sh --later)"
