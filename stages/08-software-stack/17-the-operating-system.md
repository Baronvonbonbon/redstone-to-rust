# Lesson 8.17: The Operating System (Project 12)

**Time:** 5–6 sessions of 45 min · **You need:** a terminal; Thonny;
`~/lab/n2t`; the Jack card; squared paper; about 30 building blocks ·
**New words:** operating system, shift-and-add, heap, free list,
allocate

## Goal *(read this to the learner)*

> Every program you've run on your computer has leaned on the operating
> system: `Math.multiply` for every `*`, `Memory.alloc` for every object,
> `Screen.drawRectangle` for every block. So far, the VM Emulator has
> pretended to be the OS. Now you'll write the most important parts
> yourself, in Jack: multiplying and dividing with only adding, sharing
> out memory, and drawing on the screen one pixel at a time.

## Before the lesson *(guide, 15 min)*

- [ ] Read this whole lesson once.
- [ ] Practise the block multiplication in step 1.
- [ ] The OS classes go in `~/lab/n2t/projects/12/`, which already has
      a starting file for each (`Math.jack`, `Memory.jack` and so on),
      and a test folder for each (`MathTest`, `MemoryTest`...).

## Warm-up (5 min)

"Hack's ALU can add and subtract. Can it multiply?" *(No!)* "So what
did `push constant 6`, `push constant 7`, `call Math.multiply 2` rely
on?" *(A function in the OS, written with only adding.)*

## Activity

### Session 1: multiplying with doubling

1. **Doubling with blocks.** **Say:** "To work out 6 × 13, write 13 in
   binary: 8 + 4 + 1 (1101). So 6 × 13 = 6 × 8 + 6 × 4 + 6 × 1." With
   blocks: make a row of 6. Double it (12), and again (24), and again
   (48). Those are 6 × 1, 6 × 2, 6 × 4, 6 × 8. Now add the ones where 13
   has a 1 bit: 6 + 24 + 48 = 78. **They should see:** 78, which is
   6 × 13.

   **Say:** "This is **shift-and-add**: double x each time (that's a
   shift, in binary), and add it in when y's bit is 1. Sixteen bits means
   at most sixteen doublings, however big the numbers. Doubling is just
   `x + x`."

2. **`Math.multiply`.** Open `~/lab/n2t/projects/12/Math.jack`. It has
   empty functions with comments. Hints:
   - In `Math.init`, make the static array `powersOfTwo` (already named
     at the top of the file) with `Array.new(16)`, and fill it with 1, 2,
     4, 8... 16384, -32768 (keep doubling: the last one wraps round).
   - A helper `bit(x, i)` is true when bit i of x is 1: `x & powersOfTwo[i]`
     isn't 0.
   - In `multiply`, loop i from 0 to 15: if `bit(y, i)`, add `shiftedX`
     to the sum; then double `shiftedX`.
   - **You can't use `*` inside `Math.multiply`!** The compiler turns `*`
     into a call to `Math.multiply`, which would call itself for ever.
     Write `x + x` for doubling. Negative numbers just work, because of
     two's complement (Lesson 6.5).

   Also write `abs`, `min` and `max`, which are short.

### Session 2: dividing and square roots

3. **`Math.divide`.** **Say:** "Dividing is the opposite trick: how many
   times does y fit into x? Work out how many times 2y fits, and double
   it, then check whether one more y fits." This plan is from the book:
   ```
   divide(x, y), for x and y not negative:
       if y > x: the answer is 0
       q = divide(x, 2 * y)
       if x - 2 * q * y < y: the answer is 2 * q
       otherwise:            the answer is 2 * q + 1
   ```
   Try 100 ÷ 7 on paper: 7 doesn't fit... follow it down and back up.
   *(14.)*

   Hints:
   - It's recursive, like Lesson 7.5. Write it as a helper for numbers
     that aren't negative, and make `divide` use `abs`, then put the sign
     back: negative if exactly one of x and y was negative.
   - Using `*` here is fine (it calls *your* `multiply`).
   - `2 * y` can overflow and become negative when y is big. Treat a
     negative `2 * y` like "too big": the answer is 0.

