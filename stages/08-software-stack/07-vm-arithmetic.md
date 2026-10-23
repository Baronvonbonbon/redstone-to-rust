# Lesson 8.7: The VM Translator, Part 1: Arithmetic (Project 7)

**Time:** 3–4 sessions of 45 min · **You need:** a terminal; Thonny;
`~/lab/n2t`; the VM card and the Hack card; squared paper · **New
words:** VM translator, translate, unique label

## Goal *(read this to the learner)*

> Your Hack computer has no stack: just A, D and the RAM. But the RAM can
> *hold* a stack, if we're careful with `SP`. Today you'll start the
> **VM translator**: a Python program that turns each VM command into a
> few lines of Hack assembly that do the same thing. By the end, your
> computer will run `push`, `add`, `sub`, and true-or-false comparisons.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once. As in Lesson 6.13, this is a real
      program built over several sessions. This lesson gives the start of
      it and hints for the rest, never the finished program: the Nand to
      Tetris authors ask that the solutions aren't published. The test
      is the judge.
- [ ] Check that `check-vm` is in `~/bin` (Lesson 8.6).

## Warm-up (5 min)

Play `push constant 7`, `push constant 8`, `add` with cards. "Where is
the stack really kept?" *(In the RAM, from address 256.)* "What does
`SP` hold?" *(The address of the next free place.)*

## Activity

### Session 1: push

1. **On paper first.** Draw RAM boxes 0 and 256 to 259. Put 256 in box 0
   (SP). **Say:** "To push 7, three things must happen: put 7 in D; put D
   in the box that SP points at; make SP one bigger." Write it in Hack,
   together, with the Hack card:
   ```
   @7       // A = 7
   D=A      // D = 7
   @SP      // A = 0, so M is SP
   A=M      // A = what's in SP: 256
   M=D      // RAM[256] = 7
   @SP
   M=M+1    // SP = 257
   ```
   Play it on the paper boxes. **Say:** "`A=M` is the pointer trick from
   Lesson 6.11: follow the address in SP."

2. **The starting program.** In Thonny, make
   `~/lab/n2t/projects/7/vm.py`:
   ```python
   import sys


   def push_d():
       """Hack assembly that pushes the D register onto the stack."""
       return ["@SP", "A=M", "M=D", "@SP", "M=M+1"]


   def translate(words):
       """Gives back a list of Hack assembly lines for one VM command."""
       if words[0] == "push" and words[1] == "constant":
           return ["@" + words[2], "D=A"] + push_d()
       print("I don't know how to translate", words)
       return []


   name = sys.argv[1]
   asm = []
   for line in open(name):
       words = line.split("//")[0].split()
       if words:
           asm.append("// " + " ".join(words))
           asm += translate(words)

   out = open(name.replace(".vm", ".asm"), "w")
   for line in asm:
       out.write(line + "\n")
   out.close()
   ```
   **Say:** "It reads each line of the `.vm` file, takes away the comment,
   and splits it into words: `push constant 7` becomes `['push',
   'constant', '7']`. `translate` turns those words into a list of Hack
   lines. Each VM command is written into the `.asm` file as a comment
   first, so you can find it later. `push_d` is a helper: any time
   you've got a number in D, `push_d()` pushes it."

3. **Try it.**
   ```
   cd ~/lab/n2t/projects/7
   python3 vm.py StackArithmetic/SimpleAdd/SimpleAdd.vm
   cat StackArithmetic/SimpleAdd/SimpleAdd.asm
   ```
   **They should see:** `I don't know how to translate ['add']`, then the
   `.asm` file: `// push constant 7`, the seven lines from step 1, the
   same for 8, and `// add` with nothing under it.

   Now the test, which translates the program and runs the official test
   on the CPU Emulator:
   ```
   check-vm StackArithmetic/SimpleAdd
   ```
   **They should see:**
   ```
   NOT YET. The CPU Emulator says:
       Comparison failure at line 2
   Line 2 of the test. Yours, then the right one:
   |  RAM[0]  | RAM[256] |
   |     258  |       7  |
   |     257  |      15  |
   ```
   **Say:** "Both pushes worked: SP went up to 258. Now for `add`."
   Commit (`git add vm.py`, then `git commit`).

### Session 2: add, and its family

4. **`add` on paper.** Draw before and after:
   ```
   before:  SP = 258   RAM[256] = 7   RAM[257] = 8
   after:   SP = 257   RAM[256] = 15
   ```
   **Say:** "`add` takes the top number (y = 8) and the one under it
   (x = 7), and leaves x + y where x was." Work out the Hack together,
   on paper, in two parts:
   - **Pop y into D.** SP must go down by 1, and then D gets what's at
     that address. Hint: on the Hack card, `AM=M-1` does two jobs at once.
     After `@SP`, it makes SP one smaller *and* points A at the new SP.
   - **Add D to x.** x is now just under SP. Hint: A is pointing at y's
     old box. What does `A=A-1` do? Then the card's comp table has a way
     to add D and M, and store the answer in M.

   Count: SP must end at 257. Check: the pop moved it down once, and
   nothing moves it after that, so it's right.

   **Important:** use the Hack card's spellings exactly: `D+M`, not
   `M+D`. The CPU Emulator understands both, but your own assembler from
   Lesson 6.13 only knows the card's, and in Lesson 8.18 it will have to
   read everything this translator writes.

5. **Write it.** Add a helper `pop_d()` (like `push_d`) for the first part,
   because many commands will need it, and a branch in `translate` for
   `add`. Then:
   ```
   check-vm StackArithmetic/SimpleAdd
   ```
   **They should see:** `ALL GOOD! SimpleAdd passes.` Commit.

