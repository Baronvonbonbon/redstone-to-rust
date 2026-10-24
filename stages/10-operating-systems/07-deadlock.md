# Lesson 10.7: Stuck for Ever: Deadlock

**Time:** 2 sessions of 45 min · **You need:** a terminal; a text
editor; two toys (a "pickaxe" and a "torch"), then five pencils and
five chairs or cushions; `~/lab/os` · **New words:** deadlock, lock
ordering, the dining philosophers

## Goal *(read this to the learner)*

> Locks fix races. But locks bring a new danger: two threads, each
> holding one thing and waiting for the other's, for ever. That's a
> **deadlock**. You'll cause one, find it, and fix it with one simple
> rule, and then solve a famous puzzle from 1965.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] Two toys to be the pickaxe and the torch. For Session 2: five
      pencils (pickaxes) and five places round a table.

## Warm-up (5 min)

"What does a `Mutex` do?" *(Only one thread can hold it at a time;
others wait.)* "What if the thread holding it never lets go?" *(The
others wait for ever.)*

## Activity

### Session 1: Alex and Steve

1. **Act it out.** The learner is Alex, you are Steve. **Say:** "To mine,
   you need both the pickaxe and the torch. Alex, grab the pickaxe. I'll
   grab the torch. Now each of us waits for the other's... and we're
   polite, so we never give ours up." Wait, silently, for a long time.
   **Ask:** "When does this end?" *(Never!)* **Say:** "That's a
   **deadlock**."

2. **In Rust.**
   ```
   cd ~/lab/os
   cargo new deadlock
   cd deadlock
   ```
   ```rust
   use std::sync::{Arc, Mutex};
   use std::thread;
   use std::time::Duration;

   fn main() {
       let pickaxe = Arc::new(Mutex::new("pickaxe"));
       let torch = Arc::new(Mutex::new("torch"));

       let (p, t) = (Arc::clone(&pickaxe), Arc::clone(&torch));
       let alex = thread::spawn(move || {
           let _pickaxe = p.lock().unwrap();
           println!("Alex has the pickaxe, and wants the torch...");
           thread::sleep(Duration::from_millis(100));
           let _torch = t.lock().unwrap();
           println!("Alex is mining!");
       });

       let (p, t) = (Arc::clone(&pickaxe), Arc::clone(&torch));
       let steve = thread::spawn(move || {
           let _torch = t.lock().unwrap();
           println!("Steve has the torch, and wants the pickaxe...");
           thread::sleep(Duration::from_millis(100));
           let _pickaxe = p.lock().unwrap();
           println!("Steve is mining!");
       });

       alex.join().unwrap();
       steve.join().unwrap();
       println!("Both of them finished mining.");
   }
   ```
   **Say:** "The `sleep` is to make sure both grab their first thing
   before either grabs the second, like in our act-out. Without it, the
   deadlock would only happen sometimes, which is worse: a bug that
   hides." `cargo run`. **They should see:**
   ```
   Alex has the pickaxe, and wants the torch...
   Steve has the torch, and wants the pickaxe...
   ```
   and then nothing, for ever. (The two lines can come in either order.)

3. **Looking at a stuck program.** Leave it running. In a second
   terminal:
   ```
   ps -L -o pid,lwp,stat,pcpu,comm -C deadlock
   ```
   **They should see** three lines, one for each thread (`LWP` is the
   thread's own number), each with `STAT` `Sl` and `%CPU` `0.0`.
   **Say:** "Three threads: `main`, waiting in `join`, and Alex and
   Steve, each waiting for a lock. `S` means sleeping. They aren't busy;
   they're stuck, using no CPU at all, for ever." Go back to the first
   terminal and press Ctrl+C.

4. **The fix: always in the same order.** **Ask:** "How could Alex and
   Steve agree, so this can't happen?" Let them think. *(If both always
   pick up the pickaxe first, whoever gets it will get the torch too:
   the other is still waiting for the pickaxe, holding nothing.)* Act
   it out with that rule. Then change Steve's thread so he takes the
   pickaxe first:
   ```rust
           let _pickaxe = p.lock().unwrap();
           println!("Steve has the pickaxe, and wants the torch...");
           thread::sleep(Duration::from_millis(100));
           let _torch = t.lock().unwrap();
   ```
   `cargo run`. **They should see** something like:
   ```
   Alex has the pickaxe, and wants the torch...
   Alex is mining!
   Steve has the pickaxe, and wants the torch...
   Steve is mining!
   Both of them finished mining.
   ```
   **Say:** "That's **lock ordering**: give every lock a place in a line,
   and always take them in that order. Then a circle of waiting can't
   happen." Commit.

### Session 2: the miners' table

