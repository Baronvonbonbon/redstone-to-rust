# Lesson 13.8: Linux From Scratch

**Time:** 2 sessions of 45 min, then a long quest (weeks) · **You
need:** the internet for the first session; the Arch VM from Lesson
10.11; about 40 GB of free disk space; the *Linux From Scratch* book ·
**New words:** toolchain, bootstrap, source package, chroot, SBU

## Goal *(read this to the learner)*

> In Stage 10 you installed Arch Linux by hand, but every program in it
> came ready-made. Linux From Scratch goes further: you build every
> program yourself, from its source code, starting with the compiler,
> until you have a whole Linux system that boots, and you know what
> every single file in it is for. It's a long climb, weeks of sessions,
> with a real book written for grown-ups. Today you'll plan the climb
> and take the first steps.

## Before the lesson *(guide, 30 min, and read this first)*

**Be honest with yourself and the learner: this path is different.**
The other lessons in this course were run, command by command, by the
course's authors. Linux From Scratch is too long and changes too often
for that: the *book* is the script, and it's an excellent one, written
and tested by the LFS project for every release. This lesson gets the
learner ready to follow it, and suggests how to break it into sessions.
Expect to read each section of the book yourself before the learner
does, and expect things to go wrong (they do for everyone; that's the
point).

- [ ] Read the book's Preface and Chapter 1 ("Introduction"). Read it
      online at [linuxfromscratch.org/lfs/read.html](https://www.linuxfromscratch.org/lfs/read.html),
      choosing the **stable**, **System V** version (it's simpler than
      the systemd one).
- [ ] Check the book is in the library for offline use:
      `ls /srv/redstone-library/books/lfs/` shows a file like
      `LFS-BOOK-12.4-NOCHUNKS.html` (the whole book in one page; open it
      in the browser). `mirror-library.sh` downloads it; re-run that
      script if it's missing. The book is CC BY-NC-SA (see
      Lesson 13.3), so keep it for your own use; don't put it in the
      course's repository.
- [ ] Check there's room: `df -h ~` should show at least 40 GB free.
- [ ] Make sure Lesson 10.11's Arch VM boots, and has its `fresh`
      snapshot.

## Warm-up (5 min)

"When you install a program with `apt` or `pacman`, where did it come
from? Who compiled it?" *(Someone else, on another computer.)* "What
compiled the compiler?" Let that one sit.

## Activity

### Session 1: the plan

1. **The chicken and the egg.** **Say:** "To compile programs, you need
   a compiler. But the compiler is a program too. How do you compile the
   first compiler?" *(You use an older compiler from another system.)*
   **Say:** "Getting a system started from almost nothing is called
   **bootstrapping**, from 'pulling yourself up by your bootstraps'.
   It's what Nand to Tetris did, one level at a time: gates, then the
   CPU, then the assembler, then the compiler."

