# Lesson 6.1: The Big Climb

**Time:** 2 sessions of 45 min · **You need:** a terminal; nano or vim;
the Nand to Tetris tools and project files (see below); the
[HDL card](../../labs/n2t/HDL-CARD.md), printed · **New words:** HDL,
chip, pin, part, internal pin, test script

## Goal *(read this to the learner)*

> In Stage 4 you built gates by drawing them in Digital. This stage, you
> build a whole computer, starting from nothing but NAND gates: memory, a
> processor, a screen and a keyboard, until it runs programs you wrote.
> It's called **Nand to Tetris**, and it's a real university course. Real
> chip designers don't draw their chips: they write them as text, in a
> **hardware description language**. Today you'll learn that language and
> build your first chip with it: a creeper alarm.

## Before the lesson *(guide, 15 min)*

- [ ] Read this whole lesson once, and the [Stage 6 README](README.md)
      if you haven't.
- [ ] Check the tools are in the offline library (`mirror-library.sh`
      puts them there):
      ```
      ls /srv/redstone-library/tools/nand2tetris/tools
      ```
      You should see `HardwareSimulator.sh`, `CPUEmulator.sh`,
      `Assembler.sh` and others. If not, see
      [the Nand to Tetris handbook](../../labs/n2t/README.md).
- [ ] From **your own** account, in the course folder, give the learner
      the project files and the practice chips:
      ```
      ./scripts/give-lab.sh LEARNER n2t
      ```
      They go in `~/lab/n2t/` in the learner's account.
- [ ] Print the [HDL card](../../labs/n2t/HDL-CARD.md).

## Warm-up (5 min)

"In Lesson 4.9, how did you make NOT from a NAND gate?" *(Both inputs of
the NAND joined together.)* "And AND?" *(A NAND, then a NOT.)* "What
makes a 1 come out of an AND gate?" *(Both inputs 1.)*

## Activity

### Session 1: the first chip

1. **The climb.** Draw this on paper together, from the bottom up:
   ```
   Tetris (a game)                 <- Stage 8
   an operating system             <- Stage 8
   a programming language          <- Stage 8
   machine language                <- this stage
   the computer: CPU + memory      <- this stage
   memory, adders, the ALU         <- this stage
   AND, OR, NOT, XOR               <- this stage (and Stage 4)
   NAND                            <- given: the only thing you don't build
   ```
   **Say:** "Every layer is built only from the layer below it. By the end
   of this stage, you'll have built the bottom six, and your computer will
   run programs. In Stage 8, you climb the rest of the way."

2. **Short commands for the tools.** The tools live in the offline
   library. Make links to them in `~/bin`, as with `stacks` in Lesson
   5.16:
   ```
   ln -s /srv/redstone-library/tools/nand2tetris/tools/HardwareSimulator.sh ~/bin/hardware
   ln -s /srv/redstone-library/tools/nand2tetris/tools/CPUEmulator.sh ~/bin/cpu
   ln -s /srv/redstone-library/tools/nand2tetris/tools/Assembler.sh ~/bin/assembler
   hardware --help
   ```
   **They should see:** a short usage message, with the lines `hardware`
   (to open the simulator's window) and `hardware FILE.tst` (to run a
   test).

3. **Look around, and save the starting point.**
   ```
   cd ~/lab/n2t
   ls
   ls projects/1
   ```
   **They should see:** `practice` and `projects`; then files like
   `And.hdl`, `And.tst` and `And.cmp`. **Say:** "For every chip there are
   three files. `.hdl` is the chip: that's the one you write. `.tst` is a
   **test script** that tries it out, and `.cmp` holds the right answers to
   compare against."

   Put it all in git, so every chip you build is saved:
   ```
   git init
   echo "*.out" > .gitignore
   git add .
   git commit -m "Nand to Tetris, before I built anything"
   ```
   (`.out` files are made by the tests every time they run, so git can
   ignore them.)

4. **Read a chip.**
   ```
   cd practice
   cat CreeperAlarm.hdl
   ```
   Read it together. **Say:**
   - "`CHIP CreeperAlarm` is the chip's name. It must match the file name.
   - `IN` lists the input **pins**, and `OUT` the output pins: the wires
     that come in and go out, like the switches and the lamp in Luanti.
   - `PARTS:` is where you list the chips inside it. That's what you
     write."

5. **Build it.** The comment says `alarm = creeper and night and
   not(inside)`. On paper, draw the gates first: an AND for creeper and
   night, a NOT for inside, and an AND to combine them. Name the two
   wires in the middle: `danger` and `outside`.

   Then open the file (`nano CreeperAlarm.hdl`) and replace the line
   `// Your parts go here.` with:
   ```
       And(a=creeper, b=night, out=danger);
       Not(in=inside, out=outside);
       And(a=danger, b=outside, out=alarm);
   ```
   **Say:** "Each line is one part. `And(a=creeper, ...)` means 'an AND
   chip, with its `a` pin connected to `creeper`'. The left side is always
   the part's own pin name, and the right side is a wire in *our* chip.
   `danger` and `outside` are **internal pins**: wires you invent by
   naming them. Every line ends with `;`."

6. **Test it.**
   ```
   hardware CreeperAlarm.tst
   ```
   **They should see:** `End of script - Comparison ended successfully`.
   Celebrate: that's a chip!

   **Say:** "The test set the three inputs to every combination, like a
   truth table, and checked every answer." Look at what it recorded:
   `cat CreeperAlarm.out`. **They should see:** the truth table, with
   `alarm` 1 only on the row `1 1 0`.