5. **The puzzle.** Set five places round a table, with one pencil (a
   pickaxe) *between* each pair of places. **Say:** "This is a famous
   puzzle, from 1965. It's usually about philosophers eating with
   chopsticks; ours are miners. To mine, a miner needs *both* pickaxes
   next to them: left and right. Then they put them down and rest."
   Number the places 0 to 4, and the pickaxes 0 to 4: pickaxe *n* is on
   miner *n*'s left, so miner *n*'s right one is pickaxe *n* + 1 (and
   miner 4's right one is pickaxe 0). Walk round the table: if every
   miner picks up their left pickaxe at once, what happens? *(Every
   pickaxe is taken, and everyone waits for their right one: deadlock.)*

6. **The table, in Rust.** A new project, `table`:
   ```rust
   use std::sync::{Arc, Mutex};
   use std::thread;
   use std::time::Duration;

   fn main() {
       let pickaxes: Vec<Arc<Mutex<()>>> = (0..5).map(|_| Arc::new(Mutex::new(()))).collect();
       let mut miners = Vec::new();
       for miner in 0..5 {
           let left = miner;
           let right = (miner + 1) % 5;
           let first = Arc::clone(&pickaxes[left]);
           let second = Arc::clone(&pickaxes[right]);
           miners.push(thread::spawn(move || {
               for _ in 0..3 {
                   let _first = first.lock().unwrap();
                   thread::sleep(Duration::from_millis(10));
                   let _second = second.lock().unwrap();
                   println!("Miner {miner} is mining with pickaxes {left} and {right}");
               }
           }));
       }
       for miner in miners {
           miner.join().unwrap();
       }
       println!("Everyone has finished.");
   }
   ```
   **Say:** "`Mutex<()>` is a lock with nothing inside: the pickaxe
   itself is the thing. `% 5` is the remainder, so after pickaxe 4 comes
   pickaxe 0: it goes round the table." **Ask:** "What will happen?"
   `cargo run`. **They should see:** nothing at all. Every miner took
   their left pickaxe. Ctrl+C.

7. **Fix it with lock ordering.** **Ask:** "What's the rule from Session
   1, for pickaxes with numbers?" *(Always pick up the lower-numbered one
   first.)* Change the two `Arc::clone` lines:
   ```rust
           let first = Arc::clone(&pickaxes[left.min(right)]);
           let second = Arc::clone(&pickaxes[left.max(right)]);
   ```
   **Ask:** "Which miner does this change?" *(Only miner 4: their
   pickaxes are 4 and 0, so now they reach for 0 first.)* `cargo run`.
   **They should see** fifteen lines of mining, in a muddled order, and
   then `Everyone has finished.` Act it out round the table with the new
   rule: miner 4 reaches right first, and the circle is broken. Commit.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| The fixed program still hangs | One thread still takes the torch (or the higher pickaxe) first | Check every thread takes the locks in the same order. |
| `ps` shows nothing for `-C deadlock` | The program isn't running, or has another name | Run it in the other terminal first; the name is the project's. |
| `error[E0382]: the type \`Arc\` does not implement \`Copy\`` | Both threads used the same clones, `p` and `t`, but the first thread took them | Each thread needs its own `let (p, t) = (...)` line just before it. |
| The deadlock version finishes sometimes | The `sleep` was removed or shortened | Put the 100 ms (or 10 ms) sleep back: it makes the bad timing happen every time. |

## Talk about it

- What's a deadlock? What has to happen for one? *(Each holds
  something, and waits for something another holds, in a circle.)*
- Why is the `sleep` there? Why are bugs that only *sometimes* happen
  so hard?
- What's lock ordering? Why does it break the circle?
- Why does changing only miner 4 fix the whole table?

## Challenge *(if there's time, or for next time)*

- Another fix for the table: a "host" lets only four miners sit down at
  once. Act it out. Why does it work?
- Make each miner count how many times they mined, and print the totals
  at the end. Is it fair?
- Find `try_lock` in `rustup doc --std` (search `Mutex`). How could it
  help a miner who can't get their second pickaxe?

## Checkpoint

The learner can, without help:
- [ ] Cause a deadlock, and explain it with the toys
- [ ] Find the stuck threads with `ps -L`
- [ ] Fix a deadlock with lock ordering
- [ ] Explain the miners' table, and why miner 4's change fixes it

## Lab notebook

Draw the table: five miners, five pickaxes, with the arrows of who's
waiting for whom in the deadlock (a circle!). Then draw it again with
the fix. Commit. Add *deadlock*, *lock ordering* and *the dining
philosophers* to `dictionary.md`.

## Guide's background *(optional reading)*

This is OSTEP Chapter 32, "Common Concurrency Problems", and the
dining philosophers from Chapter 31. The puzzle was set by Edsger
Dijkstra in 1965 (as an exam question!) and given its philosophers by
Tony Hoare.

A deadlock needs four things at once, called the Coffman conditions:
**mutual exclusion** (only one holder), **hold and wait** (holding one
thing while waiting for another), **no preemption** (nobody can take a
lock away), and **circular wait**. Breaking any one prevents deadlock;
lock ordering breaks the circle, and the challenge's "host" breaks it by
never letting all five hold one each.

Rust prevents data races at compile time, but not deadlocks: both
programs here are perfectly safe Rust. Real systems find deadlocks with
tools and careful design; the Linux kernel has a checker called
`lockdep` that warns when two locks are ever taken in different orders.
