# Lesson 8.4: The Heap: Asking for Memory

**Time:** 2–3 sessions of 45 min · **You need:** a terminal and an
editor; `~/lab/c`; sticky notes; squared paper · **New words:** heap,
`malloc`, `free`, memory leak, use after free, `struct`, `->`

## Goal *(read this to the learner)*

> So far, every variable's size was fixed when you wrote the program.
> But what if a player chooses how big the chest is? Then the program
> has to ask for memory while it runs, from a big pool called the
> **heap**, and give it back when it's finished. Forget to give it back,
> and memory **leaks** away. Give it back and then keep using it, and
> things go very wrong. Today you'll do all three, and catch the bugs
> with a tool called valgrind. Then you'll build Lesson 7.11's linked
> list again, in C.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Write "heap" on a sheet of paper, and cut ten sticky notes for
      "blocks" of memory.

## Warm-up (5 min)

"What's a pointer?" *(A variable holding an address.)* "What does `*p`
mean?" *(What's at the address in `p`.)* "In Lesson 7.11, how did a
linked list's nodes find each other?" *(Each node pointed to the next.)*

## Activity

### Session 1: `malloc` and `free`

1. **The library of memory.** **Say:** "Variables inside a function live
   on the **stack**, and vanish when it ends. For anything else, a
   program borrows memory from the **heap**, like borrowing a book.
   `malloc` (memory allocate) borrows some bytes and gives you the
   address. `free` gives them back." Act it out: the learner asks the
   guide (the heap) for "three boxes", and gets sticky notes with an
   address written on. They return them with `free`.

2. **A chest of any size.** New file, `~/lab/c/chest.c`:
   ```c
   #include <stdio.h>
   #include <stdlib.h>

   int main(void) {
       int size;
       printf("How many slots in the chest? ");
       scanf("%d", &size);
       int *chest = malloc(size * sizeof(int));
       if (chest == NULL) {
           printf("No room for that many!\n");
           return 1;
       }
       for (int i = 0; i < size; i++) {
           chest[i] = i * i;
       }
       printf("The last slot holds %d\n", chest[size - 1]);
       free(chest);
       return 0;
   }
   ```
   **Say:** "`scanf("%d", &size)` reads a number that you type. It needs
   the *address* of `size`, so it can put the number there: just like
   `swap`. `malloc` needs the number of bytes, so we multiply by
   `sizeof(int)`. If there's no memory left, it gives back `NULL`, so we
   check. Then the pointer works exactly like an array."

   Compile and run it twice, typing `10` and then `1000`. **They should
   see:** `The last slot holds 81`, then `The last slot holds 998001`.

   **Ask:** "Try 1000000. What happens?" *(A negative number:
   999999 × 999999 is too big for an `int`, so it wraps round, as in
   Lesson 8.1.)*

3. **Structs: bundles of variables.** **Say:** "A Python class bundles
   values together. C's version is a `struct`. Here's a mob, and a linked
   list of them, like Lesson 7.11." New file, `mobs.c`:
   ```c
   #include <stdio.h>
   #include <stdlib.h>
   #include <string.h>

   struct Mob {
       char name[16];
       int health;
       struct Mob *next;
   };

   struct Mob *push_front(struct Mob *first, const char *name, int health) {
       struct Mob *mob = malloc(sizeof(struct Mob));
       strncpy(mob->name, name, sizeof(mob->name) - 1);
       mob->name[sizeof(mob->name) - 1] = '\0';
       mob->health = health;
       mob->next = first;
       return mob;
   }

   void show(struct Mob *mob) {
       while (mob != NULL) {
           printf("%s (%d) -> ", mob->name, mob->health);
           mob = mob->next;
       }
       printf("NULL\n");
   }

   void free_all(struct Mob *mob) {
       while (mob != NULL) {
           struct Mob *next = mob->next;
           free(mob);
           mob = next;
       }
   }

   int main(void) {
       struct Mob *mobs = NULL;
       mobs = push_front(mobs, "zombie", 20);
       mobs = push_front(mobs, "creeper", 20);
       mobs = push_front(mobs, "spider", 16);
       printf("Each mob takes %zu bytes\n", sizeof(struct Mob));
       show(mobs);
       free_all(mobs);
       return 0;
   }
   ```
   **They should see:**
   ```
   Each mob takes 32 bytes
   spider (16) -> creeper (20) -> zombie (20) -> NULL
   ```
   **Say:**
   - "`struct Mob` has a name (16 `char`s), a health, and a pointer to
     the next mob.
   - `mob->health` means 'the health of the mob that `mob` points at'.
     The arrow is a pointer arrow!
   - `strncpy` copies at most 15 letters, and then we make sure there's a
     `'\0'` (the null character) in the last box, so a long name can't
     overflow. That's last lesson's bug, avoided.
   - `free_all` has to remember `next` *before* freeing the mob: after
     `free`, the mob isn't ours any more."

   Draw the three mobs as boxes with arrows, on paper. **Ask:** "Why is a
   mob 32 bytes, when 16 + 4 + 8 is 28?" *(The computer likes pointers to
   start at an address that divides by 8, so the compiler adds 4 bytes of
   padding.)* Commit.

### Session 2: leaks, and using freed memory

4. **Valgrind.** **Say:** "Valgrind runs a program inside a pretend
   computer, and watches every byte it borrows." Compile with `-g`, and:
   ```
   gcc -g mobs.c -o mobs
   valgrind ./mobs
   ```
   **They should see** the program's two lines, mixed in with valgrind's
   report, ending with lines like:
   ```
   ==14==   total heap usage: 4 allocs, 4 frees, 1,120 bytes allocated
   ==14== All heap blocks were freed -- no leaks are possible
   ```
   **Say:** "4 borrows and 4 returns. Three are our mobs. The fourth is
   `printf`'s own memory, which it tidies up by itself."

