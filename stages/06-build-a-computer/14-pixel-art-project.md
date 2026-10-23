# Lesson 6.14: Project: Pixel Art on My Computer (Stage 6 Checkpoint)

**Time:** 3–4 sessions of 45 min, plus the checkpoint on a separate day ·
**You need:** a terminal; Thonny; `~/lab/n2t`; squared paper; the Hack
card; Stage 3's Sprite Maker pictures, if they're still in
`~/lab/sprite-maker`; an audience for demo day · **New words:** code
generator, bit pattern

## Goal *(read this to the learner)*

> In Stage 3, you drew pixel art as letters in a text file, and Sprite
> Maker turned it into pictures for your games. Now you'll write a
> program that turns the same kind of text file into **Hack assembly**
> that draws the picture on your computer's screen. A program that
> writes programs! Then you'll assemble it with your own assembler, and
> run it. Finish it, pass the checkpoint, and you become a **Computer
> Builder**.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Agree a **demo day** with the learner, about two weeks away, and
      invite an audience.

## The rules for the project

The program, `~/lab/n2t/art/hackart.py`, must:
1. Read a picture file: one line per row of pixels, `k` for black and
   anything else for white. Lines starting with `#` are notes, and are
   skipped (just like Sprite Maker).
2. Write a `.asm` file that draws the picture on the Hack screen,
   somewhere away from the top-left corner.
