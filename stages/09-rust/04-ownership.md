# Lesson 9.4: Ownership

**Time:** 2–3 sessions of 45 min · **You need:** a terminal; a text
editor; `~/lab/rust`; a toy or block for each "item", and some sticky
notes · **New words:** ownership, owner, move, clone, copy, scope, drop,
`String`

## Goal *(read this to the learner)*

> In Lesson 8.4, C let you forget to `free` memory (a leak), free it
> twice, and use it after freeing it. Rust has no `free` at all, and
> none of those bugs. The secret is **ownership**: every piece of memory
> has exactly one owner, and when the owner goes away, so does the
> memory. Today you'll act it out, then watch the compiler enforce it.

## Before the lesson *(guide, 15 min)*

- [ ] Read this whole lesson once, including the Guide's background.
- [ ] Gather: two toys or blocks (a "sword" and a "pickaxe"), and sticky
      notes for names.
- [ ] This is the most important idea in Rust. Take it slowly, and
      expect to come back to it.

## Warm-up (5 min)

"In Lesson 8.4, what did `malloc` and `free` do?" *(Asked for memory on
the heap, and gave it back.)* "What went wrong when we forgot?" *(Leaks,
use after free, double free.)*

## Activity

### Session 1: acting it out

1. **The rules.** Write these three on a big sheet:
   1. Each value has one **owner**.
   2. There can only be one owner at a time.
   3. When the owner goes out of **scope** (its `{ }` block ends), the
      value is **dropped**: its memory is freed.

2. **Act it out.** Put a sticky note "sword" on the learner's hand, and
   give them the sword toy. **Say:** "`let sword = ...`: you're the owner."
   Now take the sticky note off, write "chest" on a new one, and hand the
   toy to a teddy (or the guide) with that note. **Say:** "`let chest =
   sword;`. The sword has **moved** to the chest. Is it still in your
   hand?" *(No!)* "So if you try to use `sword` now, there's nothing
   there. Rust won't let you."

   **Ask:** "What if we both wanted one?" **Say:** "Then you'd need a
   second sword: a **clone**. That takes time and materials, so Rust only
   does it when you ask."

3. **In Rust.**
   ```
   cd ~/lab/rust
   cargo new ownership
   cd ownership
   ```
   ```rust
   fn main() {
       let sword = String::from("diamond sword");
       let chest = sword;
       println!("The chest has a {chest}");
   }
   ```
   **They should see:** `The chest has a diamond sword`. **Say:** "A
   **`String`** is text that lives on the heap, like C's `malloc`ed
   strings, so it can grow. `String::from` makes one."

4. **Using a moved value.** Add one more line, after the `println!`:
   ```rust
       println!("I am holding a {sword}");
   ```
   `cargo run`. **They should see:**
   ```
   error[E0382]: borrow of moved value: `sword`
    --> src/main.rs:5:31
     |
   2 |     let sword = String::from("diamond sword");
     |         ----- move occurs because `sword` has type `String`, which does not implement the `Copy` trait
   3 |     let chest = sword;
     |                 ----- value moved here
   4 |     println!("The chest has a {chest}");
   5 |     println!("I am holding a {sword}");
     |                               ^^^^^ value borrowed here after move
   ```
   and a suggestion to use `sword.clone()`. **Say:** "Read it like a
   story: here's where it moved, here's where you tried to use it after.
   This is *use after free*, from Lesson 8.4, caught before the program
   even ran." Delete that line.

### Session 2: clones, copies and functions

5. **Functions take ownership.** Change the program to:
   ```rust
   fn put_in_chest(item: String) {
       println!("Into the chest: {item}");
   }

   fn main() {
       let sword = String::from("diamond sword");
       let chest = sword;
       println!("The chest has a {chest}");

       let pickaxe = String::from("iron pickaxe");
       let spare = pickaxe.clone();
       put_in_chest(pickaxe);
       println!("I still have a spare {spare}");

       let diamonds = 64;
       let more = diamonds;
       println!("{diamonds} and {more}: numbers are copied");
   }
   ```
   **They should see:**
   ```
   The chest has a diamond sword
   Into the chest: iron pickaxe
   I still have a spare iron pickaxe
   64 and 64: numbers are copied
   ```
   **Say:** "Giving a value to a function moves it too. When
   `put_in_chest` ends, `item` goes out of scope, and the pickaxe is
   dropped. `clone` made a whole second string first, so `spare` is still
   ours."

   **Ask:** "Why can we still use `diamonds` after `let more = diamonds`?"
   **Say:** "Small simple values, like numbers, `bool` and `char`, live on
   the stack and are **copied**. Copying 4 bytes is cheap. A `String`
   could be a million bytes, so Rust moves it instead."

6. **Try it.** Add `println!("{pickaxe}");` after `put_in_chest(pickaxe);`.
   **They should see:** `error[E0382]: borrow of moved value: \`pickaxe\``.
   Delete it. Commit.

