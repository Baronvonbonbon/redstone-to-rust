# Lesson 10.5: Pretend Memory: Address Spaces and Pages

**Time:** 3 sessions of 45 min · **You need:** a terminal; a text
editor; squared paper; `~/lab/os` · **New words:** address space,
virtual address, physical address, page, frame, page table, page fault,
ASLR

## Goal *(read this to the learner)*

> Every program thinks it has the whole memory to itself, starting at
> address 0. That's a trick! The kernel gives each process its own
> **pretend memory**, and secretly maps it, a page at a time, onto the
> real memory chips. You'll catch the trick in action, do the maths the
> CPU does on every memory access, and write a translator of your own.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] Squared paper for Session 2.

## Warm-up (5 min)

"In Hack, where was the screen in memory?" *(16384.)* "If two programs
ran on Hack at once, and both wrote to address 100, what would happen?"
*(They'd overwrite each other.)* "Today: how a real computer stops that."

## Activity

### Session 1: where things live

1. **Print some addresses.**
   ```
   cd ~/lab/os
   cargo new addresses
   cd addresses
   ```
   ```rust
   use std::fs;

   static DIAMONDS: u32 = 64;

   fn main() {
       let torches = 10;
       let chest = Box::new(27);
       println!("The code for main is at  {:p}", main as fn());
       println!("DIAMONDS is at           {:p}", &DIAMONDS);
       println!("The chest (heap) is at   {:p}", chest);
       println!("torches (stack) is at    {:p}", &torches);

       println!();
       println!("My memory map:");
       let maps = fs::read_to_string("/proc/self/maps").unwrap();
       for line in maps.lines() {
           if line.contains("addresses") || line.contains("[heap]") || line.contains("[stack]") {
               println!("{line}");
           }
       }
   }
   ```
   **Say:** "`{:p}` prints where something is in memory: its address, in
   hexadecimal. `Box::new` puts the 27 on the **heap**, which you met in
   Stage 8."
   ```
   cargo build
   ./target/debug/addresses
   ```
   **They should see** something like:
   ```
   The code for main is at  0x65493a141240
   DIAMONDS is at           0x65493a12eb48
   The chest (heap) is at   0x6549511e9d60
   torches (stack) is at    0x7ffffbf456c4

   My memory map:
   65493a127000-65493a13e000 r--p 00000000 00:56 21257785                   /home/sam/lab/os/addresses/target/debug/addresses
   65493a13e000-65493a181000 r-xp 00016000 00:56 21257785                   /home/sam/lab/os/addresses/target/debug/addresses
   65493a181000-65493a185000 r--p 00058000 00:56 21257785                   /home/sam/lab/os/addresses/target/debug/addresses
   65493a185000-65493a187000 rw-p 0005b000 00:56 21257785                   /home/sam/lab/os/addresses/target/debug/addresses
   6549511e9000-65495120a000 rw-p 00000000 00:00 0                          [heap]
   7ffffbf26000-7ffffbf47000 rw-p 00000000 00:00 0                          [stack]
   ```
   **Say:** "Each line of the map is a stretch of this program's memory:
   from one address, to another. `r`, `w` and `x` say whether it can be
   read, written, or run as code." Together, find which stretch each
   address is in. *(`main` is in the `r-xp` one: code can be run.
   `DIAMONDS` is in a read-only one. The chest is in `[heap]`, and
   `torches` in `[stack]`.)*

2. **These numbers are huge.** **Ask:** "`0x7ffffbf456c4` is about 140
   million million. Does this computer have that much memory?" *(No: a
   few thousand million bytes at most.)* **Say:** "So these can't be
   real addresses. They're **virtual addresses**: places in this
   program's own pretend memory, its **address space**."

3. **Run it again.** `./target/debug/addresses` a second time. **They
   should see:** all the addresses are different! **Say:** "The kernel
   puts things in a new, random place each time. It's called **ASLR**
   (address space layout randomisation), and it makes life harder for
   attackers, who'd like to know where things are." Now ask the kernel
   not to:
   ```
   setarch -R ./target/debug/addresses
   setarch -R ./target/debug/addresses
   ```
   **They should see:** the same addresses both times, starting
   `0x55555...` and `0x7ffff...`.

4. **Something never changes.** Look at the last three hex digits of
   `main`'s address in every run. **They should see:** they're always
   the same (`240` above). Same for `DIAMONDS`. **Ask:** "Why?" Leave it
   as a mystery until Session 2.

