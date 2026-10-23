# Lesson 6.11: Pixels and Keys (Project 4)

**Time:** 3 sessions of 45 min · **You need:** a terminal; `~/lab/n2t`;
the Hack card; squared paper · **New words:** pixel, memory map,
pointer, keyboard code

## Goal *(read this to the learner)*

> The Hack computer has a screen and a keyboard, and your programs can
> use them. There's no special instruction for drawing: the screen is
> just part of memory. Put a 1 in the right box, and a pixel turns
> black. Today you'll draw on the screen, and then write the two Project
> 4 programs: one that multiplies, and one that paints the screen black
> while you hold down a key.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] `Sum.asm` should pass its test (Lesson 6.10).

## Warm-up (5 min)

"What does `@R1` then `M=D` do?" *(Stores D in `RAM[1]`.)* "How does a
loop start again?" *(A label, then `@LABEL` and `0;JMP` at the end.)*

## Activity

### Session 1: the screen is memory

1. **The memory map.** Read the "Screen and keyboard" part of the Hack
   card. **Say:** "The screen is 512 pixels across and 256 down. Each
   pixel is one bit. Starting at address 16384 (called `SCREEN`), the
   screen's bits are stored in RAM, 16 pixels to a word. Each row of the
   screen is 32 words. When the CPU writes to those addresses, the
   screen changes."

   On squared paper, draw the top-left corner: the first word is 16
   pixels; the next word along is `SCREEN + 1`; the word below the first
   is `SCREEN + 32`. **Say:** "In a word, bit 0 is the *leftmost* pixel:
   the opposite of how we write numbers. And `-1` is all sixteen bits on:
   sixteen black pixels."

2. **Draw by hand.** Open `cpu`, set **View** to **Screen** if it isn't
   already, and find address 16384 in the RAM table (scroll, or click the
   binoculars to search). Type `-1` into it. **They should see:** a short
   black line at the top-left of the screen. Type `-1` into 16416 (one
   row down). Try `1` in 16385. *(One pixel, at the left of the second
   word.)*

3. **Pointers.** **Say:** "To draw lots of rows, the program needs to
   remember *which* address it's at, in a variable, and then write to
   that address. `@addr` then `A=M` means: 'go to the address stored in
   `addr`'. A variable that holds an address is called a **pointer**."

4. **Block.** Type this as `~/lab/n2t/practice/Block.asm`:
   ```
   // Block: draws a 16 by 16 black square in the top-left corner.
       @16
       D=A
       @rows
       M=D         // rows = 16
       @SCREEN
       D=A
       @addr
       M=D         // addr = the address of the screen's first word
   (LOOP)
       @rows
       D=M
       @END
       D;JEQ       // if rows is 0, we're done
       @addr
       A=M
       M=-1        // 16 black pixels at addr
       @32
       D=A
       @addr
       M=D+M       // the next row down is 32 words further on
       @rows
       M=M-1       // rows = rows - 1
       @LOOP
       0;JMP
   (END)
       @END
       0;JMP
   ```
   Test it (`cpu Block.tst`), then load it in the CPU Emulator and Run
   with **No animation**. **They should see:** a black square in the
   corner. Commit.

5. **Play with it.** Change `@16` to `@100` (a tall bar). Change `@32` to
   `@33` (each row steps one word right: a staircase!). Put each back
   after.

### Session 2: Mult

6. **The keyboard, quickly.** In the CPU Emulator, click the keyboard
   button under the screen and hold a key. Find address 24576 (`KBD`) in
   the RAM table. **They should see:** the key's code while it's held
   (`A` is 65, space is 32), and 0 when it's let go.

7. **Project 4, Mult.** `cd ~/lab/n2t/projects/4/mult` and
   `cat Mult.asm`: multiply `R0` by `R1`, answer in `R2`. **Say:** "The
   Hack computer can't multiply. But 6 × 7 is just 7 added up 6 times,
   or 6 added up 7 times." Write the Python-ish version on paper first,
   like Sum's. Hints, one at a time:
   - "What should `R2` start at?" *(0. The test puts −1 there first, to
     check.)*
   - "How is this like Sum?" *(A loop that adds, and counts something
     down to 0.)*
   - "Should the program change `R0` or `R1`?" *(It may, but it's safer
     to count down a copy in a variable of its own, like `i`.)*

   Write it, test (`cpu Mult.tst`), commit. **They should see:**
   `Mult.out` with 0, 0, 0, 3, 8 and 42.