5. **A leak.** Put `//` in front of the `free_all(mobs);` line, so it
   doesn't happen. Compile, and run with more detail:
   ```
   gcc -g mobs.c -o mobs
   valgrind --leak-check=full ./mobs
   ```
   **They should see**, among the lines:
   ```
   ==18==   total heap usage: 4 allocs, 1 frees, 1,120 bytes allocated
   ==18== 96 (32 direct, 64 indirect) bytes in 1 blocks are definitely lost in loss record 3 of 3
   ==18==    at 0x4846828: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
   ==18==    by 0x1091E9: push_front (mobs.c:12)
   ==18==    by 0x10932C: main (mobs.c:40)
   ```
   **Say:** "A **memory leak**: three mobs were borrowed and never given
   back. Valgrind even says where they were borrowed: line 12, in
   `push_front`. 'Directly' lost is the first mob, which nothing points
   to any more; the other two are lost 'indirectly', through it." Here
   the program ends straight away, and Linux takes all its memory back.
   **Ask:** "Why would a leak matter in a game that runs for hours?"
   *(It would keep borrowing more and more memory, until there was none
   left.)* Take the `//` away again, and commit.

6. **Use after free.** New file, `after.c`:
   ```c
   #include <stdio.h>
   #include <stdlib.h>

   int main(void) {
       int *chest = malloc(3 * sizeof(int));
       chest[0] = 64;
       free(chest);
       printf("The chest held %d\n", chest[0]);
       return 0;
   }
   ```
   Compile and run it normally. **They should see** something like `The
   chest held 839131471`: nonsense, a different number on different
   computers. **Say:** "After `free`, that memory belongs to the heap
   again, and the heap has already scribbled its own notes on it. The
   program didn't crash. It just quietly used the wrong value, which is
   worse." Now with the sanitizer:
   ```
   gcc -g -fsanitize=address after.c -o after
   ./after
   ```
   **They should see** a red report starting:
   ```
   ==47==ERROR: AddressSanitizer: heap-use-after-free on address 0x502000000010 ...
   READ of size 4 at 0x502000000010 thread T0
       #0 0x... in main /home/sam/lab/c/after.c:8
   ```
   **Say:** "Use after free, caught at line 8."

7. **The rules, and why Rust exists.** Write them on paper together:
   - Every `malloc` needs exactly one `free`.
   - Never use memory after freeing it.
   - Never free the same memory twice.
   - Always check for `NULL`.

   **Say:** "C trusts *you* to follow these rules. Real programmers
   break them all the time, and these bugs cause a huge share of security
   problems. Rust, in Stage 9, has an **owner** for every bit of memory,
   and the compiler won't build a program that breaks the rules. You'll
   appreciate that much more now that you've felt these bugs yourself."
   Commit.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `warning: implicit declaration of function ‘malloc’` | `#include <stdlib.h>` is missing | Add it. |
| `error: ‘mob’ is a pointer; did you mean to use ‘->’?` | `mob.health` with a pointer | Use `mob->health`. |
| `valgrind: command not found` | The tools for Stage 8 aren't installed | The guide runs `./scripts/install-packages.sh --later`. |
| Valgrind's report has no line numbers | It was compiled without `-g` | Compile with `-g`. |
| `definitely lost` after the fix | A `free` is still missing, or the old program ran | Compile again, then run valgrind again. |
| The program waits and does nothing | `scanf` is waiting for a number | Type a number and press Enter. |

## Talk about it

- What's the difference between the stack and the heap?
- What do `malloc` and `free` do? What are the four rules?
- What's a memory leak? What's use after free? Which tool catches each?
- How is a C `struct` like a Python class, and how is it different?

## Challenge *(if there's time, or for next time)*

- Add `int length(struct Mob *mob)` and `int total_health(struct Mob
  *mob)` to `mobs.c`, like Lesson 7.11.
- In `after.c`, change the `printf` line to a second `free(chest);`, and
  run it with the sanitizer. What's the error called? *(`double-free`.)*
- Make the chest grow: when it's full, `realloc` it to twice the size.
  That's how Python's lists work inside.

## Checkpoint

The learner can, without help:
- [ ] Use `malloc` and `free`, and explain the stack and the heap
- [ ] Make a `struct`, and use `->` through a pointer
- [ ] Find a leak with valgrind, and use after free with the sanitizer
- [ ] Say the four rules, and why Rust is built around them

## Lab notebook

Draw the three mobs and their arrows. Write the four rules. Copy
valgrind's leak line. Commit. Add *heap*, *malloc*, *free*, *memory
leak*, *use after free* and *struct* to `dictionary.md`.

## Guide's background *(optional reading)*

C has three kinds of memory: **static** (globals, there for the whole
run), the **stack** (local variables, gone when the function returns),
and the **heap** (`malloc`/`free`, under the program's control). The
heap allocator keeps its own bookkeeping, often in the bytes next to and
inside freed blocks, which is why a freed block reads back as nonsense.
In Lesson 8.17 the learner writes the Jack operating system's heap
allocator, `Memory.alloc` and `Memory.deAlloc`, and sees this from the
inside.

**Valgrind** runs the program on a simulated CPU and tracks every
allocation; it's slow (often 20 to 50 times), but needs no recompiling.
**AddressSanitizer** is built in at compile time and is much faster.
Use after free, double free and leaks are a large share of the security
bugs in C and C++ programs, and avoiding them without slowing programs
down is Rust's main design goal.

The `printf` buffer is why valgrind counts one more allocation than the
program makes; its size is 1,024 bytes when the output is a terminal,
and 4,096 when it goes to a file or a pipe, so the "bytes allocated"
number changes with how the program is run.
