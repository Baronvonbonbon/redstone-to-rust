# Lesson 6.12: The CPU and the Computer (Project 5)

**Time:** 4–5 sessions of 45 min · **You need:** a terminal; `~/lab/n2t`;
the Hack card and the HDL card; big paper and coloured pencils ·
**New words:** CPU, decode, fetch-execute cycle, ROM

## Goal *(read this to the learner)*

> This is it: the top of the hardware. You'll connect your ALU,
> registers and program counter into a **CPU**, the central processing
> unit that reads instructions and carries them out. Then you'll join
> the CPU, the memory, the screen and the keyboard into the **Computer**,
> and it will run real programs, on chips you built from NAND gates.

## Before the lesson *(guide, 15 min)*

- [ ] Read this whole lesson once. It's the hardest of the stage: plan
      for several sessions, and expect the CPU to take a few tries.
- [ ] Projects 1 to 4 should be finished.
- [ ] Know that `Memory.tst` must be run **in the simulator's window**,
      not the terminal: it waits for someone to press keys on the
      simulator's keyboard. (In the terminal it waits forever; Ctrl+C
      stops it.)

## Warm-up (5 min)

"What are the two kinds of Hack instruction?" *(A and C.)* "In
`D=D+M;JGT`, which part is dest, which is comp, and which is jump?" *(D,
D+M, JGT.)* "What does the program counter do on a jump?" *(Loads the
address in A.)*

## Activity

### Session 1: the Memory chip

1. **Three things in one.** `cd ~/lab/n2t/projects/5` and
   `cat Memory.hdl`. **Say:** "Memory is your RAM16K, the screen and the
   keyboard, joined into one big address space, like the Hack card's
   memory map." Write the addresses in binary (15 bits):

   | Addresses | Starts with | Is |
   |---|---|---|
   | 0–16383 | `0` | RAM16K |
   | 16384–24575 | `10` | Screen |
   | 24576 | `11` | Keyboard |

   **Say:** "The left two address bits, `address[14]` and `address[13]`,
   say which device. The rest say where inside it." Hints, one at a time:
   - "Which chip sends `load` to only one place?" *(A DMux. With two
     choosing bits, a DMux4Way: two of its outputs both mean RAM.)*
   - "Which chip picks which device's `out` comes out?" *(A Mux4Way16.)*
   - "How many address bits does the Screen need?" *(13: see the HDL
     card.)*
   - "Does the Keyboard need `load` or an address?" *(No: it only has an
     output.)*

2. **Test it in the window.** Open `hardware`, Load Chip `Memory.hdl`, and
   Load Script `Memory.tst`. Loading the script switches the right side to
   show the script, so now set **View** to **Screen** (the screen and a
   keyboard button appear), and **Animate** to **No animation**. Run. The
   script stops and asks you, in the bar at the bottom, to click the
   keyboard and hold **K** (capital). Click the keyboard button under the
   screen and hold Shift+K until the message changes. Then it asks for
   **Y** the same way. **They should see:** two short lines in the middle
   of the screen, and `End of script - Comparison ended successfully`.
   Commit.

### Sessions 2 and 3: the CPU

3. **What the CPU does.** **Say:** "The CPU gets one instruction at a
   time from the program, and does it. To do that, it has to **decode**
   the instruction: look at its bits and work out what each one asks
   for." Lay out the bits of a C-instruction from the Hack card on big
   paper:
   ```
   bit:   15  14 13  12  11 10  9  8  7  6   5  4  3   2  1  0
          1   1  1   a   c1 c2 c3 c4 c5 c6  d1 d2 d3  j1 j2 j3
   ```
   An A-instruction has bit 15 = 0, and the other 15 bits are the number.

4. **Draw the CPU.** On the big paper, draw these boxes and connect them
   as the jobs below say, one colour per job:
   ```
                      instruction
                           |
        +------------------+-----------------+
        |                                    |
     [ Mux16 ]<---- ALU output          control bits
        |                                    |
   [ A register ]---> addressM               v
        |   |                    [ D register ]--x-->[      ]
        |   +----> [ Mux16 ]-----------------y------>[ ALU  ]---> outM
        |            ^                               [      ]
        |           inM                               zr, ng
        v                                               |
     [ PC ] <---- jump? <-------------------------------+
        |
        +---> pc
   ```
   The jobs, one at a time. For each, ask the question, and draw the
   answer:
   - **A or C?** "Which bit says what kind of instruction it is?" *(Bit
     15: 0 for A, 1 for C.)*
   - **What goes into A?** "For an A-instruction, what goes into the A
     register?" *(The instruction itself.)* "For a C-instruction with A
     as a dest?" *(The ALU's output.)* So a Mux16 chooses.
   - **When does A load?** "For every A-instruction, and for a
     C-instruction whose d1 bit is 1."
   - **When does D load?** "For a C-instruction whose d2 bit is 1." D
     always gets the ALU's output.
   - **A or M?** "The ALU's `y` input is either A or M (`inM`). Which bit
     chooses?" *(The `a` bit, bit 12.)* The ALU's `x` input is always D.
   - **The ALU.** "Its six control bits are c1 to c6, bits 11 to 6, in
     order: zx, nx, zy, ny, f, no." Straight from the instruction!
   - **Writing to memory.** `outM` is the ALU's output. `writeM` is 1 for
     a C-instruction whose d3 bit is 1. `addressM` is A's lower 15 bits.
   - **Jumping.** "j1 means 'jump if negative', j2 'jump if zero', j3
     'jump if positive'. The ALU's `ng` and `zr` say what the answer was.
     How can you tell it's positive?" *(Not zero AND not negative.)* Jump
     if any of the three matches, and only for a C-instruction.
   - **The PC.** Its `in` is A. It loads when the jump happens, otherwise
     it counts up (`inc` can always be 1, since `load` wins). `reset` is
     the CPU's `reset`. `pc` is its lower 15 bits.

