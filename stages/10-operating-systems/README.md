# Stage 10: Operating Systems

**Badge:** Kernel Hacker · **Needs first:** Stage 9; algebra (see
[MATH-TRACK.md](../../docs/MATH-TRACK.md)) · **Lessons:** 14

The learner looks inside the operating system they've been using since
Stage 1, and then builds one. The stage follows the plan of the free
textbook *Operating Systems: Three Easy Pieces* (OSTEP): the kernel
sharing the CPU and memory between processes (**virtualization**),
programs doing several things at once (**concurrency**), and files that
survive the power going off (**persistence**). Every idea is something
to see on the real computer, act out with toys, or build in Rust.

- **Looking inside Linux** (Lessons 10.1–10.5): processes, `/proc` and
  `top`; system calls, watched with `strace`; `fork`, `exec` and a real
  zombie process, in C; a scheduler simulator with averages to work out;
  and virtual memory, with page tables by hand and in Rust.
- **Concurrency** (10.6–10.7): threads that lose half their count in a
  race, two fixes, how Rust's borrowing rule stops races, and a deadlock
  at the miners' table.
- **Files** (10.8): inodes and links, and a disk made inside a file, with
  a "deleted" secret still in it.
- **Building things** (10.9–10.14): **Shelly**, a shell in Rust with
  pipes and redirection; **Arch Linux**, installed by hand in a virtual
  machine; a real Linux kernel booting with the learner's own program as
  PID 1 (then Shelly); and finally **Redstone OS**, the learner's own
  kernel in Rust, which draws, reads the keyboard, and runs Creeper
  Chase on bare metal.

Every program in the lessons was compiled and run, every error message
is a real one, and every terminal output is from a real run (with your
numbers, names and addresses being different). The kernels were booted
in QEMU and played by a test script; the Arch install was done with the
lesson's own commands.

## Tools

- **The Stage 10 packages:** QEMU, `strace` and `bsdtar`. From your own
  account, while online: `./scripts/install-packages.sh --later` (before
  Lesson 10.2).
- **The OS lab**, from your own account, after Stage 9's setup:
  `./scripts/give-lab.sh LEARNER os`; then, as the learner and online:
  `bash ~/lab/os/setup-os.sh` (before Lesson 10.12). The [OS lab
  handbook](../../labs/os/README.md) explains it.
- **KVM** for fast virtual machines: `sudo usermod -aG kvm LEARNER`, then
  the learner logs out and back in (before Lesson 10.11).
- Rust and Cargo from Stage 9, and `gcc` from Stage 8 (for Lessons 10.3
  and 10.5).
- **(Free, by hand)** *Operating Systems: Three Easy Pieces*, by Remzi
  and Andrea Arpaci-Dusseau: free chapter PDFs at
  `pages.cs.wisc.edu/~remzi/OSTEP/`. Download them into the offline
  library's `books` folder. Each lesson's "Guide's background" says
  which chapters it follows. They're written for university students,
  so they're for the guide, or for reading together.
- **(Free, in the offline library)** *Writing an OS in Rust*, by Philipp
  Oppermann (`repos/writing-an-os-in-rust/blog/content/edition-2/posts`),
  which Lessons 10.13 and 10.14 start from; and the **xv6** teaching
  kernel (`repos/xv6-riscv`), for an older learner.

## A note on the internet

Lesson 10.11 is the stage's one online lesson: it downloads Arch Linux
(about 1.6 GB) and installs it (about 500 MB more). `setup-os.sh` is
online too, once. Everything else is offline.

## Lessons