4. **`Math.sqrt`.** **Say:** "The square root of a 16-bit number is at
   most 181, which fits in 8 bits. Find the bits one at a time, from the
   biggest: try adding 128. Is the square still not too big? Keep it.
   Then try 64, and so on." That's binary search from Lesson 7.2.
   Hint: if `(y + powersOfTwo[j])` squared is negative, it overflowed, so
   it's too big too.

5. **Test.**
   ```
   cd ~/lab/n2t/projects/12
   check-os Math
   ```
   **They should see:** `ALL GOOD! Your Math passes its test.` If not, the
   rows show 14 answers: look in `MathTest/Main.jack` for which sum each
   one is. Commit.

### Session 3: sharing out memory

6. **The heap.** **Say:** "Objects and arrays live on the **heap**:
   `RAM[2048]` to `RAM[16383]`. `Memory.alloc(size)` must find `size`
   free boxes, and give back their address. That's called
   **allocating**. `deAlloc` gives them back."

   First, a trick for `peek` and `poke`:
   ```
   let ram = 0;
   ```
   **Say:** "`ram` is an `Array` that starts at address 0. So `ram[5000]`
   is the box at 5000: the whole RAM, as one array! Jack lets us do this
   because an array is just an address."

7. **Version 1: never give back.** The simplest allocator keeps one
   number, `next`, starting at 2048. `alloc(size)` gives back `next`, and
   moves `next` on by `size`. `deAlloc` does nothing at all. Write it,
   then:
   ```
   check-os Memory
   check-os Array
   ```
   (`Array.new` is just `Memory.alloc`, and `dispose` is `deAlloc`.)
   **They should see:** `ALL GOOD!` twice. Commit.

   **Ask:** "What's wrong with it?" *(Memory that's given back can never be
   used again. A game that makes and throws away objects for an hour
   would run out.)*

### Session 4: a free list

8. **Version 2: a list of free blocks.** On squared paper, draw the heap
   as a long strip. **Say:** "We keep a linked list (Lesson 7.11) of the
   free blocks, inside the free memory itself. Each free block's first
   box holds its size, and its second box holds the address of the next
   free block (0 for none). At the start, there's one free block: the
   whole heap."

   The plan:
   - `alloc(size)`: walk along the list until a block is big enough
     (its size is at least `size + 3`). Cut `size + 1` boxes off its
     *end*: shrink the free block's size, write `size + 1` in the first of
     the cut boxes (so `deAlloc` will know how big it was), and give back
     the address just after that.
   - `deAlloc(o)`: the block starts one box before `o`, and its size is
     already written there. Put it on the front of the free list.

   Act it out on the strip with sticky notes: alloc 3, alloc 5, deAlloc
   the first, alloc 2. **Ask:** "Why `size + 3`, not `size + 1`?" *(So
   the free block that's left still has room for its size and its
   next-address: 2 boxes.)*

   ```
   check-os Memory
   ```
   Commit.

### Sessions 5 and 6: drawing

