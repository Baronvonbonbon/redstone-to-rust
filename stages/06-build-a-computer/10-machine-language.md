# Lesson 6.10: Speaking Machine Language

**Time:** 3 sessions of 45 min · **You need:** a terminal; `~/lab/n2t`;
the [Hack card](../../labs/n2t/HACK-CARD.md), printed · **New words:**
machine language, instruction, assembly, A-instruction, C-instruction,
label, jump

## Goal *(read this to the learner)*

> You've built the parts of a computer: an ALU that works things out,
> registers and RAM that remember, and a counter that keeps its place.
> Before putting them together, you need to know what the computer will
> *do*: run **machine language**, the simplest language there is. Every
> program you've ever used, Minecraft included, ends up as instructions
> like these. Today you'll read them, step through them one at a time,
> and write your first program in the Hack computer's own language.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once, with the Hack card next to it.
- [ ] Print the Hack card for the learner.

## Warm-up (5 min)

"What does a register do?" *(Remembers one number.)* "What's an
address?" *(The number of a box in memory.)* "What does the program
counter hold?" *(The number of the next instruction.)*

## Activity

### Session 1: A, D and M

1. **Three registers.** Read the top of the Hack card together. **Say:**
   "The Hack computer has two registers you can use: **D**, for working
   things out, and **A**, for addresses. And there's **M**, which isn't a
   register: it's whatever box in RAM that A is pointing at. If A is 5, M
   is `RAM[5]`."

2. **Two kinds of instruction.**
   - **A-instruction:** `@` and a number. `@7` puts 7 in A. That's all it
     does.
   - **C-instruction:** works something out with the ALU, and stores it.
     `D=A` copies A into D. `M=D+1` puts D + 1 into the box A points at.

   **Say:** "Every C-instruction is `dest=comp`: work out *comp*, store it
   in *dest*. The comp table on the card is exactly your ALU's table from
   Lesson 6.7!"

3. **Read a program.**
   ```
   cd ~/lab/n2t/projects/6/add
   cat Add.asm
   ```
   Go through it line by line, writing A, D and `RAM[0]` on paper after
   each one:

   | Instruction | A | D | RAM[0] |
   |---|---|---|---|
   | `@2` | 2 | 0 | 0 |
   | `D=A` | 2 | 2 | 0 |
   | `@3` | 3 | 2 | 0 |
   | `D=D+A` | 3 | 5 | 0 |
   | `@0` | 0 | 5 | 0 |
   | `M=D` | 0 | 5 | 5 |

   **Say:** "Six instructions to add 2 and 3. Machine language does tiny
   steps, but very, very fast."

4. **Step through it in the CPU Emulator.** `cpu` opens the CPU
   Emulator. Click the first button (the folder, **Load Program**) and
   choose `projects/6/add/Add.asm`. **They should see:** the program in
   the **ROM** on the left, RAM next to it, and the **A**, **D** and
   **PC** registers.

   Click the **single arrow** (Single Step) once per instruction, and
   watch A, D, PC and `RAM[0]` change exactly like the paper table.
   **Say:** "Watch PC: it counts 0, 1, 2... That's your program counter,
   moving to the next instruction."

### Session 2: jumps and labels

5. **Jumping.** **Say:** "So far the program only goes forwards. To make
   decisions and loops, it needs to **jump**: to set PC to a different
   instruction." Read the jump table on the Hack card. A jump is always
   two instructions:
   ```
   @END       // A = where to jump to
   D;JEQ      // jump there if D is 0
   ```
   **Say:** "`@` sets the address, then the C-instruction says *when* to
   jump. `0;JMP` means 'always jump'."

6. **Labels.** **Say:** "Counting instruction numbers is fiddly. Instead,
   you write a **label** in brackets, like `(END)`, and `@END` means 'the
   address of that label'. Labels aren't instructions: they just name a
   place."