3. Work for pictures wider than 16 pixels, including ones with black
   pixels at the right-hand edge of a word (see "the big number
   problem" below).
4. Its `.asm` must go through **your** assembler from Lesson 6.13, and
   run in the CPU Emulator.
5. Draw at least one picture of the learner's own, at least 32 pixels
   wide and 16 tall.

## Activity

### Session 1: one row, by hand

1. **The example picture.**
   ```
   mkdir -p ~/lab/n2t/art
   cd ~/lab/n2t/art
   cp ../practice/creeper16.txt .
   cat creeper16.txt
   ```
   **They should see:** a 16 by 16 creeper face made of `k`s and dots.

2. **One row into one number.** Take row 3: `..kkkk....kkkk..`. **Say:**
   "One row of 16 pixels is one word of screen memory. Remember: bit 0
   is the *leftmost* pixel. So pixel number `i`, counting from 0 on the
   left, is worth 2 to the power `i`."

   On squared paper, number the 16 pixels 0 to 15 and add up the values
   of the black ones: 4 + 8 + 16 + 32 + 1024 + 2048 + 4096 + 8192.
   *(15420.)*

3. **Draw it by hand.** Which address? **Say:** "Let's put the picture's
   top-left at screen row 112, word 15: about the middle of the screen.
   Row 3 of the picture is screen row 115. The address is
   `SCREEN + 32 × row + word`." *(16384 + 32 × 115 + 15 = 20079.)* Write
   the four instructions together:
   ```
   @15420
   D=A
   @20079
   M=D
   ```
   Put them in `test.asm` with the `(END)` loop after, and run it in the
   CPU Emulator. **They should see:** two short black bars in the middle
   of the screen: one row of the creeper's eyes.

### Sessions 2 and 3: the generator

4. **Plan it.** **Say:** "Now teach Python to do what we just did, for
   every row." Write the plan in Python-ish words together:
   ```
   read the picture's rows (skip notes and blank lines)
   for each row number r:
       for each 16-pixel piece w of the row:
           work out the piece's number
           if it's 0, skip it (the screen starts white)
           work out the address
           write the four instructions
   write the (END) loop
   ```
   Hints for the parts:
   - Reading: like the assembler's stage 1, and like Sprite Maker.
   - "How do you get the 16 pixels of piece `w`?" *(A slice:
     `row[16 * w:16 * w + 16]`.)*
   - Rows that aren't a multiple of 16 long: add dots to the end until
     they are (`while len(row) % 16 != 0:`).
   - The number: `for i, ch in enumerate(piece):`, adding `2 ** i` for
     each `k`.

5. **Test it.**
   ```
   python3 hackart.py creeper16.txt
   python3 ../projects/6/assembler.py creeper16.asm
   ```
   Load `creeper16.hack` (made by *your* assembler) in the CPU
   Emulator, **No animation**, Run. **They should see:** the creeper's
   face. Commit.

6. **The big number problem.** Make a test picture with a black pixel at
   the right-hand end of a word:
   ```
   # edge test
   kkkkkkkkkkkkkkkk
   ...............k
   ```
   Run `hackart.py` on it, then the assembler, then the emulator. **They
   should see:** neither row appears, and there's no error message. The
   first row's number is 65535, and the second is 32768. Look at the
   first line of the `.hack` file: `1111111111111111`. **Say:** "An
   A-instruction must start with a 0, so `@` can only hold 15 bits: up to
   32767. A bigger number turns into something that looks like a
   C-instruction, and the computer does something else entirely."

   **Say:** "Here's a trick. For a number that's too big, flip it first.
   65535 flipped is 0, which fits. Load that, and let the ALU flip it
   back." The Hack card's comp table has `!A`:
   ```
   @0
   D=!A        // D = 65535, which is -1: all sixteen pixels
   ```
   *(Guide: for a big number `v`, the flipped number is `65535 - v`.)* Add
   it to `hackart.py`, and check the edge test draws a full row, and one
   pixel at the right on the row below.

### Session 4: your own picture, and demo day

7. **Your own art.** Draw a picture at least 32 pixels wide and 16 tall:
   on squared paper first, then in a text file. Ideas: a Numberblock, a
   pickaxe, your initials, a Minecraft block, a spaceship. Or use a
   Sprite Maker picture from Stage 3 (`k` is already black). Make it,
   assemble it, run it. Commit.

8. **Demo day.** The learner shows the audience:
   - a picture file, and the same picture on the Hack screen;
   - how one row becomes one number (on paper);
   - the generator, the assembler and the emulator, one after another;
   - the big number problem and the `!A` trick;
   - the whole journey, with the passport: NAND, gates, ALU, memory, CPU,
     assembler, and now pictures.

## The Stage 6 checkpoint

On a separate day, without help (they may use the Hack card, the HDL
card, the lab notebook, and `dictionary.md`). Answers for the guide are
in brackets.

1. **HDL.** In `~/lab/n2t/practice`, build `Same.hdl`: `out` is 1 when
   `a` and `b` are the same. Pass `hardware Same.tst`. *(An Xor and a
   Not, or other designs.)*
2. **Negative numbers.** Write −6 in 8-bit two's complement *(11111010)*.
   What is `1111111111111110` in 16 bits? *(−2.)*
3. **Choosing and remembering.** Explain a Mux and a DMux. Draw RAM8
   from memory: the DMux8Way, eight registers, and the Mux8Way16.
4. **The ALU.** Find the control bits for `D-1` on the Hack card, and
   check them with the Python ALU from Lesson 6.7, with `x` = 5. *(001110,
   and the answer is 4.)*
5. **Machine language.** In `~/lab/n2t/practice`, write `Squares.asm`,
   which puts `R0 × R0` into `R1`. Pass `cpu Squares.tst`.
6. **Translation.** By hand, translate `@100`, `M=D+1` and `D;JLE` into
   binary. *(`0000000001100100`, `1110011111001000`,
   `1110001100000110`.)* Check with your assembler.
7. **The computer.** Explain the fetch-execute cycle, and what happens
   inside the CPU for `D=D+M`: where `D` and `M` come from, which bits
   go to the ALU, and where the answer goes.

All done means **Computer Builder!** Sign and stamp the passport.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| The picture is back to front | Pixel numbers counted from the right | Bit 0 is the **leftmost** pixel: `enumerate` from the left gives that. |
| The picture is stretched sideways or squashed | The address uses the wrong row width | Each screen row is 32 words: `SCREEN + 32 * row + word`. |
| Some pieces of the picture are missing, with no error | Their numbers are 32768 or more: they don't fit in `@` | That's the big number problem: use `65535 - v` and `D=!A`. |
| Part of a row is missing | Rows weren't padded to a multiple of 16 | Add dots until `len(row) % 16 == 0`. |
| Nothing appears | **View** isn't set to **Screen**, or the picture is drawn off the screen | Check the addresses are between 16384 and 24575. |
| `KeyError: '!A'` from your own assembler | `!A` is missing from your comp dictionary | Add it from the Hack card. |

## Talk about it

- Why is the leftmost pixel bit 0?
- Why can't `@` hold a number bigger than 32767?
- Your program wrote a program. What else could a program write?

## Checkpoint

The learner can, without help:
- [ ] Turn a row of pixels into a number, and a number into an address
- [ ] Write a Python program that writes Hack assembly
- [ ] Explain and use the `!A` trick for big numbers
- [ ] Pass the Stage 6 checkpoint above

## Lab notebook

Glue in the squared-paper drawing, and the row worked out by hand. Write
"The thing I'm proudest of in Stage 6 is..." and "If I built it again I
would...". Commit. Add *code generator* and *bit pattern* to
`dictionary.md`.

## Guide's background *(optional reading)*

A program that writes another program is a **code generator**, and
it's exactly what the back end of a compiler does. In Stage 8, the
learner writes a compiler for a whole language, which generates Hack
assembly in the same way.

The "big number problem" is a real constraint of the Hack design:
A-instructions spend one bit saying "I'm an A-instruction", leaving 15
for the value. Real processors have the same kind of limit, with the
same kinds of tricks (load in pieces, or load the complement and flip
it).

After this stage, the learner has built a working computer from NAND
gates, and written an assembler for it. Stage 7 steps back to study
algorithms and data structures, with the math that goes with them;
Stage 8 comes back to this computer and climbs the software half of
Nand to Tetris: a virtual machine, a compiler and an operating system.
