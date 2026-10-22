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

This installs everything for Stages 0 to 5: typing tutors, GCompris,
terminal toys, Python with Thonny and Pygame Zero, Luanti with the
Mesecons circuits mod, git, Docker and GNOME Boxes. **Log out and back
in afterwards**, so your account can use Docker.

Run it again with `--later` when you reach Stage 6.

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
```

The cave and the heist print the answer for you. Don't let the learner see it!

## Later: a breakable computer (Stage 5)

In Stage 5 the learner gets a computer where they *are* the admin, and
where breaking things is fine. Pick one:

**Option A: Raspberry Pi (best).** It's a real, separate machine, and it
feels like theirs. Use Raspberry Pi Imager (`flatpak install flathub
org.raspberrypi.rpi-imager`, or download it from raspberrypi.com) to write
**Raspberry Pi OS Lite** to a microSD card. In the imager's settings,
turn on SSH and set the username to the learner's name. Keep a second,
spare card with a fresh image on it, so a "broken" Pi is a 2-minute fix.

**Option B: a virtual machine in GNOME Boxes** (installed in step 2).
Download a Debian or Ubuntu Server ISO while online, then use Boxes to
make a VM. **Take a snapshot** right after installing, so "undo
everything" is one click.

Lesson 5.1 walks through either option.

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
- [ ] Hacker's Pledge printed (`docs/HACKER-PLEDGE.md`)
- [ ] Passport printed (`PASSPORT.md`)
- [ ] A paper notebook for the lab notebook