2. **The map of the book.** Open the offline book's table of contents
   together. Draw the five big steps as a mountain path:
   1. **Prepare**: a new disk, a user called `lfs`, and the **source
      packages** (about 90 programs' source code). *(Chapters 2–4.)*
   2. **A cross toolchain**: a temporary compiler, built with Arch's
      compiler, that makes programs for the new system. *(Chapters 5–6.)*
      **Ask:** "Have you cross-compiled before?" *(Yes! The Pico, in
      Lesson 13.5.)*
   3. **Into the new system**: `chroot`, which makes a folder pretend to
      be the whole computer, so you work inside your new system.
      *(Chapter 7.)*
   4. **The real system**: every program, one by one, from `glibc` and
      `gcc` to `bash`, `grep` and `vim`. *(Chapter 8: the long one.)*
   5. **Make it boot**: settings, the Linux kernel, and GRUB.
      *(Chapters 9–10.)* *"Like Lesson 10.11's GRUB, but you built the
      kernel yourself."*

3. **How long?** Find the **SBU** in the book (Chapter 4, "About
   SBUs"). **Say:** "One SBU is the time it takes to build the first
   package on your computer. Every package in the book says how many
   SBUs it takes. Then you can plan sessions." Write a rough plan on
   the quest card, in milestones: one milestone per step above. Most
   learners need 15–30 sessions.

4. **The rules for this quest.** Read the book's "How to Build an LFS
   System" together, then agree:
   - Read each section all the way through **before** typing anything.
   - Type the commands; don't paste them. (It's slower, and that's how
     you notice what they do.)
   - Every session ends with a journal entry: the last section you
     finished, and anything that went wrong.
   - Before each big step, make a VM snapshot (Lesson 10.11), so a
     mistake costs a session, not a month.

### Session 2: the first steps

5. **A disk for the new system.** On the PC, next to the Arch VM:
   ```
   cd ~/lab/os/arch
   qemu-img create -f qcow2 lfs.qcow2 30G
   qemu-img snapshot -c before-lfs arch.qcow2
   ```
   **They should see** `Formatting 'lfs.qcow2', fmt=qcow2 ...
   size=32212254720 ...` (30 GB, in bytes). Start the VM with the new
   disk as a second drive, and more memory and processors, since
   compiling is hard work:
   ```
   qemu-system-x86_64 -enable-kvm -m 4G -smp 4 -drive file=arch.qcow2,if=virtio -drive file=lfs.qcow2,if=virtio -nic user,model=virtio-net-pci
   ```
   In the VM, `lsblk`: the new disk is the one with nothing on it,
   probably `vdb`. **Ask:** "How do you know which is which?" *(Its
   size, 30G, and it has no partitions.)*

6. **Is the host ready?** The book's Chapter 2 ("Host System
   Requirements") has a script, `version-check.sh`, that checks every
   tool the build needs. Type it into the Arch VM as the book shows,
   run it, and install what it says is missing with `pacman -S` (the
   book's Arch-friendly names are mostly the same; `base-devel` gives
   most of them). Go on only when it reports everything OK.

7. **Follow the book.** From here, the book leads: Chapter 2's
   partitioning (on the *new* disk only: the guide checks the device
   name every time), then Chapter 3's downloads, and so on. **Say:**
   "This is your quest now. The guide is your partner, not your
   teacher: you both read the book." Make the quest repository's
   milestones match the five steps. Commit the journal every session.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `qemu-img: Could not create 'lfs.qcow2': Permission denied` | You're not in `~/lab/os/arch`, or it's owned by another user | `cd ~/lab/os/arch`, and check `ls -l`. |
| `lsblk` shows only one disk in the VM | The second `-drive` was left out | Shut down, and start the VM with the full command from step 5. |
| `version-check.sh` reports `ERROR` | A tool is missing or too old | `pacman -S` it (for example `texinfo`). The book says which versions are needed. |
| A package fails to build, and you can't see why | It happens to everyone | Read the last 30 lines of the error; check you're in the right folder, as the right user (`lfs` or `root`), with `$LFS` set (`echo $LFS`). The LFS FAQ and the book's "Errata" page help. |
| The whole system is in a mess | It happens | Go back to the last snapshot (`qemu-img snapshot -a ...`), and redo that section. Write down what went wrong. |
| A command in the book doesn't match your book | Two different book versions | Use one version of the book all the way through. |

## Talk about it

- What does bootstrapping mean? Where else have you seen it in this
  course?
- What are the five big steps of LFS?
- Why read each section before typing?
- Why snapshots before each big step?

## Challenge *(if there's time, or for next time)*

- Before you start Chapter 5, count the packages in the book's Chapter 3
  list. Which have you used already, in this course?
- Keep a "bill of materials" in the quest repository: every package you
  build, its version, and how many SBUs it took on your computer.
- After LFS boots: *Beyond Linux From Scratch* (BLFS) adds networking, a
  graphical desktop, and even Rust.

## Checkpoint

The learner can, without help:
- [ ] Explain bootstrapping and cross-compiling
- [ ] Name the five big steps of the LFS book
- [ ] Add a second disk to the VM and find it with `lsblk`
- [ ] Run the host check and fix what it reports
- [ ] Keep a journal entry for every LFS session

## Lab notebook

Draw the five-step mountain path, and mark it as you climb. Keep the
SBU plan. Add *toolchain*, *bootstrap*, *source package*, *chroot* and
*SBU* to `dictionary.md`.

## Guide's background *(optional reading)*

*Linux From Scratch* (LFS) has been maintained since 1999, with a new
stable book about twice a year; its commands are tested for each
release, which is why this course points to the book rather than
copying it. The build follows the classic three-stage bootstrap:
a cross toolchain (binutils, gcc and glibc) built for a deliberately
different target name, so nothing from the host leaks in; temporary
tools built with it; then a chroot, inside which the final system is
built natively. The book's tests (`make check`) can be skipped by a
learner, at some risk; the book says which ones matter.

Time and space: on a modern four-core PC, 1 SBU is a few minutes, and
the whole of Chapters 5–8 is roughly 200–300 SBU with tests, so plan in
sessions, not days. The sources are about 500 MB, the finished system a
few GB, and the VM's two disks around 25 GB. LFS uses the host's
compiler only in Chapter 5, so the Arch VM from Lesson 10.11 (with
`base-devel`) is a good host; any recent Linux distribution would also
do.
