# Lesson 8.16: Writing VM Code: Objects and Arrays (Project 11)

**Time:** 4–5 sessions of 45 min · **You need:** a terminal; Thonny;
`~/lab/n2t`; the Jack card and the VM card; squared paper; sticky notes
· **New words:** heap, object, `this` segment, `that` segment

## Goal *(read this to the learner)*

> Your compiler handles functions, loops and choices. The last part is
> the biggest idea: objects and arrays. An object is a little block of
> memory with its fields in it, and a method needs to know *which*
> block it's working on. An array is a block of boxes, and `a[i]` is
> just "go `i` boxes along". When this works, your compiler can compile
> Pong, and your own game.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] 1-Sums and 2-Loops should pass `check-jack` (Lesson 8.15).

## Warm-up (5 min)

"In Lesson 8.4, what did `malloc` do?" *(Borrowed memory from the heap,
and gave back its address.)* "What's `pointer 0`?" *(`RAM[3]`, which is
`THIS`: where the `this` segment starts.)*

## Activity

### Session 1: objects in memory

1. **An object is a block.** **Say:** "A `Creeper` has three fields: `x`,
   `y` and `health`. When `Creeper.new` runs, it borrows three boxes from
   the **heap** (`RAM[2048]` onwards), and the object *is* the address of
   those boxes." On paper, draw two creepers: `a` at address 2050, with
   3, 4, 20 in its boxes, and `b` at 2053, with 10, 1, 20.

   **Say:** "The variable `a` only holds the number 2050: a pointer, like
   in C. To work on `a`, a method sets `pointer 0` to 2050. Then `this 0`
   is `x`, `this 1` is `y`, and `this 2` is `health`. To work on `b`,
   set `pointer 0` to 2053, and the very same code works on `b`'s
   boxes." Move a sticky note labelled `THIS` between the two creepers.

2. **The rules for objects.** These are from the book:

   | Jack | VM code |
   |---|---|
   | a constructor's start | `push constant` (number of fields), `call Memory.alloc 1`, `pop pointer 0` |
   | a method's start | `push argument 0`, `pop pointer 0` |
   | a field | the `this` segment, with the field's number |
   | `this` | `push pointer 0` |
   | `a.move(2, -1)`, where `a` is a variable of class `Creeper` | push `a`, code for 2, code for −1, `call Creeper.move 3` |
   | `move(1)` inside a method | `push pointer 0`, code for 1, `call Creeper.move 2` |
   | `Creeper.new(3, 4)` (a class name, not a variable) | code for 3, code for 4, `call Creeper.new 2` |

   **Ask:** "Why does `a.move(2, -1)` call with 3 arguments?" *(The object
   itself is passed first, as argument 0. That's how the method knows
   which creeper.)* "So in a method, where are the real arguments?"
   *(From `argument 1` on. When compiling a method, put `this` into the
   subroutine table first, as argument 0.)*

   Hints:
   - A field's kind is `field`, and its segment is `this` (Lesson 8.15's
     table already says so).
   - To tell `a.move` from `Creeper.new`, look the first name up in the
     symbol tables. If it's there, it's a variable, and its *type* is the
     class name. If not, it's a class.
   - `compile_subroutine` needs to remember whether it's a constructor,
     method or function, to write the right start.

### Session 2: test the objects

3. **Test.**
   ```
   check-jack ~/lab/n2t/stack/tests/3-Objects
   ```
   3-Objects makes two creepers, moves them, hits them, and asks one how
   far it is from the other. **They should see:** `ALL GOOD!`. If an
   error says `Out of segment space`, or `'This' segment must be in the
   Heap range`, see the table at the end. Commit.

### Session 3: arrays and strings

4. **Arrays are blocks too.** **Say:** "`Array.new(10)` borrows 10 boxes,
   and gives their address. `a[i]` is the box at `a + i`. The VM reaches
   it with the `that` segment: set `pointer 1` to `a + i`, then `that 0`
   is the box." On paper: `squares` at 3000; `squares[7]` is at 3007.

   The rules, from the book:

   | Jack | VM code |
   |---|---|
   | `a[i]` in an expression | push `a`, code for i, `add`, `pop pointer 1`, `push that 0` |
   | `let a[i] = e` | push `a`, code for i, `add`, code for e, `pop temp 0`, `pop pointer 1`, `push temp 0`, `pop that 0` |

   **Ask:** "In `let`, why not set `pointer 1` straight away, before the
   code for e?" Hint: what if e is `b[j]`? *(Working out `b[j]` changes
   `pointer 1` itself! So the address waits on the stack, and the value
   waits in `temp 0`, until the end.)*