### Session 3: watching things drop

7. **Torches.** A new project, `cargo new torches`:
   ```rust
   struct Torch {
       name: String,
   }

   impl Drop for Torch {
       fn drop(&mut self) {
           println!("The {} torch burns out.", self.name);
       }
   }

   fn main() {
       let _hall = Torch { name: String::from("hall") };
       {
           let _cave = Torch { name: String::from("cave") };
           println!("Deep in the cave...");
       }
       println!("Back in the hall.");
   }
   ```
   **Say:** "Don't worry about `struct` and `impl` yet: they're Lesson 9.6.
   This makes a `Torch` that prints a message when it's dropped." **Ask:**
   "Predict: in what order will the four lines print?" Write it down, then
   `cargo run`. **They should see:**
   ```
   Deep in the cave...
   The cave torch burns out.
   Back in the hall.
   The hall torch burns out.
   ```
   **Say:** "The cave torch was dropped at the `}` that ended its block.
   The hall torch was dropped at the end of `main`. Rust put in the
   `free` for us, at exactly the right place, every time. No leaks, no
   double frees." Commit.

8. **Rustlings.** Do `vecs1`, `vecs2`, and `move_semantics1` to
   `move_semantics3`.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `error[E0382]: borrow of moved value` | The value moved somewhere else, and was used after | Use the new owner, or `.clone()` it before the move, or borrow it (next lesson). |
| `error[E0382]: use of moved value` | The same, when the value is moved a second time | The same. |
| `warning: unused variable: \`cave\`` | The variable is never used | Start its name with `_`, as in the torches. |
| The torches print in a different order | The `{ }` block is missing or in the wrong place | The cave torch must be inside the inner block. |
| Expected a move error, but it ran | The value was a number, which is copied | Try it with a `String`. |

## Talk about it

- What are the three rules of ownership?
- What's the difference between a move, a clone and a copy?
- Where did Rust put the `free`s in the torches program?
- Which C bugs from Lesson 8.4 can't happen in Rust? Why?

## Challenge *(if there's time, or for next time)*

- Make a function that *gives back* ownership: `fn sharpen(item: String)
  -> String`. Use it as `let sword = sharpen(sword);`.
- Add a third torch in a block inside the cave's block. Predict the order
  first.
- Read Chapter 4.1 of the Book, "What Is Ownership?".

## Checkpoint

The learner can, without help:
- [ ] Say the three rules of ownership
- [ ] Explain a move, a clone and a copy, with the toy or on paper
- [ ] Read a "borrow of moved value" error and fix it
- [ ] Predict when a value is dropped

## Lab notebook

Draw the stack and the heap for `let sword = ...; let chest = sword;`:
two names on the stack, one arrow to the heap, and a cross on the old
one. Write the three rules. Commit. Add *ownership*, *move*, *clone*,
*copy*, *scope* and *drop* to `dictionary.md`.

## Guide's background *(optional reading)*

This follows Chapter 4.1 of the Book. A `String` is three numbers on the
stack (a pointer to the heap, a length and a capacity), plus the bytes on
the heap. `let chest = sword;` copies the three numbers, and marks
`sword` as unusable, so that only one of them will free the heap bytes.
If both could, it would be C's double free. Types that are cheap to copy
and own no heap memory implement the `Copy` trait (Lesson 9.13), and are
copied instead of moved.

The `Drop` trait is Rust's destructor: the compiler inserts the call at
the end of the owner's scope (**RAII**, from C++). That's how files close
themselves, locks unlock themselves and memory frees itself.

Ownership is the idea most people find hardest in Rust. The compiler's
messages are the best teacher: when one appears, read every line of it
aloud together.
