# Lesson 8.8: The VM Translator, Part 2: Memory (Project 7)

**Time:** 3 sessions of 45 min · **You need:** a terminal; Thonny;
`~/lab/n2t`; the VM card and the Hack card; squared paper · **New
words:** memory segment, base address, offset

## Goal *(read this to the learner)*

> A program needs places to keep things: a function's own variables,
> the values it was given, an object's fields, and an array's boxes. The
> VM keeps each kind in its own **memory segment**: `local`, `argument`,
> `this`, `that`, and a few more. Today your translator learns to push
> from and pop into all of them. That finishes Project 7.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] `check-vm StackArithmetic/StackTest` should pass (Lesson 8.7).

## Warm-up (5 min)

"What does `push constant 5` do?" *(Puts 5 on top of the stack.)* "What
did your `pop_d` do?" *(Took the top number off, into D.)* "What does
`A=M` do after `@SP`?" *(Points A at the address that SP holds.)*

## Activity

### Session 1: segments with a base

1. **Segments on paper.** Look at the VM card's segment table together.
   **Say:** "`local 2` doesn't mean address 2. It means: find where the
   locals start, by looking in `LCL` (`RAM[1]`), and go 2 along." Draw
   RAM boxes: put 300 in box 1 (`LCL`), and the numbers 0, 0, 7 in boxes
   300, 301, 302. **Ask:** "What's `local 2`?" *(7, in box 302.)* "And
   if LCL held 500?" *(Box 502.)*

   **Say:** "The number in `LCL` is the **base address**: where the
   segment begins. The 2 is the **offset**: how far along. `argument`
   uses `ARG` the same way, `this` uses `THIS`, and `that` uses `THAT`."

2. **`push local 2` on paper.** Work out the Hack together:
   - Get the base into D: `@LCL`, then `D=M`.
   - Add the offset, and point A at the result. Hint: `@2` puts the
     offset in A. The card has a comp that adds D and A, and the dest
     can be A.
   - Now M *is* `local 2`. Put it in D, and use `push_d`.

3. **Write it.** The commands now have a segment word and a number:
   `words[1]` and `words[2]`. A dictionary saves four branches:
   ```python
   SEGMENTS = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}
   ```
   Write `push` for these four segments, then test with the official
   test:
   ```
   cd ~/lab/n2t/projects/7
   check-vm MemoryAccess/BasicTest
   ```
   It won't pass yet (BasicTest pops too), but your translator mustn't
   crash on the pushes. Commit.

### Session 2: pop, and the D problem

4. **`pop local 2` on paper.** **Say:** "To pop, we need two things at
   the same time: the number from the top of the stack, and the address
   `LCL + 2`. But Hack only has one D register to keep things in, and
   working out either one uses A." **Ask:** "Where could we keep one of
   them for a moment?" *(In the RAM! The VM card says `R13`, `R14` and
   `R15` are spare places for the translator.)*

   The plan:
   ```
   work out the address LCL + 2, in D
   save it in R13
   pop the top number into D
   point A at the address saved in R13
   put D there
   ```
   Hints: `pop_d()` from Lesson 8.7 does the third line. For the fourth,
   `@R13` then `A=M` follows the address in R13, just like `@SP` then
   `A=M`.

5. **Test.**
   ```
   check-vm MemoryAccess/BasicTest
   ```
   BasicTest also uses `temp` (next step), so it may still fail. If it
   does, look at the row. Each column is a RAM box it checks, from
   `RAM[256]` (the top of the stack) to `RAM[11]`. **Ask:** "Which of
   those are local, which argument, which this and that?" Look at
   `BasicTest.tst`: it sets `LCL` to 300, `ARG` to 400, `THIS` to 3000
   and `THAT` to 3010. *(`RAM[300]` is `local 0`; `RAM[401]` and
   `RAM[402]` are arguments; `RAM[3006]` is `this 6`; `RAM[3012]` and
   `RAM[3015]` are `that 2` and `that 5`.)* `RAM[11]` comes next.

### Session 3: fixed places, and static

6. **`temp` and `pointer`.** **Say:** "These two have no base to look
   up: they're always in the same place. `temp i` is `RAM[5 + i]`, and
   `pointer i` is `RAM[3 + i]`." **Ask:** "So `pointer 0` is which
   box?" *(3, which is `THIS`!)* **Say:** "Changing `pointer 0` moves the
   whole `this` segment. That's how a program chooses which object it's
   working on, in Lesson 8.16."

   For fixed places, the translator can work out the address itself,
   while it's translating: `temp 6` is `@11`, with no adding at run
   time. Write `push` and `pop` for `temp` and `pointer`.
   ```
   check-vm MemoryAccess/BasicTest
   check-vm MemoryAccess/PointerTest
   ```
   **They should see:** `ALL GOOD!` for both. Commit.