6. **The family.** `sub`, `and` and `or` are the same as `add`, with a
   different comp (`M-D`: x − y, not y − x!). `neg` and `not` only touch
   the top number, so they don't pop at all: point A at the top (SP − 1)
   and change M where it is. Try one at a time. To test one command,
   write a tiny `.vm` file in `projects/7/mine` (like Lesson 8.6's), and
   `python3 vm.py mine/Try.vm`. Load `mine/Try.asm` in `cpu`, then click
   `RAM[0]`'s value and type 256 (the emulator starts with 0 there, and
   the stack needs SP to start at 256). Single-step to the end of the
   program, and look at `RAM[256]`.

   **Ask:** "Could a dictionary make this shorter?" *(Yes: `{"add":
   "D+M", "sub": "M-D", ...}`, so the four two-number commands share one
   branch.)*

### Sessions 3 and 4: true and false

7. **Comparisons on paper.** `eq`, `gt` and `lt` leave −1 (true) or 0
   (false). **Say:** "Hack can't compare directly, but it can *jump* on
   a number: `D;JEQ` jumps if D is 0. So work out D = x − y. Then x = y
   exactly when D = 0, x > y when D > 0, and x < y when D < 0."

   Plan, in Python-ish words, on paper:
   ```
   pop y into D
   point A at x
   D = x - y
   put -1 (true) where x is
   if D passes the test, jump past the next part
   point A at x again, and put 0 (false) there
   (the place to jump to)
   ```
   Hints:
   - Writing −1 into x first, then fixing it to 0 if the test fails,
     saves a jump.
   - The jump needs a label, like `(TRUE)`. But a program might have a
     hundred `eq`s, and every label must be different! Keep a **counter**
     at the top of the program (`count = 0`), and add 1 each time you
     make a label, so you get `TRUE1`, `TRUE2`... Inside a function,
     changing a variable from outside needs `global count` first.
   - After the jump, `@TRUE1` has put a new number in A, so you have to
     point A back at x.

8. **The big test.**
   ```
   check-vm StackArithmetic/StackTest
   ```
   **They should see:** `ALL GOOD! StackTest passes.` StackTest does
   every command. If it fails, look at the row it prints: `RAM[0]` is SP,
   then the stack. Find the first wrong number, and look in
   `StackTest.vm` for the command that made it. Commit.

   **Say:** "Your computer can now do arithmetic and logic on a stack.
   Next, it needs variables."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `I don't know how to translate ['sub']` | That command isn't written yet | Add a branch to `translate`. |
| `NOT YET: vm.py crashed (above).` | A Python error | Read the traceback above it, like any Python error. |
| `Comparison failure at line 4` in StackTest, with `-115` where `-91` should be | `sub` works the wrong way round | x − y is `M-D` (M is x, D is y). |
| `Comparison failure at line 2` in StackTest, with `1` where `-1` should be | True is 1, not −1 | `M=-1` for true. |
| StackTest fails with `RAM[0]` at 258 instead of 266, and leftover numbers on the stack | Two comparisons share one label, so a jump lands in the wrong place | Add 1 to the counter for every label. |
| `In line 12: ...` when loading in the CPU Emulator | A line of Hack the emulator can't read (it counts from 0) | Look at that line in the `.asm`, and check it against the Hack card. |
| `SimpleAdd` passes, but your assembler says `KeyError: 'M+D'` (Lesson 8.18) | A spelling the Hack card doesn't have | Use `D+M`, `D&M`, `D\|M`. |

## Talk about it

- What does the VM translator do? Which rung of the ladder is it?
- How does `push` work in Hack? How does `pop`?
- Why must every label be different?
- How can Hack compare two numbers when it has no compare instruction?

## Challenge *(if there's time, or for next time)*

- Make the translator stop with a friendly message (and the line number)
  for a command it doesn't know, instead of carrying on.
- How many Hack instructions does each VM command become, in your
  translator? Which is the longest?
- `push constant 0` could be shorter: there's no need for D at all (look
  for `M=0` on the card). What else could be shorter? Keep this for
  Lesson 8.18!

## Checkpoint

The learner can, without help:
- [ ] Translate `push constant`, `add` and `neg` into Hack on paper
- [ ] Explain how a comparison becomes −1 or 0 with a jump
- [ ] Explain why labels need a counter
- [ ] Pass `check-vm` for SimpleAdd and StackTest

## Lab notebook

Draw the RAM before and after `add`. Write the plan for `eq`. Commit.
Add *VM translator* and *unique label* to `dictionary.md`. Tick Project
7 (half) on the passport's Nand to Tetris climb.

## Guide's background *(optional reading)*

This is the first half of Nand to Tetris Project 7. The VM translator
is the "back end" of the two-stage compiler: it maps each stack command
onto Hack, keeping the stack in RAM from address 256 with `SP` at
`RAM[0]`. Pushing is "write at `*SP`, then increment `SP`"; popping is
"decrement `SP`, then read at `*SP`". Comparisons use the subtraction
and a conditional jump, because the Hack ALU has no comparison output
that can be stored. Subtraction can overflow for numbers far apart,
which the official tests carefully avoid; the book mentions this.

`check-vm` (in `~/lab/n2t/stack`) runs the learner's `vm.py` on a test
folder, then the official `.tst` script on the CPU Emulator, which
loads the `.asm`, sets up `SP`, runs a fixed number of clock cycles, and
compares the RAM. It prints the failing row with its heading, so you
can see which RAM word is wrong without opening anything.

As in Stage 6, solutions aren't published here, and please keep the
learner's `vm.py` private. The hints in this lesson have all been
checked against a working translator, kept out of the repository.
