# Setup

Do all of this **from the guide's account, while online.** Afterwards,
lessons through Stage 8 work with no internet. A few later steps (Rust
in Stage 9, VM images in Stages 5 and 10) need the internet once more,
at the start of those stages.

Written for **Pop!_OS 24.04** (and Ubuntu 24.04, which it's built on).

## 1. Get this course onto the computer

```bash
cd ~
git clone <this repository's URL> redstone-to-rust
cd redstone-to-rust
```

(If you received it as a zip, unzip it into your home folder instead.)

## 2. Install the software (about 10 minutes)

```bash
./scripts/install-packages.sh
```

This installs everything for Stages 0 to 7: typing tutors, GCompris,
terminal toys, Python with Thonny and Pygame Zero, Luanti with the
Mesecons circuits mod, git, Docker and GNOME Boxes. **Log out and back
in afterwards**, so your account can use Docker.

Run it again with `--later` when you reach Stage 8.

## 3. Make the learner's account

```bash
./scripts/setup-learner.sh sam      # use the learner's name, lowercase, no spaces
```

Choose the password *together*; it's the first thing they'll type in
Lesson 0.4. The script makes sure the account has **no admin (sudo)
and no Docker** powers, so the learner can explore freely without being
able to break the computer.

## 4. Download the offline library (about 1 GB)

```bash
sudo mkdir -p /srv/redstone-library && sudo chown "$USER" /srv/redstone-library
./scripts/mirror-library.sh
```

At the end it lists the things a script can't download; fetch those by
hand into `/srv/redstone-library/books/`. Every account can read the
library, including the learner's.

## 5. Build the Mineshaft wargame (needed for Lesson 1.14)

```bash
cd labs/mineshaft
./mineshaft.sh build     # about 2 minutes, needs internet this once
./mineshaft.sh start
./test_solutions.sh      # optional: checks every level works ("ok" on every line)
```

It keeps running in the background, and restarts by itself when the
computer reboots. The other commands you'll need:

| Command | What it does |
|---|---|
| `./mineshaft.sh answers` | Shows every level's password (for the guide only!) |
| `./mineshaft.sh reset` | Builds new random passwords, for a fresh start or a sibling |
| `./mineshaft.sh stop` | Turns it off |

## 6. Labs that go in the learner's home folder

The lessons tell you when to run these:

```bash
./scripts/give-lab.sh sam cave      # Lesson 1.11
./scripts/give-lab.sh sam heist     # Lesson 1.13
./scripts/give-lab.sh sam sprites   # Lesson 3.13 (a tool, so there's no answer)
./scripts/give-lab.sh sam redstone  # Lesson 4.7 (a Luanti world, so there's no answer)
./scripts/give-lab.sh sam sql       # Lesson 5.14 (a database file, so there's no answer)
./scripts/give-lab.sh sam n2t       # Lesson 6.1 (Nand to Tetris projects, so there's no answer)
./scripts/give-lab.sh sam algo      # Lesson 7.1 (a checker and mazes; your answers are in labs/algo/answers)
./scripts/give-lab.sh sam stack     # Lesson 8.6 (Stage 8 test scripts and an example game, so there's no answer)
./scripts/give-lab.sh sam rust      # Lesson 9.1 (Rust's setup script, crate kit and check-hack; no answer)
./scripts/give-lab.sh sam os        # Stage 10 (the OS setup script and the kernel kit; no answer)
./scripts/give-lab.sh sam net       # Lesson 11.9 (secret messages and a word list; answers in labs/net/README.md)
./scripts/give-lab.sh sam lang      # Lesson 12.5 (check-pickaxe and its tests; no answers needed)
./scripts/give-lab.sh sam pico      # Lesson 13.5 (the Pico kit, reference programs and emulator; no answers needed)
```

The cave and the heist print the answer for you. Don't let the learner see it!

## Later: a breakable computer (Stage 5)

In Stage 5 the learner gets a computer where they *are* the admin, and
where breaking things is fine. The lessons are written for the Sandbox;
a Pi or a VM works too.

**The Sandbox (the default).** A small Linux computer in Docker, like
the Mineshaft. From your own account, once, while online:

```bash
cd labs/sandbox
./sandbox.sh build sam    # the learner's account name; about 5 minutes
./sandbox.sh start
```

The learner logs in with `ssh sam@localhost -p 2222` (first password:
their name). `./sandbox.sh reset` makes a brand-new one in seconds. The
[Sandbox handbook](../labs/sandbox/README.md) has the rest.

**Option B: Raspberry Pi.** It's a real, separate machine, and it
feels like theirs. Use Raspberry Pi Imager (`flatpak install flathub
org.raspberrypi.rpi-imager`, or download it from raspberrypi.com) to write
**Raspberry Pi OS Lite** to a microSD card. In the imager's settings,
turn on SSH and set the username to the learner's name. Keep a second,
spare card with a fresh image on it, so a "broken" Pi is a 2-minute fix.

**Option C: a virtual machine in GNOME Boxes** (installed in step 2).
Download a Debian or Ubuntu Server ISO while online, then use Boxes to
make a VM. **Take a snapshot** right after installing, so "undo
everything" is one click.

The [Sandbox handbook](../labs/sandbox/README.md) says how to adapt the
lessons for a Pi or a VM.

## Later: Nand to Tetris (Stage 6)

Nothing new to install: the Nand to Tetris tools come with the offline
library (`mirror-library.sh`), and they use the Java installed in step
2. Before Lesson 6.1, give the learner the project files with
`./scripts/give-lab.sh sam n2t`. The
[Nand to Tetris handbook](../labs/n2t/README.md) has the details, and
what to do if the download fails.

## Later: Algorithms (Stage 7)

Nothing new to install: Stage 7 is Python, Thonny and the turtle, from
Stages 2 and 3. Before Lesson 7.1, run `./scripts/give-lab.sh sam algo`.
The [Algorithms lab handbook](../labs/algo/README.md) explains the
checker.

## Later: C and the software stack (Stage 8)

While online, from your own account, install the C tools (`gcc`, `gdb`,
`valgrind` and the C manual pages):

```bash
./scripts/install-packages.sh --later
```

Before Lesson 8.6, run `./scripts/give-lab.sh sam stack`. The rest of
Stage 8 uses the Nand to Tetris tools from Stage 6. The
[Nand to Tetris handbook](../labs/n2t/README.md) has a section on
Stage 8.

## Later: Rust (Stage 9)

Rust is installed *in the learner's account* (it doesn't need admin).
Before Lesson 9.1, from your own account:

```bash
./scripts/give-lab.sh sam rust
```

Then, **as the learner, while online**:

```bash
bash ~/lab/rust/setup-rust.sh
```

It installs Rust with rustup (the official installer, no account), the
offline Rust books, Rustlings, and the six outside libraries ("crates")
that Stage 9 uses, then switches Cargo to offline mode. It takes 5 to
15 minutes and about 2 GB of the learner's disk. After that, `rustup doc
--book` opens *The Rust Programming Language* offline, and all of Stage
9 works with no internet. The [Rust lab handbook](../labs/rust/README.md)
explains how to fetch another crate later, if you ever need one.

## Later: operating systems (Stage 10)

Before Lesson 10.1, from your own account, while online:

```bash
./scripts/install-packages.sh --later   # QEMU, strace and bsdtar (if not done for Stage 8)
./scripts/give-lab.sh sam os
sudo usermod -aG kvm sam                # fast virtual machines; sam logs out and in again
```

Then, **as the learner, while online** (after Stage 9's `setup-rust.sh`):

```bash
bash ~/lab/os/setup-os.sh
```

It installs a pinned nightly Rust compiler for the kernel lessons,
`bootimage`, and the `musl` target, and builds the kernel kit once, so
that its crates are cached. It takes 5 to 10 minutes and about 1 GB.
Lesson 10.11 also needs the internet: it downloads and installs Arch
Linux in a virtual machine (about 2.5 GB). The
[OS lab handbook](../labs/os/README.md) has the details.

## Later: networks and security (Stage 11)

Before Lesson 11.1, from your own account, while online:

```bash
./scripts/install-packages.sh --later   # dig, tracepath, curl and openssl
cd labs/sandbox
./sandbox.sh build sam                  # the Sandbox, with network tools and a firewall
./sandbox.sh reset                      # start it again from the new image
```

Then, as the learner: `ssh-keygen -R '[localhost]:2222'` (the rebuilt
Sandbox has a new identity, and `ssh` would otherwise refuse it with a
warning). Before Lesson 11.9, run `./scripts/give-lab.sh sam net`. Read
the [Hacker's Pledge](HACKER-PLEDGE.md) with the learner before Lesson
11.4. The [net lab handbook](../labs/net/README.md) has the answers and
the safety notes.

## Later: languages and data (Stage 12)

Before Lesson 12.2, from your own account, while online (if not done
already for Stage 8 or 10):

```bash
./scripts/install-packages.sh --later   # includes MIT Scheme
```

Before Lesson 12.5, run `./scripts/give-lab.sh sam lang`: it puts
`check-pickaxe` and its tests in `~/lab/lang`. Lessons 12.11 and 12.12
use the Stage 5 SQL lab (`give-lab.sh sam sql`). The [language lab
handbook](../labs/lang/README.md) has the finished interpreter, for you.

## Later: specialize and contribute (Stage 13)

Lessons 13.2 to 13.4 need only Git, `gcc` and the offline library. For
Lesson 13.4, make a bundle of your copy of the course where the learner
can read it: `git bundle create /tmp/course.bundle --all` from the
course's folder.

**The Pico path** (Lessons 13.5 to 13.7), from your own account, while
online:

```bash
./scripts/install-packages.sh --later   # includes libudev-dev, pkg-config, Node.js
./scripts/give-lab.sh sam pico
sudo usermod -aG dialout sam            # for the Pico's USB serial, Lesson 13.7
```

Then, logged in as the learner and online: `bash
~/lab/pico/setup-pico.sh` (Stage 9's `setup-rust.sh` must have run
first). The [Pico lab handbook](../labs/pico/README.md) lists the parts
to buy and explains loading programs and the emulator.

**The Linux From Scratch path** (Lesson 13.8): download the book (stable,
System V) from the LFS website into `/srv/redstone-library/books/lfs/`,
and keep about 40 GB free. The lesson explains the rest.

## Checklist

- [ ] Packages installed, guide logged out and back in
- [ ] Learner account made; learner can log in
- [ ] Offline library downloaded; hand downloads done
- [ ] Mineshaft built, started and tested
- [ ] (Before Stage 5) Sandbox built and started
- [ ] Hacker's Pledge printed (`docs/HACKER-PLEDGE.md`)
- [ ] Passport printed (`PASSPORT.md`)
- [ ] A paper notebook for the lab notebook