9. **`Screen.drawPixel`.** **Say:** "The screen is memory (Lesson 6.11):
   row y starts at 16384 + 32 × y, and each word holds 16 pixels." Hints:
   - The word is at `16384 + (32 * y) + (x / 16)`.
   - The pixel is bit `x & 15` of that word (that's `x` mod 16).
   - To make it black, `|` the word with that bit; to make it white,
     `&` it with `~` that bit. Keep a static `color` for `setColor`.
   - Use `Memory.peek` and `Memory.poke`.

10. **Lines, rectangles and circles.**
    - `drawRectangle`: one horizontal line for each row.
    - `drawLine`: do the easy ones first, horizontal (y stays the same)
      and vertical (x stays the same). A sloping line is a staircase:
      from one end, take a step across or a step down (or up), each time
      choosing the one that keeps closest to the true line. The book's
      trick keeps a number `diff`: step across when it's below 0, and add
      the height; otherwise step down, and take away the width.
    - `drawCircle(x, y, r)`: for each row `dy` from −r to r, draw a
      horizontal line of half-width `sqrt(r*r - dy*dy)` (Pythagoras!).

    Test it in the window:
    ```
    cp Screen.jack ScreenTest/
    jackc ScreenTest
    ```
    Load the folder `ScreenTest` in `vme` (Yes to built-in, for the rest
    of the OS; No animation; Run). **They should see:** a house with a
    door and window, and a sun with rays, the same as the picture
    `ScreenTest/ScreenTestOutput.gif` (open it with
    `xdg-open ScreenTest/ScreenTestOutput.gif`). Commit.

11. **The rest.** `Output`, `String`, `Keyboard` and `Sys` are the other
    OS classes. They're optional here: the book has the plans, and
    `OutputTest`, `StringTest`, `KeyboardTest` and `SysTest` show what
    each should do. Every program in this course works with your Math,
    Memory, Array and Screen, plus the official versions of the rest.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `Stack overflow in Math.multiply.14` | `*` was used inside `Math.multiply`, so it called itself for ever | Double with `x + x`. |
| Math's answers start `4  48  144`, where they should be `6  -180  -18000` | `multiply` doesn't double `shiftedX` each time round | Double it at the end of every loop. |
| `NOT YET. The Jack compiler says: ... Expected ;` | A typo in the OS file | Fix the line it names. |
| `'This' segment must be in the Heap range in String.new.3` (Memory) | `alloc` gives the same block twice, or an address outside the heap | Check that the free block shrinks, and the address is after the size box. |
| The screen test draws stripes, or pixels in the wrong place | The bit or the word is wrong in `drawPixel` | Try `drawPixel(0, 0)`, then `(15, 0)`, then `(16, 0)`, and look at `RAM[16384]` and `RAM[16385]`. |
| `check-os can test Math, Memory and Array.` | `check-os Screen` was asked | Look at Screen in the window (step 10). |

## Talk about it

- How does shift-and-add multiply with only adding?
- Why can't `Math.multiply` use `*`?
- What's a free list? Where is it kept?
- How does `drawPixel` find the right bit?

## Challenge *(if there's time, or for next time)*

- When `deAlloc` gives back a block that's right next to another free
  block, join them into one bigger block (this stops the heap breaking
  into crumbs).
- Write `String.jack`: a string is an array of characters, a length and
  a maximum length. Test it with `StringTest`.
- Make `drawRectangle` faster by filling whole words of 16 pixels at a
  time in the middle of each row.

## Checkpoint

The learner can, without help:
- [ ] Multiply two numbers with doubling and adding, with blocks or on
      paper, and explain the bits
- [ ] Explain the recursive divide, and why `2 * y` can overflow
- [ ] Explain a free list, and act out `alloc` and `deAlloc`
- [ ] Pass `check-os` for Math, Memory and Array, and draw ScreenTest's
      picture with their own Screen

## Lab notebook

Draw the doubling rows for 6 × 13. Draw the heap strip with its free
list arrows. Stick in a printout or sketch of the house and sun. Commit.
Add *operating system*, *shift-and-add*, *free list* and *allocate* to
`dictionary.md`. Tick Project 12 on the passport.

## Guide's background *(optional reading)*

This is Nand to Tetris Project 12. A real operating system (Stage 10)
manages processes, files and devices; the Jack OS is a smaller thing,
more like a standard library plus a memory manager. Its algorithms are
classics: shift-and-add multiplication (which is what multiplier
circuits do in hardware), division by repeated doubling, square root by
binary search on the bits, a **first-fit** heap allocator with a free
list kept inside the free blocks themselves (C's `malloc` from Lesson
8.4 works the same way, with more cleverness), and Bresenham-style line
drawing.

The plans in this lesson are the book's algorithms, given in words and
pseudocode; the Jack is the learner's. `check-os` (in
`~/lab/n2t/stack`) compiles the official test with the learner's class,
adds the rest of the OS as VM code, and runs the official test with more
steps than the `.tst` file asks for, because the VM-code OS takes a
while to start up. Screen, Output, String and Keyboard have only
picture tests, which is why step 10 uses the window.

The first, "never give back" allocator passes `MemoryTest`, and the book
suggests starting with it. The free list is what makes a long-running
program possible.
