# Lesson 8.9: Loops and Jumps in the VM (Project 8)

**Time:** 2 sessions of 45 min · **You need:** a terminal; Thonny;
`~/lab/n2t`; the VM card and the Hack card · **New words:** program
flow, label, `goto`, `if-goto`

## Goal *(read this to the learner)*

> So far, VM programs run straight from top to bottom. Real programs
> need loops and choices. The VM has three commands for that: `label`
> marks a place, `goto` jumps to it, and `if-goto` jumps only if the
> top of the stack is true. Today you'll write a VM loop by hand, then
> teach your translator the three commands. It's a short step, because
> Hack already knows how to jump.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] All five Project 7 tests should pass (Lesson 8.8).

## Warm-up (5 min)

"In Hack, how do you jump to `(LOOP)`?" *(`@LOOP`, then `0;JMP`.)* "How
do you jump only if D isn't 0?" *(`@LOOP`, then `D;JNE`.)* "What's
true, in the VM?" *(−1. False is 0.)*

## Activity

### Session 1: a loop in VM code

1. **A new folder.** Project 8 grows the same translator, so copy it:
   ```
   cp ~/lab/n2t/projects/7/vm.py ~/lab/n2t/projects/8/vm.py
   cd ~/lab/n2t/projects/8
   ```
   **Say:** "From now on, `projects/8/vm.py` is the one we change."
   Commit.

2. **Read a loop.** In Thonny, make `~/lab/n2t/projects/8/mine/Sum.vm`:
   ```
   // Adds 1 + 2 + ... + 10, and leaves the answer in temp 0.
   push constant 0
   pop temp 0          // sum = 0
   push constant 10
   pop temp 1          // i = 10
   label LOOP
   push temp 1
   push constant 0
   eq
   if-goto DONE        // if i = 0, the loop is finished
   push temp 0
   push temp 1
   add
   pop temp 0          // sum = sum + i
   push temp 1
   push constant 1
   sub
   pop temp 1          // i = i - 1
   goto LOOP
   label DONE
   label END
   goto END            // stay here
   ```
   **Say:** "It's this Python, written for the stack machine:
   ```python
   sum = 0
   i = 10
   while i != 0:
       sum = sum + i
       i = i - 1
   ```
   `if-goto DONE` takes the top of the stack off. If it's true (not 0),
   it jumps to `DONE`. If not, it carries on to the next line."

3. **Run it in the VM Emulator.** Open `vme`, load `mine/Sum.vm`, set
   **Animate** to **Program flow**, and click Run (the double arrow).
   Watch the yellow line go round the loop. Stop it after a while.
   **They should see:** in the RAM box, `Temp0` (`RAM[5]`) ends at 55,
   and `Temp1` (`RAM[6]`) at 0.

   **Ask:** "Why does the program end with `goto END`?" *(Without it,
   the computer would carry on into whatever is after the program. Hack
   programs end the same way.)*

4. **Write your own.** The learner writes `mine/Times.vm`: 6 × 7, by
   adding 6 seven times, with the answer in `temp 0`. Plan it as Python
   first, on paper. Check it in `vme`. *(42.)* Commit.

### Session 2: the translator

5. **The three commands, on paper.** **Say:** "Each one becomes Hack
   you already know."
   - `label LOOP` becomes a Hack label: `(LOOP)`.
   - `goto LOOP` is an unconditional jump.
   - `if-goto LOOP` pops the top number into D, then jumps if D isn't 0.
     *(Hint: `pop_d()` and the card's jump table.)*

   Write the Hack for each on paper, then add them to `translate`.

6. **Test.**
   ```
   check-vm ProgramFlow/BasicLoop
   check-vm ProgramFlow/FibonacciSeries
   ```
   **They should see:** `ALL GOOD!` twice. **Say:** "FibonacciSeries
   writes the Fibonacci numbers, 0, 1, 1, 2, 3, 5, 8..., into the RAM,
   using a loop and the `that` segment as a pointer into an array."

7. **Your program, on your translator.**
   ```
   python3 vm.py mine/Sum.vm
   ```
   Load `mine/Sum.asm` in `cpu`. Click `RAM[0]` and type 256, set
   **Animate** to **No animation**, Run for a second or two, and Stop.
   **They should see:** `RAM[5]` is 55. **Say:** "Your loop, translated by
   your translator, running on the computer you built in Stage 6." Commit.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `I don't know how to translate ['label', 'LOOP']` | Not written yet | Add the three commands to `translate`. |
| The loop never stops | `if-goto` jumps on false, or doesn't pop | Jump when D is *not* 0 (`JNE`), after popping. |
| BasicLoop's row shows `RAM[0]` as 260 where it should be 257 | `if-goto` looks at the top without popping it, so the stack grows | Use `pop_d()` so SP goes down. |
| `Sum.asm` gives the wrong answer in `cpu`, but right in `vme` | `RAM[0]` wasn't set to 256 | Set it before running. |
| The CPU Emulator says a label is unknown | A typo, or a VM label with a space in it | Labels are one word. |

## Talk about it

- What do `label`, `goto` and `if-goto` do?
- Why does `if-goto` pop the stack?
- How is a VM `while` loop built out of these three commands?

## Challenge *(if there's time, or for next time)*

- Write `mine/Count.vm`: count how many of the numbers from 1 to 20
  divide by 3, using only subtraction. *(6.)*
- What does an `if` with an `else` look like in VM code? Write one that
  puts the bigger of `temp 0` and `temp 1` into `temp 2`.

## Checkpoint

The learner can, without help:
- [ ] Write a loop in VM code, and run it in the VM Emulator
- [ ] Translate `label`, `goto` and `if-goto` into Hack on paper
- [ ] Pass BasicLoop and FibonacciSeries

## Lab notebook

Copy `Sum.vm` and its Python side by side, with arrows between the
matching parts. Commit. Add *program flow*, *label*, *goto* and
*if-goto* to `dictionary.md`.

## Guide's background *(optional reading)*

This is the first part of Nand to Tetris Project 8. Branching in the VM
maps almost directly onto Hack: labels become Hack labels, `goto`
becomes `0;JMP`, and `if-goto` pops and jumps on `JNE`, so any non-zero
value counts as true. In the next lesson, labels are made unique to
their function (a label `LOOP` inside `Main.run` becomes
`Main.run$LOOP`), so two functions can both have a `LOOP`. The book
specifies this, and the tests don't mind either way, because BasicLoop
and FibonacciSeries have no functions.

The CPU Emulator starts with every RAM word at 0, including `SP`, which
is why the learner sets `RAM[0]` to 256 by hand for their own programs.
The official tests set it in their `.tst` scripts, and from Lesson 8.10
the translator's own start-up code does it.