### Session 3: Fill

8. **Project 4, Fill.** `cd ../fill` and `cat Fill.asm`: when a key is
   pressed, the whole screen goes black; when no key is pressed, it goes
   white. Forever. Plan on paper, in Python-ish words. Hints:
   - "How does the program know whether a key is pressed?" *(`RAM[KBD]`
     is not 0.)*
   - "How many words is the whole screen?" *(256 rows × 32 words =
     8192.)*
   - "Block drew 16 rows of one word each. How can a loop like Block's
     do 8192 words, one after another?" *(The pointer moves on by 1 each
     time, not by 32.)*
   - "Black is −1. White is 0. Can the program choose the colour first,
     then use one loop for both?" *(Yes: store the colour in a variable.)*
   - "When the screen is done, what then?" *(Jump back to the start, and
     check the keyboard again.)*

9. **Try it, then test it.** Load `Fill.asm` in the CPU Emulator, set
   **No animation**, Run, click the keyboard button, and hold a key.
   **They should see:** the screen fill black from the top, and clear
   again when the key is let go. Then the automatic test:
   ```
   cpu FillAutomatic.tst
   ```
   It pretends to press and let go of a key, and checks the screen. When
   it passes, commit: `git commit -am "Project 4: Mult and Fill"`.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| Mult: `Comparison failure at line 2` | `R2` isn't set to 0 at the start | The test puts −1 in `R2` first. Start with `@R2` and `M=0`. |
| Mult works for small numbers but fails the last rows | The loop stops too soon or too late | Trace `R0` = 2, `R1` = 3 on paper, writing every variable at each jump. |
| Nothing appears on the screen | View isn't set to Screen, or the program writes to the wrong addresses | Set **View: Screen**. Check the addresses start at `SCREEN`. |
| Fill: the screen goes black but never white again | The colour variable is never set back to 0 | When no key is pressed, set the colour to 0 too. |
| Fill: very slow | Animation is on | Set **Animate** to **No animation**, and the speed slider to Fast. |
| `FillAutomatic` fails | The screen loop doesn't reach the end, or the program stops checking the keyboard | It must keep looping forever: after the last word, jump back to check the keyboard. |
| Fill draws past the screen, into the keyboard | The loop does one word too many | 8192 words: from `SCREEN` up to `SCREEN + 8191`. |

## Talk about it

- Why is the screen "just memory"?
- What's a pointer? Where did Block use one?
- How did you multiply without a multiply instruction?

## Challenge *(if there's time, or for next time)*

- Make Fill draw stripes instead of solid black: alternate rows of
  black and white.
- Make a program that draws a black square only while the `A` key is
  held. *(Compare `RAM[KBD]` with 65: `D=M`, then `@65`, `D=D-A`.)*
- How many instructions does Mult run for 6 × 7? Could a different
  order (counting down `R0` or `R1`) make it faster?

## Checkpoint

The learner can, without help:
- [ ] Explain how the screen and keyboard are part of memory
- [ ] Use a pointer with `A=M`
- [ ] Write Mult and Fill, with passing tests
- [ ] Find a bug by tracing a program on paper

## Lab notebook

Draw the screen's memory map with a few addresses labelled. Write Fill's
plan in Python-ish words. Commit. Add *pixel*, *memory map*, *pointer*
and *keyboard code* to `dictionary.md`. Tick
Project 4 on the passport's Nand to Tetris climb.

## Guide's background *(optional reading)*

Using ordinary memory addresses for devices is called **memory-mapped
I/O**, and real computers use it too: a graphics card's memory, and many
hardware devices, appear at addresses the CPU can read and write. It
means the CPU doesn't need any special instructions for input and output.

The Fill program is the learner's first **event loop**: check the input,
react, repeat forever. Every game, and every program with a window,
works that way. A PLC's scan cycle is the same idea: read inputs, run
the logic, write outputs, repeat.
