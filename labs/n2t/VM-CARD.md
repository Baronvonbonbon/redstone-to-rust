# VM Card

The Nand to Tetris virtual machine (VM) language, on one page:
everything you need for Lessons 8.6 to 8.10. Print it and keep it next
to the keyboard, with the Hack card.

## The stack

The VM has one **stack**: a pile of numbers. `push` puts a number on
top, and `pop` takes the top one off. Every other command takes its
numbers off the top of the stack and pushes its answer back.

```
push constant 7     stack: 7
push constant 8     stack: 7 8
add                 stack: 15
```

`SP` (`RAM[0]`) holds the address of the **next free place**, just
above the top. The stack starts at 256 and grows upwards.

## Arithmetic and logic

| Command | Takes | Pushes | Example (stack before → after) |
|---|---|---|---|
| `add` | x, y | x + y | `7 8` → `15` |
| `sub` | x, y | x − y | `7 8` → `-1` |
| `neg` | y | −y | `5` → `-5` |
| `eq` | x, y | true if x = y | `3 3` → `-1` |
| `gt` | x, y | true if x > y | `7 8` → `0` |
| `lt` | x, y | true if x < y | `7 8` → `-1` |
| `and` | x, y | x And y, bit by bit | `12 10` → `8` |
| `or` | x, y | x Or y, bit by bit | `12 10` → `14` |
| `not` | y | Not y, bit by bit | `0` → `-1` |

y is the top of the stack and x is just under it. **True is −1** (all
16 bits 1) and **false is 0**.

## Memory segments: `push SEGMENT i` and `pop SEGMENT i`

| Segment | What it is | Where it lives in the RAM |
|---|---|---|
| `constant` | the number i itself (push only) | nowhere |
| `local` | the function's local variables | starting at the address in `LCL` (`RAM[1]`) |
| `argument` | the function's arguments | starting at the address in `ARG` (`RAM[2]`) |
| `this` | the fields of the current object | starting at the address in `THIS` (`RAM[3]`) |
| `that` | an array, or another object | starting at the address in `THAT` (`RAM[4]`) |
| `pointer` | `pointer 0` *is* `THIS`, `pointer 1` *is* `THAT` | `RAM[3]` and `RAM[4]` |
| `temp` | eight spare places | `RAM[5]` to `RAM[12]` |
| `static` | the file's variables, shared by all its functions | the assembler's variables, from 16 |

"Starting at" means: `local 2` is at the address in `LCL`, plus 2.

## The RAM

| Addresses | What's there |
|---|---|
| 0 | `SP`, the stack pointer |
| 1, 2, 3, 4 | `LCL`, `ARG`, `THIS`, `THAT` |
| 5–12 | `temp` |
| 13–15 | `R13`, `R14`, `R15`: spare places for the translator's own use |
| 16–255 | `static` variables |
| 256–2047 | the stack |
| 2048–16383 | the **heap**, for objects and arrays (Lesson 8.17) |
| 16384–24575 | the screen |
| 24576 | the keyboard |

## Program flow

| Command | Does |
|---|---|
| `label NAME` | marks this place in the program |
| `goto NAME` | jumps to the label, always |
| `if-goto NAME` | **pops** the top number, and jumps if it isn't 0 |

## Functions

| Command | Does |
|---|---|
| `function NAME k` | starts a function with k local variables (all set to 0) |
| `call NAME n` | calls a function, after n arguments have been pushed |
| `return` | goes back to the caller, with the top of the stack as the answer |

After `call`, the caller's n arguments are replaced by the one answer.
Function names have the file's name in front: `Main.main`, `Math.abs`.

**The frame.** `call` saves the caller's world on the stack before
jumping, and `return` puts it back:

```
argument 0        <- ARG points here
...
argument n-1
return address    (where to go back to)
saved LCL
saved ARG
saved THIS
saved THAT
local 0           <- LCL points here
...
local k-1
(working stack)   <- SP
```

## Starting up (the bootstrap)

A whole program is a folder of `.vm` files. It starts with `SP = 256`,
then `call Sys.init 0`. `Sys.init` calls `Main.main`.

## Comments

`//` starts a comment, to the end of the line, as in Hack and Jack.
