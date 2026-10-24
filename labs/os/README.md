# The OS Lab: the Guide's Handbook

Stage 10 (Operating Systems) happens in the learner's `~/lab/os` folder.
This lab gives them two things:

| File | What it does | Lessons |
|---|---|---|
| `setup-os.sh` | Installs a pinned nightly Rust compiler, `bootimage` and the `musl` target, in the learner's own account; then builds the kernel kit once | 10.12–10.14 (once, online) |
| `kernel-kit/` | The starting point for the learner's kernel: the target description, the Cargo settings, the `bootloader` crate, and a "Hello" kernel | 10.13, 10.14 |

This folder also has, for **you** to compare with if the learner's
version won't work:

- `shelly/`: the finished shell from Lessons 10.9 and 10.10;
- `redstone-os/`: the finished kernel from Lessons 10.13 and 10.14, with
  Creeper Chase.

Both are the course's own code (MIT), and the lessons show all of it,
so they aren't secrets; but `give-lab.sh` doesn't copy them, so that the
learner types and thinks first.

## Setting it up

1. Stage 9's setup must be done first (`~/lab/rust/setup-rust.sh`): it
   installs Rust in the learner's account.
2. From your own account, while online:
   ```
   ./scripts/install-packages.sh --later
   ./scripts/give-lab.sh LEARNER os
   sudo usermod -aG kvm LEARNER
   ```
   The first installs QEMU, `strace` and `bsdtar`. The second puts the
   kit and the script in the learner's `~/lab/os/`; it never deletes
   anything else there, so it's safe to run again. The third lets the
   learner's virtual machines use KVM (fast); they must log out and back
   in afterwards.
3. Log in as the learner (or open a terminal in their account), make
   sure the computer is **online**, and run:
   ```
   bash ~/lab/os/setup-os.sh
   ```
   It takes 5 to 10 minutes. It:
   - installs the **nightly** compiler named in `kernel-kit/
     rust-toolchain.toml`, with `rust-src`, `llvm-tools`, `rustfmt` and
     `clippy` (about 900 MB in `~/.rustup`);
   - adds the `x86_64-unknown-linux-musl` target, for Lesson 10.12's
     static programs;
   - installs `bootimage` 0.10.5, which turns a kernel into a disk image
     and runs it in QEMU;
   - runs `cargo bootimage` in the kit, which downloads the `bootloader`
     crate and the pieces of Rust's `core` library it needs, so that
     everything works offline afterwards.
4. Check, as the learner: `cd ~/lab/os/kernel-kit && cargo run`. A QEMU
   window should open with `Hello from Redstone OS!` at the top left.
   Close it.

Running `setup-os.sh` a second time is safe: it skips what's already
done.

## Things to know

- **Nightly, only for the kernel.** Kernels need a few experimental
  features, so the kit pins one nightly compiler (`nightly-2026-10-15`)
  with its `rust-toolchain.toml`. That file makes `cargo` use nightly
  *only inside* the kit and the learner's copy of it
  (`~/lab/os/redstone-os`). Everywhere else, Stage 9's stable compiler is
  used as before.
- **Offline.** Stage 9 set Cargo to offline mode, and the kit's crates
  are cached by `setup-os.sh`. The kernel lessons need nothing else. If
  you follow the challenge in Lesson 10.14 (*Writing an OS in Rust*,
  Chapters 5 to 7), it needs two more crates, fetched online in the
  learner's account:
  ```
  cd ~/lab/os/THE-COPY
  CARGO_NET_OFFLINE=false cargo add x86_64 pic8259
  CARGO_NET_OFFLINE=false cargo build
  ```
  The blog's chapters say which versions; read them first.
- **Warnings you can ignore.** The first build of a kernel prints
  `Compiling core` and `Compiling compiler_builtins`: Rust's own core
  library, built for the new target. `bootimage` prints `WARNING:
  CARGO_MANIFEST_DIR env variable not set` in some cases; it's harmless.
- **QEMU windows.** Click inside a QEMU window to type in it; **Ctrl+Alt+G**
  lets go of the keyboard and mouse. Closing the window stops the VM (for
  the Arch VM, prefer `poweroff` inside it, like a real computer). In
  Lesson 10.12, QEMU runs inside the terminal (`-nographic`); leave it with
  **Ctrl+A**, then **X**. If the terminal acts strangely afterwards,
  type `reset`.
- **KVM.** Without KVM (the `kvm` group, and virtualization switched on in
  the computer's firmware), leave `-enable-kvm` out of the QEMU commands:
  everything still works, but the Arch VM is very slow. The kernel
  lessons don't use KVM.
- **The kernel's speed.** Creeper Chase on Redstone OS times itself with
  the CPU's clock counter, assuming about 3 GHz (`TICK` in `main.rs`). On
  a much faster or slower computer the creeper is too fast or slow:
  change `TICK`, as Lesson 10.14 says.
- **The Arch VM** lives in `~/lab/os/arch`: the ISO (1.6 GB) and
  `arch.qcow2` (about 1.5 GB after Lesson 10.11, growing as it's used).
  `qemu-img snapshot -l ~/lab/os/arch/arch.qcow2` lists its save points.
  To start over completely, delete `arch.qcow2` and repeat Lesson 10.11
  from step 3.
- **Files to keep out of git:** the ISO, `arch.qcow2`, `disk.img`
  (Lesson 10.8), the `.cpio` files and `vmlinuz-linux` (Lesson 10.12).
  Each project's `target` folder is already ignored by `cargo new`.

## Licences

QEMU is GPL-2.0; `bootimage` and the `bootloader` crate are MIT/Apache-2.0;
Arch Linux is a collection of free software under many licences. The
kit's target description and configuration follow *Writing an OS in
Rust* by Philipp Oppermann (code MIT/Apache-2.0). This folder's scripts,
Shelly and Redstone OS are the course's own (MIT).
