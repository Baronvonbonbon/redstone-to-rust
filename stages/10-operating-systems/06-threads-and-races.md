# Lesson 10.6: Threads, and the Lost Diamonds

**Time:** 2–3 sessions of 45 min · **You need:** a terminal; a text
editor; a whiteboard or a sheet of paper and two pens; `~/lab/os` ·
**New words:** thread, `spawn`, `join`, race condition, atomic, lock,
`Mutex`, `Arc`

## Goal *(read this to the learner)*

> One process can do several things at once, with **threads**: workers
> that share the same memory. Sharing is fast, but dangerous. You'll
> make four threads count to four million together, watch them lose
> more than half the count, and fix it two ways. You'll also see why
> Rust's borrowing rule turns out to be exactly what threads need.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] A whiteboard (or paper) with a tally number on it, and two pens,
      for the act-out in step 4.

## Warm-up (5 min)

"In the scheduler lesson, the CPU took turns between jobs. How many
CPUs does this computer have?" *(Lesson 10.1: count the `model name`
lines, or run `nproc`.)* "So how many things can it *really* do at
once?" *(That many.)*

## Activity

### Session 1: threads

1. **Three miners.**
   ```
   cd ~/lab/os
   cargo new miners
   cd miners
   ```
   ```rust
   use std::thread;
   use std::time::Duration;

   fn main() {
       let mut miners = Vec::new();
       for number in 1..=3 {
           miners.push(thread::spawn(move || {
               for block in 1..=3 {
                   println!("Miner {number} dug block {block}");
                   thread::sleep(Duration::from_millis(10));
               }
           }));
       }
       for miner in miners {
           miner.join().unwrap();
       }
       println!("All the miners are back.");
   }
   ```
   `cargo run`. **They should see** each miner dig block 1, then each
   dig block 2, then block 3, and `All the miners are back.` at the end:
   ```
   Miner 1 dug block 1
   Miner 2 dug block 1
   Miner 3 dug block 1
   Miner 1 dug block 2
   ...
   ```
   (The order inside each round can change from run to run.)

2. **What happened?** **Say:**
   - "`thread::spawn` starts a **thread**: a new worker inside this same
     process, running the closure. Now four things are running: three
     miners, and `main`."
   - "`move` gives each thread its own copy of `number`."
   - "`join` waits for a thread to finish, like `wait` for a process."
   - "Threads are like processes, but they share one address space:
     the same memory. That makes sharing data easy. Too easy."

   **Ask:** "What happens if `main` doesn't wait?" Delete the `for
   miner in miners` loop (three lines), and run it a few times. **They
   should see:** only some of the miners' lines, or none: `main`
   finished, and when `main` ends, the whole process ends, threads and
   all. Put the loop back.

3. **Without `move`.** Delete `move`, and `cargo build`. **They should
   see:**
   ```
   error[E0373]: closure may outlive the current function, but it borrows `number`, which is owned by the current function
   ```
   with a `help:` that says to use the `move` keyword. **Say:** "A thread
   might keep running after the loop has moved on, and `number` would be
   gone. Rust won't let a thread borrow something that might disappear."
   Put `move` back. Commit.

### Session 2: the race

4. **Act it out.** Write `5` on the board. **Say:** "We're two threads,
   and our job is to add one to the tally, ten times each. Adding one
   takes two steps: **read** the number, then **write** the number plus
   one." Do it slowly, together, but interleave on purpose: you both
   read 5, you both write 6. **Ask:** "Two of us added one. How much did
   it go up?" *(One: an add was lost!)* **Say:** "That's a **race
   condition**: the answer depends on who gets there first."

5. **The race, in Rust.** A new project, `race`:
   ```rust
   use std::sync::atomic::{AtomicU32, Ordering};
   use std::thread;

   static COUNT: AtomicU32 = AtomicU32::new(0);

   fn main() {
       let mut workers = Vec::new();
       for _ in 0..4 {
           workers.push(thread::spawn(|| {
               for _ in 0..1_000_000 {
                   let now = COUNT.load(Ordering::SeqCst);
                   COUNT.store(now + 1, Ordering::SeqCst);
               }
           }));
       }
       for worker in workers {
           worker.join().unwrap();
       }
       let count = COUNT.load(Ordering::SeqCst);
       println!("Count: {count} (it should be 4000000)");
   }
   ```
   **Say:** "`COUNT` is shared by all four threads. An **atomic** number
   is one where each single step, a `load` (read) or a `store` (write),
   happens all at once, so it can't be half done. But we do *two* steps,
   just like on the board." `cargo run` three times. **They should see**
   something like:
   ```
   Count: 1601499 (it should be 4000000)
   Count: 1725869 (it should be 4000000)
   Count: 1660691 (it should be 4000000)
   ```
   **Ask:** "How many adds were lost?" *(More than half!)* "Why is it
   different every time?" *(It depends on exactly when the kernel runs
   each thread, which is never the same twice.)*

6. **Fix 1: one step.** Replace the two lines inside the loop with:
   ```rust
                   COUNT.fetch_add(1, Ordering::SeqCst);
   ```
   `cargo run`. **They should see:** `Count: 4000000 (it should be
   4000000)`, every time. **Say:** "`fetch_add` reads and writes in one
   step that nobody can get in the middle of. The CPU has a special
   instruction for it." Commit.