5. **Strings.** **Say:** "A string constant like `"Hi"` must be built
   while the program runs, one letter at a time, with the OS:"
   ```
   push constant 2
   call String.new 1
   push constant 72
   call String.appendChar 2
   push constant 105
   call String.appendChar 2
   ```
   "`String.new(2)` makes an empty string with room for 2 letters, and
   each `appendChar` gives back the same string, ready for the next
   letter. 72 is `H` and 105 is `i`. Python's `ord("H")` gives the code."

   ```
   check-jack ~/lab/n2t/stack/tests/4-Arrays
   ```
   4-Arrays fills an array with square numbers, adds them, looks things
   up with one array inside another (`squares[order[0]]`), keeps
   creepers in an array, and reads strings. **They should
   see:** `ALL GOOD!` Commit.

### Sessions 4 and 5: real programs

6. **Pong.** Compile the official Pong with your compiler:
   ```
   cd ~/lab/n2t/projects/11
   python3 compiler.py Pong
   ```
   Load the folder `Pong` in `vme` (Yes, No animation, Run), click the
   keyboard bar, and play with the arrow keys. **They should see:** Pong,
   just as in Lesson 6.13, but this time *you* compiled it. Try
   `Square` (arrow keys move it, `z` and `x` change its size, `q`
   stops), `Average`, and `ComplexArrays` too.

7. **Your own game.** Compile your Lesson 8.12 game, and Diamond Dash,
   with your compiler, in their folders in `projects/9`:
   ```
   python3 compiler.py ../9/DiamondDash
   ```
   Run each in `vme`. **They should see:** they play exactly as they did
   with `jackc`. Commit. Project 11 is done, and so is the compiler!

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `Out of segment space in Creeper.new.2` | The constructor didn't borrow memory for the fields | `push constant` (fields), `call Memory.alloc 1`, `pop pointer 0`. |
| `Out of segment space in Creeper.move.1` | The method didn't set `pointer 0` from `argument 0` | Start every method with `push argument 0`, `pop pointer 0`. |
| `'This' segment must be in the Heap range in Creeper.move.2` | `a.move(...)` didn't push `a` first | Push the object, and count it as an argument. |
| 4-Arrays' fourth answer is `1` where it should be `104` | `pointer 1` was set before the right-hand side was worked out | Use the `temp 0` pattern for `let a[i] = ...`. |
| A method's arguments are all off by one | `this` wasn't put into the subroutine table as argument 0 | Define `this` first, for methods only. |
| Pong runs, but very slowly | Animation is on | Set **No animation**. |

## Talk about it

- What *is* an object, in memory? What does `pointer 0` do?
- Why is the object passed as argument 0 to a method?
- How does `a[i]` become VM code? Why does `let a[i] = ...` need `temp 0`?
- How are string constants made?

## Challenge *(if there's time, or for next time)*

- Compile every program in `~/lab/n2t/projects/9` with your compiler,
  and run them all.
- Count the VM lines your compiler makes for Pong
  (`cat Pong/*.vm | wc -l`). Compare with `jackc`'s.
- What would go wrong if a program used `this` inside a `function`?
  Make your compiler give a friendly error for it.

## Checkpoint

The learner can, without help:
- [ ] Draw two objects on the heap, and explain how `pointer 0` chooses
      between them
- [ ] Explain how a method call passes the object
- [ ] Turn `a[i]` and `let a[i] = e` into VM code on paper
- [ ] Pass `check-jack` for all four tests, and play Pong compiled by
      their own compiler

## Lab notebook

Draw the two creepers on the heap, with `THIS` pointing at one. Write
the patterns for `a[i]`. Commit. Add *heap*, *object*, *this segment*
and *that segment* to `dictionary.md`. Tick Project 11 on the passport.

## Guide's background *(optional reading)*

This completes Nand to Tetris Project 11, and the compiler. Objects are
compiled exactly as in C (Lesson 8.4): a constructor allocates a block
with `Memory.alloc`, the object reference is that block's address, and
fields are reached at fixed offsets from it. A method receives the
object as a hidden first argument, which is how `self` works in Python
and `this` in Java and C++. Arrays use the second pointer, `that`, so a
method can work on its own fields (through `this`) and an array (through
`that`) at the same time.

The `temp 0` dance in `let a[i] = e` is the most famous subtle point of
the project. The tests catch it: 4-Arrays has `let squares[order[2]] =
squares[order[0]] + 100;`, where the right-hand side moves `pointer 1`.

All the code patterns here are the book's, given as VM templates; the
learner writes the Python that produces them. `check-jack`'s tests are
the course's own, written to cover each feature with known answers, and
the official programs (Pong, Square, Average, ComplexArrays, Seven,
ConvertToBin) are checked by running them.