| # | Lesson | What happens | Key ideas |
|---|---|---|---|
| 10.1 | [The Boss of the Computer](01-the-boss.md) | The referee game; `ps`, `pstree`, `top`; `/proc`; a program that reads its own status | kernel, process, PID |
| 10.2 | [Asking the Kernel: System Calls](02-system-calls.md) | `strace` on `echo`, `ls` and Rust; file descriptors; the kernel saying no | system calls, user and kernel mode |
| 10.3 | [Making Processes: Fork, Exec and Zombies](03-processes.md) | `fork` and `exec` in C; a zombie; `kill`, Ctrl+C, Ctrl+Z | process API, signals |
| 10.4 | [Whose Turn Is It? Scheduling](04-scheduling.md) | FIFO, shortest job first and round robin, on paper and in a simulator | scheduling, averages |
| 10.5 | [Pretend Memory: Address Spaces and Pages](05-memory.md) | Addresses and ASLR; page tables by hand; a translator; segfaults; lazy memory | virtual memory, paging |
| 10.6 | [Threads, and the Lost Diamonds](06-threads-and-races.md) | Three miners; a race that loses half the count; atomics and a `Mutex` | threads, race conditions |
| 10.7 | [Stuck for Ever: Deadlock](07-deadlock.md) | Alex and Steve; the miners' table; lock ordering | deadlock |
| 10.8 | [Files, Inodes and a Disk in a File](08-files.md) | Hard and symbolic links; devices; `mkfs` and `debugfs`; deleting isn't wiping | inodes, file systems |
| 10.9 | [Build a Shell, Part 1: Shelly](09-shell-1.md) | A shell in Rust; errors; why `cd` must be built in | shells, `Command` |
| 10.10 | [Build a Shell, Part 2: Pipes and Arrows](10-shell-2.md) | `>` and `\|` in Shelly; `strace` shows `pipe2` and `dup2` | redirection, pipes |
| 10.11 | [Install Linux by Hand: Arch in a VM](11-arch-in-a-vm.md) | QEMU; partition, `mkfs`, `pacstrap`, chroot, GRUB; snapshots | virtual machines, installing |
| 10.12 | [You Are PID 1](12-pid-1.md) | The boot relay; a Linux kernel with your program, then Shelly, as PID 1 | booting, init, static linking |
| 10.13 | [A Kernel of Your Own, Part 1](13-kernel-1.md) | `no_std`; the VGA text buffer; a creeper scene; `write!`; a red screen of panic | bare metal |
| 10.14 | [A Kernel of Your Own, Part 2](14-kernel-2.md) | The keyboard's ports; random numbers; Creeper Chase on bare metal; Stage 10 checkpoint | ports, polling, timing |

## Setup notes

- The learner's Stage 10 projects all live in `~/lab/os`, one folder
  each (`cargo new` makes each a git repository), plus `~/lab/os/files`
  (Lesson 10.8), `~/lab/os/arch` (the VM, 10.11) and `~/lab/os/pid1`
  (10.12). The C programs of Lessons 10.3 and 10.5 go in `~/lab/c`, with
  Stage 8's.
- Run `give-lab.sh LEARNER os` before Lesson 10.1, so that `~/lab/os`
  exists. Running it again later is safe: it only replaces the kit and
  the setup script.
- Disk space: the Arch VM grows to about 1.5 GB, plus the 1.6 GB ISO; the
  nightly compiler adds about 900 MB to the learner's `~/.rustup`. Never
  commit the ISO, the VM disk, `disk.img` or the `.cpio` files.
- The kernel lessons use a **nightly** Rust compiler, pinned to one day
  by the kit's `rust-toolchain.toml`, only inside `~/lab/os/redstone-os`.
  Everything else stays on the normal (stable) compiler from Stage 9.

## Free play for this stage

- `htop` (if installed) or `top`, watching what the computer does while
  playing a game.
- More `strace`: what system calls does `cowsay` make? `python3`?
- More programs in the Arch VM (`pacman -Ss` to search), and breaking
  and mending it, with snapshots.
- New Shelly built-ins, and more programs in the tiny PID 1 Linux.
- Redstone OS: a title screen, levels, two creepers, a second game.
- For an older learner: the first chapters of OSTEP, its homework
  simulators (Python, in the OSTEP homework repository online), or the
  xv6 source in the offline library.

## Habits to build now

- **Ask the kernel.** `/proc`, `strace`, `ps` and `lsblk` say what's
  really happening.
- **Act it out first.** Pencils, tallies and toys before code, for
  every new idea.
- **Make bugs happen every time.** A `sleep` turns a rare race or
  deadlock into a reliable one you can study.
- **Save points.** Snapshot the VM before experiments.
- **`cargo fmt`, `cargo clippy`, commit** (as in Stage 9).

## Checkpoint

The learner can, without help:
- [ ] Explain the kernel's jobs, and system calls, with `strace` as
      evidence
- [ ] Explain `fork`, `exec` and `wait`, and what a shell does with them
- [ ] Work out scheduling averages, and translate an address with a page
      table
- [ ] Explain and fix a race condition and a deadlock
- [ ] Explain inodes and links, and why deleting isn't wiping
- [ ] Explain the boot relay, and what PID 1 is

They can also:
- [ ] Run pipelines in their own shell, Shelly
- [ ] Install Arch Linux in a VM, and boot their own program as PID 1
- [ ] Play Creeper Chase on their own kernel (Lesson 10.14)