7. **`static`.** **Say:** "Static variables belong to the whole file, and
   every function in the file shares them. Where do we put them? Your
   assembler already knows how to find a free place for a variable:
   any `@name` it hasn't seen gets 16, then 17, and so on!" So `push
   static 3` in a file called `Thing.vm` can use the Hack variable
   `@Thing.3`. Two files can each have a `static 3`, and the file's name
   keeps them apart.

   Hints: `translate` needs the file's name now, so give it a second
   argument. `os.path.basename` (after `import os`) turns
   `MemoryAccess/StaticTest/StaticTest.vm` into `StaticTest.vm`, and
   `[:-3]` takes off the `.vm`.
   ```
   check-vm MemoryAccess/StaticTest
   ```
   **They should see:** `ALL GOOD! StaticTest passes.` Commit, and run
   all five Project 7 tests once more:
   ```
   for t in StackArithmetic/SimpleAdd StackArithmetic/StackTest MemoryAccess/BasicTest MemoryAccess/PointerTest MemoryAccess/StaticTest; do check-vm $t; done
   ```
   **They should see:** five `ALL GOOD!` lines. Project 7 is done!

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| BasicTest's row starts `-2580` where `472` should be | `pop` used D for the address, then popped into D, so the address was lost | Save the address in `R13` before popping. |
| BasicTest's last column is `0` where `510` should be | `temp` always uses `RAM[5]`, forgetting the offset | `temp i` is `5 + i`. |
| `KeyError: 'temp'` | `temp` went to the `SEGMENTS` dictionary, which only has the four with a base | Check the segment before looking it up. |
| `ValueError: invalid literal for int()` | `int()` was used on a word that isn't a number | `words[2]` is the number; `words[1]` is the segment. |
| `NOT YET: vm.py didn't make StaticTest.asm` | The output's name was worked out wrongly | Keep `name.replace(".vm", ".asm")` from the start. |
| PointerTest's row has `0` under `RAM[3]` and `RAM[4]` | `pointer 0` and `1` are `RAM[3]` and `RAM[4]` themselves, not what they point at | Use `@3` and `@4` directly, without `A=M`. |

## Talk about it

- What's a memory segment? Name four that have a base address.
- Why does `pop` need `R13`?
- Why can `temp 6` be worked out while translating, but `local 6` can't?
- How does the assembler give each static variable its own place?

## Challenge *(if there's time, or for next time)*

- Which VM commands make the most Hack lines now? Count for `push local
  3` and `pop local 3`.
- `push local 0` doesn't need the adding part at all. Can you make
  `push local 1` shorter with `A=A+1`? Save this for Lesson 8.18 too.
- Write a `.vm` program that swaps `local 0` and `local 1`, using only
  push and pop.

## Checkpoint

The learner can, without help:
- [ ] Explain base address and offset, and find `argument 3` on paper
- [ ] Translate `push local 2` and `pop local 2` into Hack on paper
- [ ] Explain why `pointer 0` changes the `this` segment
- [ ] Pass all five Project 7 tests

## Lab notebook

Draw the RAM with `LCL`, `ARG`, `THIS` and `THAT` pointing into it, as
arrows. Write the plan for `pop`. Commit. Add *memory segment*, *base
address* and *offset* to `dictionary.md`. Tick Project 7 on the
passport.

## Guide's background *(optional reading)*

This finishes Nand to Tetris Project 7. The eight segments let the
compiler (Lessons 8.13 to 8.16) map every kind of Jack variable onto the
VM: a subroutine's local variables onto `local`, its parameters onto
`argument`, an object's fields onto `this` (with `pointer 0` set to the
object's address), array elements onto `that` (with `pointer 1` set to
the element's address), and class-level variables onto `static`.
`temp` holds short-lived values the compiler needs, and `constant` is a
pretend segment for numbers.

`local`, `argument`, `this` and `that` are reached **indirectly**,
through a base address held in `RAM[1..4]`, because their place changes
at run time (every function call gets its own locals, Lesson 8.10).
`temp`, `pointer` and `static` are **direct**: the translator knows the
address. Using Hack variables named `File.i` for statics lets the
assembler allocate them, which is exactly what the book recommends.