5. **Build it in pieces.** Write the parts for one job at a time,
   checking the drawing. Two important rules:
   - Use the built-in **ARegister** and **DRegister** chips (not
     Register) for A and D. They work the same, but the test looks
     inside them.
   - Remember the "Several outputs" trick from the HDL card, for wires
     like A's lower 15 bits.

6. **Test in two steps.** First the test that only checks the outputs:
   ```
   hardware CPU-external.tst
   ```
   Then the full test, which also checks inside the D register:
   ```
   hardware CPU.tst
   ```
   When a test fails, `diff CPU.out CPU.cmp` shows the row. The
   `instruction` column shows the instruction in binary: decode it with
   the Hack card, work out what *should* happen, and find the job that
   went wrong. Commit when both pass.

### Session 4: the Computer

7. **Three parts.** `cat Computer.hdl`. **Say:** "The Computer is a
   **ROM** that holds the program, your CPU, and your Memory. Connect
   them." Hints:
   - "What tells the ROM which instruction to give?" *(The CPU's `pc`.)*
   - "Where does the CPU's `inM` come from?" *(Memory's `out`.)*
   - "What tells Memory where and whether to write?" *(The CPU's
     `addressM`, `outM` and `writeM`.)*

   Build it (three parts), then run its tests:
   ```
   hardware ComputerAdd.tst
   hardware ComputerMax.tst
   hardware ComputerRect.tst
   ```
   Commit: `git commit -am "Project 5: my own computer runs programs"`.

8. **Watch your computer draw.** Open `hardware`, Load Chip `Computer.hdl`,
   Load Script `ComputerRect.tst`, then set **View** to **Screen**. Leave
   **Animate** on **Program flow**, move the speed slider to **Fast**, and
   Run. **They should see:** the instructions ticking through, and a small
   rectangle drawn at the top left of the screen, then `End of script -
   Comparison ended successfully`. **Say:** "That rectangle was drawn by a
   program, running on a CPU you built, using an ALU you built, using
   adders you built, using gates you built, from NAND. You've built a
   computer."

   Celebrate properly.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `hardware Memory.tst` in the terminal never finishes | It's waiting for key presses | Ctrl+C. Run it in the window (step 2). |
| In the window, the keyboard button isn't there | The right side is showing the script | Set **View** to **Screen** after loading the script. |
| Holding K does nothing | The keyboard button wasn't clicked first, or it's a lowercase k | Click the keyboard button, then hold **Shift**+K. |
| The window freezes or stops partway through a long test | The simulator's window sometimes struggles with fast runs | Close it. The terminal gives the same result: `hardware ComputerRect.tst`. |
| `No such built-in chip used: DRegister` | D is a plain Register | Use the built-in `DRegister` (and `ARegister` for A). |
| `CPU-external` passes but `CPU.tst` fails | Usually the D register loads at the wrong time | Check D loads only for a C-instruction with d2 = 1. |
| A row with an A-instruction fails | A-instructions are treated like C-instructions | Bit 15 decides. Every C-only job (D load, writeM, jump) must also check bit 15 is 1. |
| Jumps go wrong, or happen on A-instructions | The jump isn't limited to C-instructions, or "positive" is wrong | Positive is NOT zr AND NOT ng. |
| `writeM` is 1 on an A-instruction | The same: d3 must count only for C-instructions | AND it with bit 15. |
| `ComputerAdd` passes, `ComputerMax` fails | Jumps don't work yet (Add has no jumps) | Test the jump job: try `CPU.tst` rows with `JGT` in them. |
| `addressM(15) and ...(16)` width messages | A full 16-bit bus went into a 15-bit pin | Split A's output: `out[0..14]=addressM`. |

## Talk about it

- What does "decode" mean?
- Which bits of a C-instruction control the ALU? Where else have you
  seen those six bits?
- What does the Computer do, over and over, every clock beat?

## Challenge *(if there's time, or for next time)*

- In the window, load `Computer.hdl`, then the `ComputerMax.tst`
  script, and step through it slowly with **Program & data flow**
  animation. Watch the instruction, the registers and the PC change.
- How many NANDs are in your whole computer? Estimate it by counting
  (roughly) up from the chips: RAM16K is the big one.

## Checkpoint

The learner can, without help:
- [ ] Explain what each group of a C-instruction's bits does inside the CPU
- [ ] Build Memory, CPU and Computer, with every test passing
- [ ] Use a failing test row to find which part of the CPU is wrong
- [ ] Explain the fetch-execute cycle in their own words

## Lab notebook

Glue in the big CPU drawing. Write "My computer runs programs because..."
in their own words. Commit. Add *CPU*, *decode*, *fetch-execute cycle* and
*ROM* to `dictionary.md`. Tick Project 5 on the passport's Nand to Tetris
climb.

## Guide's background *(optional reading)*

Every clock beat, the Computer does one instruction: the ROM gives the
instruction at `pc` (**fetch**), and the CPU decodes it and does it
(**execute**): the ALU works something out, the answer goes to A, D or
memory, and the PC either counts up or jumps. That's the
**fetch-execute cycle**, and every CPU since the 1940s works this way,
just faster and with more instructions. A PLC's scan cycle is the same
loop at a bigger scale.

Hack keeps the program in a separate ROM from the data (a "Harvard
architecture"). Most real computers keep both in one memory, so a program
can load another program (a "von Neumann architecture"). Stage 8 builds a
virtual machine on top of Hack that works around this.

This lesson describes the CPU's design in words and questions, but not
its HDL, following the authors' request. The two tests make it possible
to check every part without an answer key.