7. **Read Max.** `cat ../max/Max.asm`. Ask: "What does it do?" Work
   through it with `R0` = 7 and `R1` = 4, on paper. *(It puts the bigger
   of `R0` and `R1` into `R2`. `D=D-M` works out R0 − R1; if that's more
   than 0, R0 is bigger.)* Then load it in the CPU Emulator, set `RAM[0]`
   to 7 and `RAM[1]` to 4 (double-click the value in the RAM table, type,
   press Enter), and Run (double arrow) with **Animate** on **No
   animation**. Click stop after a second. **They should see:** `RAM[2]`
   is 7.

   **Say:** "Look at the end: `(END) @END 0;JMP`. It jumps to itself
   forever. A Hack program can't stop, so it waits there."

### Session 3: your first program

8. **Sum.** The program adds up 1 + 2 + ... + n, for n in `R0`, and puts
   the answer in `R1`. Write the idea in Python-ish words first:
   ```
   R1 = 0
   while R0 is not 0:
       R1 = R1 + R0
       R0 = R0 - 1
   ```
   Then type the Hack version, in `~/lab/n2t/practice/Sum.asm`
   (`nano Sum.asm` in the practice folder):
   ```
   // Sum: adds up 1 + 2 + ... + R0, and puts the answer in R1.
       @R1
       M=0         // R1 = 0
   (LOOP)
       @R0
       D=M         // D = R0
       @END
       D;JEQ       // if D is 0, jump to END
       @R1
       M=D+M       // R1 = R1 + D
       @R0
       M=M-1       // R0 = R0 - 1
       @LOOP
       0;JMP       // go back to LOOP
   (END)
       @END
       0;JMP       // stay here forever
   ```
   Match each Python-ish line to its Hack lines.

9. **Test it.**
   ```
   cpu Sum.tst
   ```
   **They should see:** `End of script - Comparison ended successfully`.
   `cat Sum.out` shows the answers: 0, 1, 10 and 5050.

   **Say:** "5050 is 1 + 2 + ... + 100. There's a famous story that a
   schoolboy called Gauss worked that out in his head, by pairing 1 with
   100, 2 with 99, and so on: 50 pairs of 101." Commit `Sum.asm`.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `In line 4, Destination expected` (or `Expression expected`) | A typo on that line, like lowercase `d=m` or a comp that's not on the card | The CPU Emulator counts lines from **0**, so "line 4" is the fifth line. Check it against the Hack card. |
| `Comparison failure at line 2` | The program runs, but gets the wrong answer | Step through it in the window with a small number, like `R0` = 3, and compare with paper. |
| The program never stops in the window | It's in the `(END)` loop: that's normal | Click stop. The answer is already in RAM. |
| A jump goes to the wrong place | A label is spelled differently in `@LOOP` and `(LOOP)` | A misspelled `@` name doesn't cause an error: it becomes a new variable. Check spellings carefully. |
| `/home/.../Sum.tst doesn't exist` | Running the test in the wrong folder | `cd ~/lab/n2t/practice` first. |

## Talk about it

- What's the difference between A, D and M?
- What are the two kinds of instruction?
- How does a loop work in machine language?
- Why does every program end with a loop that goes nowhere?

## Challenge *(if there's time, or for next time)*

- Write `Double.asm`: put 2 × `R0` into `R1`. *(No multiply: what's
  `D+M` when D and M are the same?)*
- Change Sum to add only the even numbers.
- Work out on paper how many instructions Sum runs for `R0` = 100.

## Checkpoint

The learner can, without help:
- [ ] Explain A, D, M, and the two kinds of instruction
- [ ] Trace a short program on paper, writing A, D and RAM after each step
- [ ] Step through a program in the CPU Emulator
- [ ] Write a loop with a label and a jump, and test it

## Lab notebook

Copy the Add trace table. Write Sum with the Python-ish version next to
it. Commit. Add *machine language*, *instruction*, *assembly*,
*A-instruction*, *C-instruction*, *label* and *jump* to `dictionary.md`.

## Guide's background *(optional reading)*

Hack programs are written in **assembly language**, a readable form of
machine language: each line is one instruction. The real machine
language is binary (the card shows the bit patterns), and in Lesson 6.13
the learner writes the **assembler** that translates one into the other.
The CPU Emulator can load assembly directly, because it has an assembler
built in.

Hack is deliberately tiny: two registers, two instruction types, and
no multiply, divide, or call instructions. Everything else is built in
software, which is what Stage 8 is about. Real processors have hundreds
of instructions, but the ideas of registers, memory addresses and jumps
are exactly the same.