7. **Break it on purpose.** Change the last line to use `inside` instead
   of `outside`, save, and test again. **They should see:** `Comparison
   failure at line 8`. **Say:** "Line 8 of the answers is where yours went
   wrong. The `.out` file stops at the first wrong line." Compare them:
   ```
   diff CreeperAlarm.out CreeperAlarm.cmp
   ```
   **They should see:** your line 8 (`< ... 0`) next to the right answer
   (`> ... 1`). Put it back and test until it passes.

### Session 2: the Hardware Simulator, and a chip on your own

8. **Open the simulator.** `hardware`. A window opens. Click the first
   button on the toolbar (the chip picture, **Load Chip**). In **File
   Name**, type the whole path, with the learner's own name:
   `/home/sam/lab/n2t/practice/CreeperAlarm.hdl`, and press Enter. (Or
   click through the folders.)

   **They should see:** the chip's name, its **Input pins** and **Output
   pins** with their values, the HDL, and **Internal pins** with `danger`
   and `outside`.

9. **Poke it.** Double-click the `0` next to `creeper`, type `1`, and
   press Enter. Do the same for `night`. The output turns grey: it's out
   of date. Click the **calculator** button (Eval). **They should see:**
   `alarm` become `1`, and the internal pins change. Now set `inside` to
   1, and Eval again. Explore every combination.

10. **Run the test in the window.** Click the **scroll** button (Load
    Script) and choose `CreeperAlarm.tst`. The script appears on the
    right. Set **Animate** to **No animation**, then click the **double
    arrow** (Run). **They should see:** `End of script - Comparison ended
    successfully` in the bar at the bottom. Close the window.

    **Say:** "The window is for exploring and finding mistakes. The
    terminal is quicker for testing. Use whichever helps."

11. **Now on your own: the voting machine.** Remember Lesson 4.14's
    voting machine? `cat Vote.hdl`. Read the comment, draw it on paper,
    write the parts, and test with `hardware Vote.tst` until it passes.
    *(Guide: three ANDs and two ORs. If stuck, ask "how many ANDs does
    the formula have?", then "how can two ORs join three wires?")*

12. **Save your work.**
    ```
    cd ~/lab/n2t
    git add practice
    git commit -m "My first two chips: CreeperAlarm and Vote"
    ```

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `hardware: command not found` | The link isn't in `~/bin`, or the terminal is old | Check `ls -l ~/bin`. Open a new terminal. |
| `ln: failed to create symbolic link ... File exists` | The link was made before | That's fine: it's already there. |
| `In HDL file ..., Line 8, Missing ';'` | A part line has no `;` at the end | The line *before* the one named often lacks it. |
| `Chip and is not found in the working and built in folders` | A chip name with the wrong capitals | Chip names start with a capital: `And`, `Not`, `Or`. |
| `In HDL file ..., c is not a pin in And` | A pin name that chip doesn't have | And has pins `a`, `b` and `out`. Not has `in` and `out`. The [HDL card](../../labs/n2t/HDL-CARD.md) lists them. |
| `Chip name doesn't match the HDL name` | The name after `CHIP` isn't the file's name | They must match exactly, capitals too. |
| `Comparison failure at line 8` | The chip runs, but gives a wrong answer | `diff` the `.out` and `.cmp` files to see which row. |
| `An internal pin may only be fed once by a part's output pin` | Two parts both write to the same wire | Each wire can have only one part driving it. Give one a new name. |
| `Can't connect gate's output pin to part` | An output pin (like `alarm`) is used as an input to another part | Make an internal pin for the inside, and use it. |
| `/home/.../X.tst doesn't exist` | Wrong name, or wrong folder | `ls` to check; run the test from the chip's own folder. |

## Talk about it

- What are the three files for each chip?
- What's an internal pin? Why does it need a name?
- How is writing a chip like writing a program? How is it different?
  *(All the parts work at the same time; the order of lines doesn't
  matter.)*

## Challenge *(if there's time, or for next time)*

- The order of the parts doesn't matter in HDL. Swap the lines of
  `CreeperAlarm` around and test it. Does it still pass? Why?
- Make your own practice chip with your own test: copy `Vote.tst`, and
  change it for a chip with a different rule. (The `.cmp` file you write
  by hand, very carefully, from the truth table.)

## Checkpoint

The learner can, without help:
- [ ] Explain what `CHIP`, `IN`, `OUT` and `PARTS` mean
- [ ] Write a chip from a formula, naming internal pins
- [ ] Run a test in the terminal and in the simulator, and read the result
- [ ] Use `diff` to find the row a chip gets wrong

## Lab notebook

Draw CreeperAlarm and Vote as gate diagrams, with every wire named as in
the HDL. Commit `~/lab/n2t`. Add *HDL*, *chip*, *pin*, *part*, *internal
pin* and *test script* to `dictionary.md`.

## Guide's background *(optional reading)*

**Nand to Tetris** (Noam Nisan and Shimon Schocken) is a famous course
in which you build a computer from NAND gates, then a language, a
compiler and an operating system for it. This stage covers the
hardware half (the book's Projects 1 to 6); Stage 8 does the software
half. The book, *The Elements of Computing Systems*, is an optional
purchase; everything the lessons need is in the project files, the
lessons, and the course's own [Hack card](../../labs/n2t/HACK-CARD.md)
and [HDL card](../../labs/n2t/HDL-CARD.md).

HDL describes **wiring**, not steps: every part works at once, like real
circuits, which is why the order of the lines doesn't matter. In the
practice folder, the simulator uses its own **built-in** And, Or and
Not. In the project folders, as soon as the learner writes `Not.hdl`,
any chip in that folder that uses Not uses *theirs*. That's what makes
it really their computer, and it's why chips must be built in order.

The authors ask that solutions to the projects aren't published. This
course follows that: lessons give designs, hints and tests, never the
finished HDL. The tests tell you whether a chip is right, so you never
need an answer key.
