# Lesson 8.2: Addresses and Pointers

**Time:** 2 sessions of 45 min · **You need:** a terminal and an editor;
`~/lab/c`; squared paper; sticky notes · **New words:** address,
pointer, `&` (address of), `*` (what's at), array, `sizeof`, byte

## Goal *(read this to the learner)*

> In your Hack computer, every word of RAM had an address, and `@` let
> you point at any of them. A real computer is just the same, only
> bigger. In Python you never see the addresses, but in C you can: you
> can ask where a variable lives, keep that address in another variable
> (a **pointer**), and change things through it. That's how C programs
> share big things without copying them, and also how they break in
> strange ways.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Draw a row of eight boxes on squared paper, labelled with
      addresses 100, 104, 108... *(Real addresses are much longer.)*

## Warm-up (5 min)

"In Hack, what does `@100` then `M=1` do?" *(Puts 1 in the RAM word at
address 100.)* "What did `A` hold?" *(An address. `M` is the word it
points at.)*

## Activity

### Session 1: where does a variable live?

1. **Boxes with numbers on.** On the paper boxes, write "diamonds = 64"
   in box 104. **Say:** "Every variable lives somewhere in the RAM. The
   place has a number: its **address**. In this computer, the RAM is
   counted in **bytes** (8 bits each), and an `int` takes four of them,
   so the boxes go up in fours."

2. **Ask C where.** New file, `~/lab/c/address.c`:
   ```c
   #include <stdio.h>

   int main(void) {
       int diamonds = 64;
       int *where = &diamonds;
       printf("diamonds is %d\n", diamonds);
       printf("it lives at address %p\n", (void *) where);
       printf("what's at that address: %d\n", *where);
       *where = 100;
       printf("diamonds is now %d\n", diamonds);
       return 0;
   }
   ```
   Compile and run (`gcc address.c -o address`, then `./address`).
   **They should see** something like:
   ```
   diamonds is 64
   it lives at address 0x7ffde860be2c
   what's at that address: 64
   diamonds is now 100
   ```
   The address will be different, and different every run. **Say:**
   - "`&diamonds` means 'the address of diamonds'.
   - `int *where` makes a **pointer**: a variable that holds the address
     of an `int`. The `*` here means 'pointer to'.
   - `*where`, used later, means 'what's at that address'. So
     `*where = 100` changes `diamonds`, without ever saying its name!
   - `%p` prints an address in hexadecimal (base 16, from Stage 4). The
     `(void *)` tells `printf` it's just an address."

   **Ask:** "Which Hack instruction is like `&`, and which like `*`?"
   *(`@diamonds` puts the address in A, like `&`. Using `M` is like `*`:
   what's at that address.)*

   Run it three times. **Ask:** "Why does the address change?" *(Linux
   puts programs at a different place each time, on purpose, to make
   them harder to attack. Stage 11 explains why.)*

3. **On paper.** Draw `diamonds` in box 104 with 64 in it, and `where`
   in box 120 with **104** in it, and an arrow from `where` to
   `diamonds`. **Say:** "A pointer is just a number. It happens to be an
   address, and the arrow is how we think about it."

### Session 2: why pointers matter

4. **A swap that doesn't work.** New file, `swap.c`:
   ```c
   #include <stdio.h>

   void swap_copies(int a, int b) {
       int t = a;
       a = b;
       b = t;
   }

   void swap(int *a, int *b) {
       int t = *a;
       *a = *b;
       *b = t;
   }

   int main(void) {
       int x = 1, y = 2;
       swap_copies(x, y);
       printf("after swap_copies: x = %d, y = %d\n", x, y);
       swap(&x, &y);
       printf("after swap:        x = %d, y = %d\n", x, y);
       return 0;
   }
   ```
   **They should see:**
   ```
   after swap_copies: x = 1, y = 2
   after swap:        x = 2, y = 1
   ```
   **Say:** "`void` means the function gives nothing back. When you call
   a function in C, it gets *copies* of the numbers. `swap_copies`
   swapped its own copies, then threw them away. `swap` got the
   *addresses* of `x` and `y`, so it could reach back and change the real
   ones."

   Act it out: one person holds sticky notes "x: 1" and "y: 2". In
   `swap_copies`, the other person copies them onto new notes and swaps
   those. In `swap`, they're told *where* the real notes are, and swap
   those.

5. **Arrays are boxes in a row.** New file, `array.c`:
   ```c
   #include <stdio.h>

   int main(void) {
       int chest[5] = {10, 20, 30, 40, 50};
       printf("an int takes %zu bytes\n", sizeof(int));
       for (int i = 0; i < 5; i++) {
           printf("chest[%d] = %d at %p\n", i, chest[i], (void *) &chest[i]);
       }
       int *p = chest;
       printf("*p = %d, *(p + 2) = %d\n", *p, *(p + 2));
       printf("chest[7] = %d  (there is no chest[7]!)\n", chest[7]);
       return 0;
   }
   ```
   **They should see** something like:
   ```
   an int takes 4 bytes
   chest[0] = 10 at 0x7ffede843e70
   chest[1] = 20 at 0x7ffede843e74
   chest[2] = 30 at 0x7ffede843e78
   chest[3] = 40 at 0x7ffede843e7c
   chest[4] = 50 at 0x7ffede843e80
   *p = 10, *(p + 2) = 30
   chest[7] = 665067732  (there is no chest[7]!)
   ```
   **Say:** "An **array** is a row of boxes, side by side. `int
   chest[5]` makes five `int`s, and the addresses go up by 4, because
   `sizeof(int)` is 4 bytes. (`%zu` prints a size.) In hexadecimal,
   after `...e7c` comes `...e80`: c is 12, and 12 + 4 = 16, which carries."

   "The name `chest` on its own is the address of the first box. So
   `p + 2` is two boxes along, and `*(p + 2)` is what's in it:
   `chest[2]` is just a short way to write `*(chest + 2)`."

6. **The scary line.** **Ask:** "What's `chest[7]`?" *(There isn't one!)*
   **Say:** "Python would stop with an `IndexError`. C just goes 7 boxes
   along and reads whatever happens to be there: something else's
   memory. Your number will be different, and might change every run. C
   trusts you completely. That's why it's fast, and why it's dangerous.
   Next lesson, we'll see what happens when you *write* past the end."

   Commit all three programs.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `warning: initialization of ‘int *’ from ‘int’ makes pointer from integer` | `int *where = diamonds;` is missing the `&` | `&diamonds`: the *address* of diamonds. |
| `warning: passing argument 1 of ‘swap’ makes pointer from integer` | `swap(x, y)` instead of `swap(&x, &y)` | Pass the addresses. |
| `error: invalid type argument of unary ‘*’ (have ‘int’)` | A `*` in front of something that isn't a pointer | Only pointers can be followed with `*`. |
| `Segmentation fault (core dumped)` | The program used an address that isn't its own (Lesson 8.3) | Look for a pointer that was never given an address. |
| The address is the same every run | Some computers or debuggers turn off the shuffling | That's fine. |

## Talk about it

- What's an address? What's a pointer? What do `&` and `*` do?
- Why didn't `swap_copies` work?
- What happens in C if you read past the end of an array? And in Python?

## Challenge *(if there's time, or for next time)*

- Print the addresses of a `char`, a `double` and an `int`, and
  `sizeof` each one. *(1, 8 and 4 bytes.)*
- Write `void double_it(int *n)`, which doubles the number its argument
  points at. Test it.
- Write a function that sets all five boxes of `chest` to 0, given only
  `int *p` and the size 5.

## Checkpoint

The learner can, without help:
- [ ] Explain address and pointer, and draw a pointer as an arrow
- [ ] Use `&` and `*`, and say what each means
- [ ] Explain why `swap` needs pointers
- [ ] Explain an array as boxes in a row, and why reading past the end
      gives nonsense

## Lab notebook

Draw the paper boxes for `address.c`, with the arrow. Draw `chest` with
its addresses. Commit. Add *address*, *pointer*, *array*, *byte* and
*sizeof* to `dictionary.md`.

## Guide's background *(optional reading)*

A **pointer** is a variable whose value is a memory address. In C,
`&x` gives the address of `x`, and `*p` **dereferences** `p` (follows it
to what it points at). Array indexing is defined in terms of pointers:
`a[i]` means `*(a + i)`, and adding `i` to a pointer moves it on by
`i` *items*, not bytes, which is why the addresses in `array.c` go up by
`sizeof(int)`.

C doesn't check array bounds. Reading `chest[7]` is **undefined
behaviour**: the C standard says anything may happen. In practice it
reads whatever is on the stack there. Writing past the end is worse,
and Lesson 8.3 shows it. The changing addresses are **ASLR** (address
space layout randomisation), a defence against attacks that need to
know where things are in memory.

The learner already knows all of this from the Hack machine: Hack's
pointers were RAM addresses in the A register (Lesson 6.11), and the
VM's `pointer`, `this` and `that` segments (Lessons 8.8 and 8.16) are
pointers too.
