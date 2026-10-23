# Lesson 8.6: The Stack Machine

**Time:** 2 sessions of 45 min · **You need:** a terminal; `~/lab/n2t`;
the VM card and the Hack card; a pack of playing cards (or numbered
sticky notes) · **New words:** virtual machine, stack, push, pop, stack
pointer, VM code

## Goal *(read this to the learner)*

> In Stage 6 you built a computer, and it only speaks Hack. Writing a
> whole game in Hack would take for ever. So the second half of Nand to
> Tetris builds a ladder of languages on top: first a simple language
> for an imaginary computer, a **virtual machine**, which works with a
> pile of numbers called a **stack**. Then a real language, Jack, which
> turns into VM code. Then an operating system, and a game. Today you'll
> learn the stack machine with cards, and run its code in the VM
> Emulator.

## Before the lesson *(guide, 15 min)*

- [ ] Read this whole lesson once, and the note on solutions in the
      [stage's README](README.md).
- [ ] From your own account: `./scripts/give-lab.sh LEARNER stack`. It
      puts the Stage 8 test scripts, compiler tests and an example game
      in `~/lab/n2t/stack/`. (The Nand to Tetris projects for this stage
      are already in `~/lab/n2t/projects/`, from Lesson 6.1.)
- [ ] Print the [VM card](../../labs/n2t/VM-CARD.md) and the
      [Jack card](../../labs/n2t/JACK-CARD.md).

## Warm-up (5 min)

"In Hack, how would you work out 7 + 8 and put it in `RAM[0]`?" *(`@7`,
`D=A`, `@8`, `D=D+A`, `@0`, `M=D`.)* "How many instructions would a
whole game need?" *(Thousands! Pong was 27,483.)*

## Activity

### Session 1: a pile of cards

1. **The ladder.** Draw it on paper, bottom to top:
   ```
   Diamond Dash (a game)          Lesson 8.12
   Jack (the language)            Lessons 8.11 to 8.16
   VM code (the stack machine)    Lessons 8.6 to 8.10
   Hack assembly                  Lesson 6.10
   Hack machine code              Lesson 6.13
   the Hack computer              Lessons 6.1 to 6.12
   NAND gates
   ```
   **Say:** "We're going to climb from the middle to the top. Each rung
   is translated into the one below it by a program. You already wrote
   the assembler. In this stage you'll write the **VM translator** (VM
   code into Hack assembly) and the **compiler** (Jack into VM code).
   Then the whole ladder will be yours."

2. **A stack of cards.** **Say:** "A **stack** is a pile. You can only
   put a card on top (**push**), or take the top card off (**pop**). Like
   the stacks in Lesson 7.10." Play the stack machine with real cards,
   the learner being the computer. The guide reads each command:
   ```
   push constant 7
   push constant 8
   add
   ```
   For `add`: take off the top two cards, add them, and push a card with
   the answer. **They should see:** one card, 15.

3. **More commands.** Use the VM card's table. Play these, one at a time:
   ```
   push constant 10
   push constant 3
   sub
   ```
   *(7. The top card, 3, is taken away from the one under it.)*
   ```
   push constant 5
   push constant 5
   eq
   ```
   *(−1, which means true.)* **Say:** "On this machine, true is −1: all
   16 bits are 1. False is 0." Then `push constant 3`, `push constant 9`,
   `gt` *(0, false: 3 isn't greater than 9)*.

4. **Expressions into VM code.** **Say:** "To work out `10 - (3 + 4)`,
   push what you need, and do each sum when its two numbers are on top."
   Work it out together:
   ```
   push constant 10
   push constant 3
   push constant 4
   add
   sub
   ```
   Play it with cards. *(3.)* Now the learner writes VM code for these on
   paper, then plays them:
   - `(2 + 3) - 1` *(push 2, push 3, add, push 1, sub: 4)*
   - `20 - (6 - 1)` *(push 20, push 6, push 1, sub, sub: 15)*
   - Is `7 + 1` equal to `8`? *(push 7, push 1, add, push 8, eq: −1)*

   **Say:** "Notice that we never need to name a place to keep a number.
   The stack keeps everything in order. That's why it's so easy to
   translate other languages into it."

### Session 2: the VM Emulator

5. **The tools.** Make links to two more Nand to Tetris tools, and the
   course's test scripts, in `~/bin`:
   ```
   ln -s /srv/redstone-library/tools/nand2tetris/tools/VMEmulator.sh ~/bin/vme
   ln -s /srv/redstone-library/tools/nand2tetris/tools/JackCompiler.sh ~/bin/jackc
   ln -s ~/lab/n2t/stack/check-* ~/bin/
   ls ~/bin
   ```
   **They should see:** `vme`, `jackc`, `check-vm`, `check-xml`,
   `check-jack` and `check-os` among the older links.

6. **Step through a program.** Open `vme`. Click **Load Program** (the
   folder button at the top left) and choose
   `~/lab/n2t/projects/7/StackArithmetic/SimpleAdd/SimpleAdd.vm`.
   **They should see:** three lines in the Program box: `push constant
   7`, `push constant 8`, `add`.

   Click the single blue arrow (**Single Step**) once, and look at the
   **Stack** box and the **Global Stack** box. Click it twice more.
   **They should see:** the stack shows 7, then 7 and 8, then just 15.
   In the RAM box, **SP** (`RAM[0]`) goes 256, 257, 258, 257.

   **Say:** "This is the stack, really in the RAM: it starts at address
   256. `SP`, the **stack pointer**, holds the address of the next free
   place, just above the top." **Ask:** "Look at address 257 in the Global
   Stack. Why is the 8 still there?" *(Pop doesn't wipe a number out. It
   just moves SP down, so the 8 is above the top now, and will be written
   over by the next push.)*