### Session 3: the borrow checker, and locks

7. **Can't Rust just stop this?** It does, for ordinary variables. A
   new project, `borrow`:
   ```rust
   use std::thread;

   fn main() {
       let mut count = 0;
       thread::scope(|s| {
           s.spawn(|| count += 1);
           s.spawn(|| count += 1);
       });
       println!("Count: {count}");
   }
   ```
   `cargo build`. **They should see:**
   ```
   error[E0499]: cannot borrow `count` as mutable more than once at a time
   ```
   with arrows to `first mutable borrow occurs here` and `second mutable
   borrow occurs here`. **Say:** "`thread::scope` promises that the
   threads finish before the function goes on, so borrowing is fine.
   But remember Lesson 9.5's rule: many readers, *or* one writer. Two
   threads both changing `count` is two writers. The rule you learned
   for borrowing books is exactly the rule that stops races!" **Say:**
   "That's why the race needed a `static` atomic: it's one of the few
   ways to share a number without asking the borrow checker."

8. **Fix 2: a lock.** A new project, `locked`:
   ```rust
   use std::sync::{Arc, Mutex};
   use std::thread;

   fn main() {
       let count = Arc::new(Mutex::new(0));
       let mut workers = Vec::new();
       for _ in 0..4 {
           let count = Arc::clone(&count);
           workers.push(thread::spawn(move || {
               for _ in 0..1_000_000 {
                   let mut number = count.lock().unwrap();
                   *number += 1;
               }
           }));
       }
       for worker in workers {
           worker.join().unwrap();
       }
       println!("Count: {} (it should be 4000000)", *count.lock().unwrap());
   }
   ```
   **Say:**
   - "A `Mutex` (mutual exclusion) is a **lock**, like a talking stick:
     only the thread holding it can touch the number inside. `lock()`
     waits until it's free."
   - "When `number` goes out of scope at the end of the loop, the lock
     is let go by itself: that's `drop`, from Lesson 9.4."
   - "`Arc` lets several threads own the same thing. (It's the `Rc` from
     Rustlings, made safe for threads.)"

   `cargo run`. **They should see:** `Count: 4000000 (it should be
   4000000)`. Try `time cargo run` against the race version. **Ask:**
   "Which is slower?" *(The lock: the threads spend time waiting for
   each other.)* Commit.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `error[E0373]: closure may outlive the current function, but it borrows ...` | The thread borrows something that might disappear | Add `move` before the closure. |
| `Count: 4000000` even for the race | A computer with only one CPU, or very lucky timing | Run it a few more times; try `0..8` threads. |
| `error[E0599]: no method named \`lock\` found for struct \`Arc<{integer}>\`` | `count` isn't a `Mutex` | Check `Arc::new(Mutex::new(0))`. |
| `error[E0368]: binary assignment operation \`+=\` cannot be applied to type \`std::sync::MutexGuard<'_, {integer}>\`` | The `*` is missing: `number` is the lock's guard, not the number | Use `*number += 1;` exactly. |
| `error[E0382]: the type \`Arc\` does not implement \`Copy\`` | The `Arc` was moved into the first thread, so the others can't have it | Clone it for each thread, inside the loop: `let count = Arc::clone(&count);`. |

## Talk about it

- What's a thread? How is it different from a process?
- What's a race condition? Act it out again, with three people.
- Two ways to fix it: what are they, and which is faster?
- How is Rust's borrowing rule like a lock?

## Challenge *(if there's time, or for next time)*

- In `race`, try 2 threads, then 8. Does more threads lose more?
- Use `fetch_add` and `Ordering::Relaxed` instead of `SeqCst`. Still
  right? Faster? *(Look up `Ordering` in `rustup doc --std`.)*
- Change `locked` to count diamonds found by name, in a
  `Mutex<HashMap<String, u32>>`.

## Checkpoint

The learner can, without help:
- [ ] Start threads with `spawn` and wait for them with `join`
- [ ] Explain a race condition with the tally act-out
- [ ] Fix a race with `fetch_add`, and with a `Mutex`
- [ ] Explain how "many readers or one writer" stops races

## Lab notebook

Draw the race on the tally board: two threads, read, read, write,
write. Write the three wrong counts and the right one. Commit. Add
*thread*, *race condition*, *atomic*, *lock*, *Mutex* and *Arc* to
`dictionary.md`.

## Guide's background *(optional reading)*

This is OSTEP Chapters 26 to 28: "Concurrency: An Introduction", the
thread API, and locks. OSTEP's first concurrency example is this same
counter, in C with plain variables, where the lost updates are just as
bad. In C, nothing stops you; in Rust, a plain shared variable doesn't
compile (step 7), so we needed an atomic `static` to show the bug. The
separate `load` and `store` are each safe, but the pair isn't, which is
the heart of every race: a check and an action that should have been
one step.

`fetch_add` compiles to a single CPU instruction with a `lock` prefix,
which stops other cores touching that memory until it's done. A `Mutex`
is built from such instructions, plus a way to put waiting threads to
sleep (on Linux, the `futex` system call). The `Arc` is needed because
`thread::spawn` threads might outlive `main`'s variables; with
`thread::scope` (step 7) a plain reference to a `Mutex` would do.

Rust's promise is called **fearless concurrency**: safe Rust code can't
have a data race at all. It can still have other concurrency bugs, like
the deadlock in the next lesson.
