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

Rust is installed *in the learner's account* (it doesn't need admin),
while online:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
rustup component add rust-docs rust-src
cargo install rustlings
```

After that, `rustup doc --book` opens *The Rust Programming Language*
offline. Rust projects that use outside libraries ("crates") need them
downloaded once while online (`cargo fetch` inside the project). Stage 9
tells you when.

## Checklist

- [ ] Packages installed, guide logged out and back in
- [ ] Learner account made; learner can log in
- [ ] Offline library downloaded; hand downloads done
- [ ] Mineshaft built, started and tested
- [ ] (Before Stage 5) Sandbox built and started
- [ ] Hacker's Pledge printed (`docs/HACKER-PLEDGE.md`)
- [ ] Passport printed (`PASSPORT.md`)
- [ ] A paper notebook for the lab notebook