7. **Your own VM program.** In Thonny, make
   `~/lab/n2t/projects/7/mine/Mine.vm` (make the `mine` folder first):
   ```
   // 10 - (3 + 4), then is it equal to 3?
   push constant 10
   push constant 3
   push constant 4
   add
   sub
   push constant 3
   eq
   ```
   Load it in `vme`, and step through it. **They should see:** 10, 3, 4,
   then 10 and 7, then 3, then 3 and 3, then −1. Commit.

   Now the learner writes VM programs for the three paper expressions
   from step 4, as `Mine2.vm` and so on, and checks each answer in the
   emulator.

8. **Looking ahead.** **Say:** "The VM Emulator pretends to be a stack
   machine. But your Hack computer doesn't have a stack: it only has A,
   D and M. Next lesson, you'll write a program that turns every VM
   command into Hack assembly, so these programs can run on your real
   computer."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `vme: command not found` | The link is missing, or the terminal is old | `ls -l ~/bin`, and open a new terminal. |
| The emulator says it can't find the folder `stack` | `give-lab.sh LEARNER stack` hasn't been run | The guide runs it. |
| `Mine.vm: in line 2: unknown instruction - Push`, when loading | A typo on that line of the `.vm` file (counting from 1) | Check the spelling against the VM card: `push constant 7`, all lowercase. |
| The stack box shows nothing | Nothing has run yet | Click Single Step. |
| `sub` gives the wrong sign | The order: it's (the one under) minus (the top) | Push the first number first. |

## Talk about it

- What's a stack? What do push and pop do?
- What does SP hold? Why does it point *above* the top?
- Why is true −1 and not 1?
- Why is VM code easy to translate other languages into?

## Challenge *(if there's time, or for next time)*

- Write VM code for `(1 + 2) - (3 - 4)`, then check it. *(4.)*
- What do `push constant 12`, `push constant 10`, `and` give? Work it
  out in binary first. *(8: 1100 and 1010 is 1000.)*
- `neg` and `not` take only one number. What's the difference between
  them on `push constant 5`? *(−5, and −6: `not` flips every bit, and
  two's complement adds 1 as well.)*

## Checkpoint

The learner can, without help:
- [ ] Play the stack machine with cards, for every arithmetic command
- [ ] Turn an expression with brackets into VM code
- [ ] Step through a VM program in the emulator, and explain SP
- [ ] Explain the ladder of languages, and which rungs they'll write

## Lab notebook

Draw the ladder. Write the VM code for three expressions, with the
stack drawn after each line. Commit. Add *virtual machine*, *stack*,
*push*, *pop* and *stack pointer* to `dictionary.md`.

## Guide's background *(optional reading)*

This is the start of Nand to Tetris Part 2 (Projects 7 to 12), from
*The Elements of Computing Systems* by Nisan and Schocken. Their
compiler works in two stages, as Java's and C#'s do: Jack is compiled
into code for a **virtual machine** (an imaginary computer with a
stack), and the VM code is then translated into Hack assembly. The VM
is simple to compile *into* (expressions become push-push-operate), and
simple to translate *from* (each VM command becomes a few lines of
assembly). The same idea lets Java run on any computer that has a Java
VM.

A stack machine works out expressions in **postfix** (Reverse Polish)
order: operands first, then the operation. Old HP calculators worked
this way. In the VM, `SP` lives at `RAM[0]` and the stack grows upward
from address 256; popping just moves `SP` down, so old values stay in
memory until something overwrites them.

The VM Emulator runs VM code directly, so it's the "reference" for what
the learner's translator must do on the CPU Emulator.
