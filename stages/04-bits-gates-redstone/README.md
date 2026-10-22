# Stage 4: Bits, Gates & Redstone

**Badge:** Redstone Engineer · **Needs first:** Stage 3; place value
(ones, tens, hundreds) and doubling. Powers of 2 are taught in the
stage · **Lessons:** 14

The course goes **down** inside the computer. The learner starts with the
binary from Stage 0's dot cards and finds out how a computer stores
numbers, colours and letters as bits, using Python to check everything.
Then they meet **logic gates**: first on paper and in Python, then as
redstone-style circuits they can walk around inside, in **Luanti** with
the **Mesecons** mod, and finally in **Digital**, a real circuit
simulator. They discover that NAND can build every other gate, that
adding numbers is just XOR and AND, and that memory is a loop of two
gates. The stage ends with ladder logic (how factory machines are
programmed) and a machine of the learner's own design.

Every lesson is fully scripted. The Python programs, the Digital test
tables and the Luanti build plans in this stage were all checked by
automated tests: the programs run, the circuits pass, and the builds
work exactly as drawn.

## Tools

- **Thonny** and Python, as before. Programs go in `~/lab/python/binary/`.
- **xxd** (installed by setup), for looking at the bytes inside files in
  Lessons 4.4 and 4.5.
- **Luanti** (called **Minetest** on Pop!_OS 24.04 and older) with the
  **Mesecons** mod, both installed by setup, for Lessons 4.7, 4.8, 4.10
  and 4.14. Before Lesson 4.7, the guide gives the learner a ready-made
  world with `./scripts/give-lab.sh LEARNER redstone`: flat, creative,
  no damage, Mesecons switched on. Lesson 4.7 lists the controls.
- **Digital** (in the offline library, `/srv/redstone-library/tools/Digital/`,
  put there by `mirror-library.sh`), a logic circuit simulator, for
  Lessons 4.9 to 4.14. It needs Java, installed by setup. Lesson 4.9 sets
  up a short `digital` command and has a table of how to use it. Circuits
  go in `~/lab/circuits/`.
- References for the guide: the Digital manual (`Documentation_en.pdf`,
  in the same folder as Digital); *Code: The Hidden Language of Computer
  Hardware and Software* by Charles Petzold, if you can borrow it, is
  the best book there is for this stage. **(Online, optional, no
  account):** *nandgame.com*, a puzzle game that builds a computer from
  NAND gates.

## Lessons

| # | Lesson | What happens | Key ideas |
|---|---|---|---|
| 4.1 | [Counting Like a Computer](01-counting-like-a-computer.md) | Place value in base ten and base two; bits and bytes; `bin()` and a counting machine | binary, place value, byte |
| 4.2 | [The Doubling Machine](02-the-doubling-machine.md) | Powers of two, the chessboard and the rice, halving to find a number, kilobytes | powers of 2, exponents |
| 4.3 | [The Binary Machine](03-the-binary-machine.md) | Convert by halving and doubling, on paper and in Python, with round-trip tests; a binary quiz | algorithms, testing |
| 4.4 | [Hex, Binary's Shorthand](04-hex-binary-shorthand.md) | Sixteen digits, colour codes, a colour mixer, and the magic number inside a PNG | hexadecimal, bytes in files |
| 4.5 | [Letters Are Numbers](05-letters-are-numbers.md) | ASCII, `ord` and `chr`, binary messages, newlines in a hex dump, Unicode and emoji | encoding, ASCII, UTF-8 |
| 4.6 | [True or False Machines](06-true-or-false-machines.md) | NOT, AND, OR and XOR on paper, as a people game, and in Python truth tables | logic gates, truth tables |
| 4.7 | [Redstone Basics](07-redstone-basics.md) | Luanti and Mesecons: a lamp circuit, a torch NOT, wires as OR | circuits, inverter |
| 4.8 | [Torch Logic and Gate Blocks](08-torch-logic-and-gate-blocks.md) | AND from torches (De Morgan's law); gate blocks; a two-key vault door and a stair light | De Morgan, combining gates |
| 4.9 | [NAND Builds Everything](09-nand-builds-everything.md) | The Digital simulator; test cases; NOT, AND and OR from NAND alone | simulation, universal gates |
| 4.10 | [Adding with Gates](10-adding-with-gates.md) | Binary sums with carries; the half adder in Digital, Python and Luanti | arithmetic is logic |
| 4.11 | [The Adding Machine](11-the-adding-machine.md) | Full adders from half adders, a 4-bit ripple-carry adder, and the same in Python | abstraction, sub-circuits |
| 4.12 | [Circuits That Remember](12-circuits-that-remember.md) | Feedback and the SR latch; why computers reset; a Python latch | memory, state |
| 4.13 | [Ladder Logic, How Factories Think](13-ladder-logic.md) | PLCs and ladder diagrams; the seal-in rung; a pretend PLC scan in Python | control systems, scan cycle |
| 4.14 | [Project: My Redstone Machine](14-my-redstone-machine.md) | Specify, design, test in Digital, build in Luanti, demo day; Stage 4 checkpoint | putting it together |

## Free play for this stage

- Luanti in the **redstone-lab** world: pistons, note blocks, pressure
  plates, doors and lamps are all in the creative inventory. Pistons
  and doors make great traps and secret entrances.
- Digital's own examples, in `/srv/redstone-library/tools/Digital/examples/`
  (try `combinatorial` and `74xx`).
- Finger binary and hex speed rounds.
- The binary quiz from Lesson 4.3, against the family.

## Habits to build now

- **Truth table first.** Before building any circuit, write down what it
  should do, for every input.
- **Test the design, then build it.** Digital test cases, like Python
  `assert`s, catch mistakes while they're cheap to fix.
- **Build one piece at a time.** In Luanti, test each gate with its own
  lamp before connecting it to the next.
- **Label everything.** Inputs and outputs in Digital; signs in Luanti.

## Checkpoint

The learner can, without help:
- [ ] Convert between ordinary numbers, binary and hex, for numbers up to 255
- [ ] Explain how letters and colours are stored as numbers
- [ ] Write truth tables for NOT, AND, OR, XOR and NAND, and build each
      in Python, Luanti or Digital
- [ ] Build NOT, AND and OR from NAND gates in Digital, with passing tests
- [ ] Explain and build a half adder, and explain how full adders chain
      into a bigger adder
- [ ] Explain how a latch remembers one bit

They can also:
- [ ] Read a simple ladder rung, including the seal-in
- [ ] Turn a specification into a truth table, a tested design, and a
      working Luanti machine