### Session 2: pages

5. **Pages.** **Say:** "The kernel doesn't map memory a byte at a time:
   that would need a list as big as the memory. It maps it in blocks
   called **pages**." Check how big a page is:
   ```
   getconf PAGESIZE
   ```
   **They should see:** `4096`. **Ask:** "What's 4096 in hex?" *(0x1000:
   it's 16 × 16 × 16.)* **Say:** "So in hex, the last three digits of an
   address say where you are *inside* a page, the **offset**, and the
   rest says *which* page. ASLR moves whole pages, so the offset never
   changes!" That solves the mystery.

6. **A tiny computer, on paper.** **Say:** "Real pages are too big to
   draw. Here's a computer with 16-byte pages, and a program whose
   address space is 64 bytes: 4 pages." Draw the program's 4 pages
   (numbered 0 to 3) on the left, and 8 **frames** of real memory
   (numbered 0 to 7, 16 bytes each) on the right. **Say:** "A page of
   pretend memory lives in a frame of real memory. The **page table**
   says which." Write the page table:

   | Page | Frame |
   |---|---|
   | 0 | 3 |
   | 1 | 7 |
   | 2 | (not there) |
   | 3 | 5 |

   Draw the arrows. **Say:** "To translate an address, the CPU does
   this, for *every* memory access:"
   - page = address ÷ 16 (the whole-number part)
   - offset = address remainder 16
   - look up the page's frame in the table
   - real address = frame × 16 + offset

   Do these together on paper: virtual address 21 *(page 1, offset 5,
   frame 7: 7 × 16 + 5 = 117)*, then 0, 5, 63 and 40. **Ask:** "What
   happens with 40?" *(Page 2 isn't there!)* **Say:** "That's a **page
   fault**. The CPU stops and asks the kernel what to do."

7. **The translator.** In a new project, `paging`:
   ```rust
   const PAGE_SIZE: u32 = 16;

   /// The page table: for each page of the program's pretend memory,
   /// which frame of real memory it lives in (or None if it isn't there).
   const PAGE_TABLE: [Option<u32>; 4] = [Some(3), Some(7), None, Some(5)];

   /// Turns a virtual address into a physical one.
   fn translate(virtual_address: u32) -> Option<u32> {
       let page = virtual_address / PAGE_SIZE;
       let offset = virtual_address % PAGE_SIZE;
       let frame = PAGE_TABLE.get(page as usize).copied().flatten()?;
       Some(frame * PAGE_SIZE + offset)
   }

   fn main() {
       for address in [0, 5, 21, 40, 63, 64] {
           match translate(address) {
               Some(physical) => println!("Virtual {address} is physical {physical}"),
               None => println!("Virtual {address}: PAGE FAULT! That page isn't there."),
           }
       }
   }
   ```
   **Say:** "`get` gives `None` if the page number is past the end of the
   table. `copied().flatten()` turns 'maybe a maybe-frame' into just
   'maybe a frame'. And `?` gives back `None` straight away if there's no
   frame." `cargo run`. **They should see:**
   ```
   Virtual 0 is physical 48
   Virtual 5 is physical 53
   Virtual 21 is physical 117
   Virtual 40: PAGE FAULT! That page isn't there.
   Virtual 63 is physical 95
   Virtual 64: PAGE FAULT! That page isn't there.
   ```
   Check each against the paper. **Ask:** "Why is 64 a page fault?" *(It's
   page 4, past the end of the address space.)* Commit.

### Session 3: page faults

8. **Segmentation fault.** In `~/lab/c`, make `segv.c`:
   ```c
   #include <stdio.h>

   int main(void) {
       int *nowhere = NULL;
       printf("About to look at address 0...\n");
       printf("%d\n", *nowhere);
       return 0;
   }
   ```
   ```
   gcc -Wall -o segv segv.c
   ./segv
   ```
   **They should see:**
   ```
   About to look at address 0...
   Segmentation fault (core dumped)
   ```
   **Say:** "You saw this in Stage 8. Now you know what's going on: page
   0 is never in the page table, on purpose. The CPU has a page fault,
   the kernel sees the program has no business there, and sends it the
   signal `SEGV`, which stops it."

9. **The kernel is lazy (in a good way).** In a new project, `lazy`:
   ```rust
   use std::fs;

   /// How much real memory this process is using, from /proc.
   fn real_memory() -> String {
       let status = fs::read_to_string("/proc/self/status").unwrap();
       let line = status.lines().find(|l| l.starts_with("VmRSS:")).unwrap();
       line.trim_start_matches("VmRSS:").trim().to_string()
   }

   fn main() {
       println!("At the start:              {}", real_memory());
       let mut chest = vec![0u8; 200_000_000];
       println!("After asking for 200 MB:   {}", real_memory());
       for place in (0..chest.len()).step_by(4096) {
           chest[place] = 1;
       }
       println!("After touching every page: {}", real_memory());
   }
   ```
   **Ask** before running: "What will the middle line say?" Then `cargo
   run`. **They should see** something like:
   ```
   At the start:              2040 kB
   After asking for 200 MB:   2048 kB
   After touching every page: 197360 kB
   ```
   **Say:** "Asking for 200 MB used almost no real memory! The kernel
   only promised it: it put the pages in the address space, but not in
   any frames. The first time each page is touched, there's a page
   fault, and the kernel quietly finds a real frame for it. That's a
   *good* page fault." **Ask:** "How many pages did the loop touch?"
   *(200,000,000 ÷ 4096, about 48,829.)* Commit.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `setarch: failed to set personality to (null): Operation not permitted` | Turning off ASLR isn't allowed here (some containers block it) | Run it on the computer itself. |
| The addresses are the same every run, even without `setarch` | ASLR is turned off on this computer | That's fine: skip step 3's first part. |
| `lazy` says the same small number all three times | It was built with `--release`, and the compiler noticed the chest is never read, and left it out | Use `cargo run`, without `--release`. |
| `memory allocation of 200000000 bytes failed` | Not enough free memory | Use a smaller number, like `50_000_000`. |
| `error[E0599]: no method named \`flatten\` found for enum \`Option<&Option<u32>>\`` | `.copied()` is missing, so it's a maybe-*borrowed*-maybe-frame | Copy it exactly: `.get(page as usize).copied().flatten()?`. (Don't follow the compiler's `into_iter` hint here.) |

## Talk about it

- What's an address space? A virtual address? A physical one?
- What does the page table do? Do the translation for address 50 aloud.
- Why do the last three hex digits never change, even with ASLR?
- What are the two kinds of page fault you met: the good one and the
  bad one?

## Challenge *(if there's time, or for next time)*

- Make the translator's page size 32 and its table 2 pages long. Which
  addresses work now?
- The real page table: with 4096-byte pages, which page and offset is
  the address `0x7ffffbf456c4`? *(Just split the hex digits: page
  `0x7ffffbf45`, offset `0x6c4`.)*
- Change `lazy` to touch only every other page (`step_by(8192)`).
  Predict the last number first, then check.

## Checkpoint

The learner can, without help:
- [ ] Explain virtual and physical addresses with the paper drawing
- [ ] Translate an address by hand: page, offset, frame, answer
- [ ] Explain the translator's `translate` function
- [ ] Explain a segmentation fault, and why asking for memory is
      cheaper than using it

## Lab notebook

Stick in the drawing of pages, frames and the page table, with your
working for addresses 21 and 40. Copy the three lines from `lazy`.
Commit. Add *address space*, *virtual address*, *physical address*,
*page*, *frame*, *page table*, *page fault* and *ASLR* to
`dictionary.md`.

## Guide's background *(optional reading)*

This lesson covers OSTEP Chapters 13 ("The Abstraction: Address
Spaces"), 15 ("Address Translation") and 18 ("Paging: Introduction");
the tiny 64-byte address space with 16-byte pages is the textbook's
own example. On a real x86-64 computer, the page table has four (or
five) levels, so that it doesn't need an entry for every one of the 2³⁶
possible pages; a cache in the CPU, the **TLB**, remembers recent
translations so that the table is rarely walked.

The translation formula, real = frame × 16 + offset, is a linear
function, and the stage's maths gate. With page sizes that are powers
of two, dividing and taking remainders is just splitting the binary (or
hex) digits, which is why hardware can do it on every memory access.

`lazy` shows **demand paging**: memory that's asked for is only given
real frames when it's touched. Its last number is a little under
200,000 kB because 200,000,000 bytes is 195,313 kB (1 kB is 1024
bytes). If real memory runs out, the kernel can move pages that haven't
been used lately to the disk (**swap**), which is OSTEP Chapters 21 and
22.
