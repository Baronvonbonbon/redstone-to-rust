# Lesson 6.9: Memory and the Program Counter (Project 3, Part 2)

**Time:** 3 sessions of 45 min · **You need:** a terminal; `~/lab/n2t`;
squared paper; the HDL card · **New words:** RAM, address, program
counter, reset

## Goal *(read this to the learner)*

> One register remembers one number. A computer needs thousands. Today
> you'll build **RAM**: thousands of registers, each with its own number,
> called its **address**, like the numbered boxes of a huge Minecraft
> storage room. You'll start with 8 boxes and keep multiplying by 8 until
> you have 16,384. Then you'll build the **program counter**, which keeps
> track of which instruction the computer runs next.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Bit and Register should pass (Lesson 6.8).

## Warm-up (5 min)

"What does a DMux8Way do?" *(Sends one input to one of eight outputs,
chosen by `sel`.)* "And a Mux8Way16?" *(Chooses one of eight 16-bit
inputs.)* "How many numbers can 3 bits count?" *(8: 000 to 111.)*

## Activity

### Session 1: RAM8

1. **What RAM does.** `cd ~/lab/n2t/projects/3/a` and `cat RAM8.hdl`.
   **Say:** "Eight registers. The `address` picks one of them. If `load`
   is 1, the number on `in` is stored in that one register, and none of
   the others. And `out` always shows what's in the register at
   `address`."

   Act it out: eight numbered boxes (cups or paper squares). The guide
   calls "store 42 in box 5" and "what's in box 3?"; the learner does it.

2. **Design it on paper.** Remember Lesson 6.3: a DMux sends something
   to one place, and a Mux picks one thing out. Hints, one at a time:
   - "Only one register should get `load`. Which chip sends `load` to
     exactly one of eight places?" *(DMux8Way, with `sel` = `address`.)*
   - "Which register's number comes out? Which chip picks one of eight
     numbers?" *(Mux8Way16, with `sel` = `address`.)*
   - "Which registers get the number on `in`?" *(All of them! But only
     the one that gets `load` will keep it.)*

   Draw it: the DMux8Way at the top, eight Registers in the middle, the
   Mux8Way16 at the bottom. *(Guide: ten parts.)*

3. **Build and test.** Write it, then `hardware RAM8.tst`, and commit.
   **Say:** "That's a memory with eight boxes. Now for the clever part:
   using it to build bigger ones."

### Session 2: bigger and bigger

4. **RAM64: eight RAM8s.** `cat RAM64.hdl`: `address[6]`. **Say:** "Six
   address bits. Think of a big storage room with 8 chests, each with 8
   slots. To find slot 29, which chest, and which slot in it?" *(29 =
   3 × 8 + 5: chest 3, slot 5.)* "In binary, 29 is `011 101`. The left
   three bits are the chest, and the right three are the slot!"

   Hints:
   - "Which address bits choose the RAM8?" *(The left three:
     `address[3..5]`.)*
   - "Which address bits go *into* every RAM8?" *(The right three:
     `address[0..2]`.)*
   - "Otherwise it's just like RAM8, with RAM8s instead of Registers."

   Build, test, commit. *(Ten parts again.)*

5. **RAM512, RAM4K, RAM16K.** `cd ../b`. **They should see:** these three
   chips, but no RAM64. **Say:** "In this folder, the simulator uses its
   built-in RAM64. Each chip is eight of the one before. Work out the
   address bits for each one on paper first."

   | Chip | Address bits | Made of | Bits that choose | Bits that go inside |
   |---|---|---|---|---|
   | RAM512 | 9 | 8 × RAM64 | `address[6..8]` | `address[0..5]` |
   | RAM4K | 12 | 8 × RAM512 | ? | ? |
   | RAM16K | 14 | **4** × RAM4K | ? | ? |

   *(RAM4K: `[9..11]` and `[0..8]`. RAM16K: only four chips, so it
   needs a four-way DMux and Mux, and two choosing bits, `[12..13]`, with
   `[0..11]` going inside.)*

   Build each, test, commit. RAM16K's test takes a little longer.

### Session 3: the program counter

