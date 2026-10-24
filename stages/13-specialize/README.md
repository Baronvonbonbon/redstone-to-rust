# Stage 13: Specialize & Contribute

**Badge:** Open Source Contributor · **Needs first:** Stage 12 ·
**Lessons:** 10 (four for everyone, a path, then two to finish), and an
open-ended quest

The last stage is different. The learner has seen the whole mountain,
from NAND gates to their own programming language. Now they choose
where to go deeper, learn how real open-source projects work, send a
patch to this course, take one path in depth, teach someone else, and
graduate. The guide becomes more of a mentor than a script reader.

- **Everyone** (Lessons 13.1–13.4): choosing a field, with stars and
  question marks on the passport, and planning a **quest** with
  milestones and a journal; reading a real codebase (clox, the C
  interpreter from *Crafting Interpreters*) with five rules, and
  comparing its scanner with Pickaxe's; licences, maintainers and
  patches, with the learner as maintainer; and the learner's first
  patch to this course, with review and a v2.
- **A path** (choose at least one):
  - **The Pico path** (13.5–13.7): a Raspberry Pi Pico in embedded
    Rust: `no_std`, cross-compiling and flashing a blink; the Cookie
    Factory's seal-in rung on real buttons, as a PLC scan; and a fan
    controller with the chip's thermometer, a setpoint, a deadband and
    USB serial. About $15 of parts, or the emulator for free.
  - **The Linux From Scratch path** (13.8): building a whole Linux
    system from source in a VM, following the LFS book over many
    sessions.
  - **A quest of the learner's own**, planned in Lesson 13.1 the same
    way.
- **Finishing** (13.9–13.10): writing a lesson with the course's
  template, trying it with a real student, and sending it as a patch;
  then a retrospective, a portfolio, a show-and-tell, and the last
  badge.

**How it was tested.** Lessons 13.2–13.4: every command was run, and the
outputs are real (clox built with `gcc`; the patch workflow run with
Git 2.43). The Pico programs were built with the pinned crates, checked
with `cargo fmt` and `cargo clippy`, and run as real `.uf2` files in the
**rp2040js emulator**, which produced every emulator output shown; they
have **not** yet been run on a physical Pico by the course's authors
(see the [Pico lab handbook](../../labs/pico/README.md)). Lesson 13.8
prepares the learner to follow the *Linux From Scratch* book, which is
tested by its own project for each release; this course doesn't
reproduce or test the build itself.

## Tools

- Git, `gcc` and the offline library (Stages 5 and 8; *Crafting
  Interpreters* is in `repos/crafting-interpreters`).
- **The Pico path:** a Raspberry Pi Pico H (or Pico; *not* a Pico W or
  Pico 2), a micro-USB data cable, a breadboard, 2 push buttons and
  jumper wires. Then `./scripts/install-packages.sh --later` (adds
  `libudev-dev`, `pkg-config` and Node.js), `./scripts/give-lab.sh
  LEARNER pico`, and, as the learner and online, `bash
  ~/lab/pico/setup-pico.sh`. Everything is in the [Pico lab
  handbook](../../labs/pico/README.md).
- **The LFS path:** the Arch VM from Lesson 10.11, about 40 GB of free
  disk, the internet for downloading the sources, and the *Linux From
  Scratch* book (stable, System V), downloaded from
  [linuxfromscratch.org](https://www.linuxfromscratch.org/lfs/) into
  the library.
- A "student" for Lesson 13.9, and an audience for Lesson 13.10.

## A note on the internet

Lessons 13.1–13.7, 13.9 and 13.10 work offline, once the Pico setup has
run. Lesson 13.8 needs the internet to download the LFS book and
sources (about 500 MB). Sending a learner's patch to a public project
needs an account, which is the guide's, never the learner's (Lesson
13.4).

## Lessons

| # | Lesson | What happens | Key ideas |
|---|---|---|---|
| 13.1 | [Choose Your Path](01-choose-your-path.md) | The mountain map; stars and question marks; fields of computing; OSSU; a quest card and a journal | planning |
| 13.2 | [Reading Real Code](02-reading-real-code.md) | Five rules; building and exploring clox; its scanner beside Pickaxe's; answering a question by reading | code reading |
| 13.3 | [How Open Source Works](03-how-open-source-works.md) | Copyright and licences; maintainers; reviewing and applying a guide's patch with `git am` | licences, review |
| 13.4 | [Your First Patch](04-your-first-patch.md) | A bundle of the course; a branch; a fix; `git format-patch`; review and v2; credit | contributing |
| 13.5 | [Hello, Pico](05-hello-pico.md) | Microcontrollers; the kit; `no_std` and `#[entry]`; cross-compiling; blink | embedded |
| 13.6 | [The Cookie Factory, for Real](06-cookie-factory-pico.md) | Wiring buttons; pull-ups; the seal-in rung as a scan; scan time; fail-safe | GPIO, PLC |
| 13.7 | [The Fan Controller](07-fan-controller.md) | The chip's thermometer and ADC; setpoint and deadband; USB serial | control loops |
| 13.8 | [Linux From Scratch](08-linux-from-scratch.md) | Bootstrapping; the book's five steps; SBUs; a second VM disk; the host check | toolchains |
| 13.9 | [Teach It](09-teach-it.md) | Writing a lesson from the template; a trial run; feedback; a patch | teaching |
| 13.10 | [Graduation](10-graduation.md) | Retrospective; portfolio; show-and-tell; the last badge; what's next | reflection |

Lessons 13.5–13.7 are the Pico path and 13.8 the LFS path; a learner
does at least one path, or their own quest, between 13.4 and 13.9.

## Setup notes

- The learner's Stage 13 work lives in `~/lab/quest` (a Git repository
  with `QUEST.md`, `JOURNAL.md` and, later, `PORTFOLIO.md`), with
  `clox` (13.2) and `course` (the course clone, 13.4) inside it, and in
  `~/lab/pico` (one folder per program, copied from `kit`) or the LFS
  disk next to the Arch VM in `~/lab/os/arch`.
- The guide's bundle of the course goes in `/tmp/course.bundle`; make a
  new one whenever the course changes.
- `give-lab.sh LEARNER pico` can be run again safely: it refreshes the
  kit, the reference programs and the emulator script, and leaves the
  learner's programs alone.

## Free play for this stage

- More codebases from the library, with the five rules.
- Pico projects: a reaction-time game with a button and the LED; a
  Morse code sender; a dice roller; the full Cookie Factory with a
  sensor button and a stamper LED.
- Beyond Linux From Scratch, after LFS boots.
- More patches: typos, error rows, challenges, cheat sheets.

## Habits to build now

- **Small first steps.** Every quest starts with something that fits in
  one session.
- **Read before you write.** Other people's code, the book's section, the
  project's rules.
- **Keep a journal.** What I did, what surprised me, what's next.
- **Review kindly; take review well.** Every patch gets a v2 sometimes.
- **Fail safe.** Ask what happens when a wire breaks.
- **Teach it to learn it.**

## Checkpoint

The learner can, without help:
- [ ] Plan a quest with a small first step and milestones, and keep a
      journal
- [ ] Find their way around an unfamiliar codebase and answer a
      question by reading it
- [ ] Explain permissive, copyleft and Creative Commons licences
- [ ] Review and apply a patch, and make one with `git format-patch`
- [ ] Explain what they built on their path (the Pico's scan loop and
      deadband, LFS's bootstrap, or their own quest's design)

They can also:
- [ ] Show a patch of theirs that was accepted into the course
- [ ] Show a lesson they wrote and tried with a real student
- [ ] Present their quest to an audience (Lesson 13.10)