6. **What the PC does.** `cd ../a` and `cat PC.hdl`. **Say:** "A program
   is a list of instructions, numbered 0, 1, 2... The **program counter**
   holds the number of the next one to run. Usually it just counts up by
   one. But sometimes the program says 'jump to instruction 7', and
   sometimes we want to start again from 0." Read the rules in the comment
   together:
   ```
   if      reset(t): out(t+1) = 0
   else if load(t):  out(t+1) = in(t)
   else if inc(t):   out(t+1) = out(t) + 1
   else              out(t+1) = out(t)
   ```
   **Say:** "`reset` wins over everything. Then `load`. Then `inc`."

7. **Design it.** The PC is a Register (to remember the count) plus some
   choosing in front of it. Hints, one at a time:
   - "Where's the current count?" *(Coming out of the Register.)*
   - "How do you make 'count + 1'?" *(Inc16, from Lesson 6.6.)*
   - "Each rule chooses between keeping the number so far and changing
     it. Which chip chooses?" *(Mux16. One for each rule.)*
   - "The rule that wins must be the *last* choice before the Register.
     Which one wins?" *(`reset`. So the order is inc, then load, then
     reset.)*
   - "What does the Register's `load` need to be?" *(It can always be
     1: the Muxes in front have already decided what to store.)*

   Draw it, build it, test it (`hardware PC.tst`), commit.

8. **Project 3 is done!** Run every test in both folders:
   ```
   cd ~/lab/n2t/projects/3
   for t in a/*.tst b/*.tst; do echo -n "$t: "; (cd $(dirname $t) && hardware $(basename $t)); done
   ```
   Then `git commit -am "Project 3: memory and the PC"`.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| A RAM test fails on a row where another address was loaded | `load` reaches more than one register | `load` must go through the DMux, not straight to the registers. |
| RAM fails when reading back | `out` isn't chosen by `address` | Every register's output goes into the Mux8Way16, with `sel` = `address`. |
| `address(3) and address(6) have different bus widths` or similar | A whole `address` bus went where part of it belongs | Use sub-buses: `address[0..2]` and `address[3..5]`. |
| RAM64 passes some rows but not others | The choosing bits and the inside bits are mixed up | The same bits must choose the RAM8 in *both* the DMux and the Mux. |
| PC fails on a row with `reset` 1 | `reset` isn't the last choice | The Mux16 for `reset` must be the last one before the Register. |
| PC fails on a row with `inc` 1 | Inc16 isn't counting from the Register's output | Inc16's input is the loop from the Register's output. |

## Talk about it

- What's an address?
- How did you split the address bits in RAM64?
- Why does `reset` have to be the last Mux?
- How many registers are in RAM16K? How many Bits?

## Challenge *(if there's time, or for next time)*

- RAM16K has 16,384 registers of 16 bits. How many DFFs is that? How
  many bytes? *(262,144 DFFs; 32,768 bytes, or 32 KB.)*
- Why did the course make RAM16K from four RAM4Ks, and not eight?

## Checkpoint

The learner can, without help:
- [ ] Explain RAM, addresses and `load`
- [ ] Build RAM8 from a DMux, registers and a Mux
- [ ] Split an address into "which chip" and "which box inside"
- [ ] Explain the PC's three rules and why `reset` is last

## Lab notebook

Draw RAM8, and the address split for RAM64 with the storage-room
picture. Draw the PC's Mux chain. Commit. Add *RAM*, *address*, *program
counter* and *reset* to `dictionary.md`. Tick
Project 3 on the passport's Nand to Tetris climb.

## Guide's background *(optional reading)*

**RAM** stands for "random access memory": any address can be read or
written in the same time, unlike a tape that must be wound to the right
place. The recursive design (each RAM is eight of the smaller one, with
the address split into "which block" and "which word in the block") is
how real memory is organised too, in banks, rows and columns.

The **program counter** is how a CPU steps through a program: it
increments after each instruction, loads a new address for a jump, and
resets to 0 when the computer starts. Lesson 6.12 connects it to the
CPU, and Lesson 6.10 shows it from the programmer's side.
