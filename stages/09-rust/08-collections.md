# Lesson 9.8: Vecs, Strings and HashMaps

**Time:** 2–3 sessions of 45 min · **You need:** a terminal; a text
editor; `~/lab/rust` · **New words:** `Vec`, `HashMap`, key, value,
index, bounds check, module

## Goal *(read this to the learner)*

> Every game needs lists and lookups: the slots in a chest, how many of
> each block you've collected. Rust's **Vec** is a list that can grow,
> and a **HashMap** is like Python's dictionary. You'll fill a chest,
> count your loot, and then try to reach past the end of the chest,
> which in C (Lesson 8.3) quietly overwrote other memory.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.

## Warm-up (5 min)

"In Python, how did you make a list, and add to it?" *(`[1, 2, 3]` and
`.append`.)* "And a dictionary?" *(`{"dirt": 3}`.)* "What happened in C
when you wrote past the end of an array?" *(It overwrote whatever was
next: the overflow.)*

## Activity

### Session 1: Vec

1. **A chest.**
   ```
   cd ~/lab/rust
   cargo new inventory
   cd inventory
   ```
   ```rust
   fn main() {
       let mut chest = vec![10, 20, 30, 40, 50];
       chest.push(60);
       println!("The chest has {} slots: {chest:?}", chest.len());
       println!("Slot 2 holds {}", chest[2]);
   }
   ```
   **They should see:**
   ```
   The chest has 6 slots: [10, 20, 30, 40, 50, 60]
   Slot 2 holds 30
   ```
   **Say:** "`vec![...]` makes a **Vec**, a list that lives on the heap and
   can grow. `push` adds to the end, like Python's `append`. `chest[2]`
   reads by **index**, counting from 0."

2. **Past the end.** Add one more line at the end of `main`:
   ```rust
       println!("Slot 7 holds {}", chest[7]);
   ```
   `cargo run`. **They should see**, after the first two lines:
   ```
   thread 'main' (441) panicked at src/main.rs:6:38:
   index out of bounds: the len is 6 but the index is 7
   ```
   **Say:** "Every time you use `[ ]`, Rust checks the index is inside the
   Vec. That's called a **bounds check**. C didn't check, and overwrote
   other memory. Rust stops, and says exactly what was wrong." Leave the
   line in for now: we'll need it later.

3. **Safer still.** **Say:** "If you don't know whether a slot exists,
   `get` gives back an `Option`." Try it in a new line, just above the
   panic: `println!("{:?} {:?}", chest.get(2), chest.get(7));`. **They
   should see:** `Some(30) None`. Then delete that line.

### Session 2: HashMap

4. **Counting loot.** Change the program to:
   ```rust
   use std::collections::HashMap;

   fn main() {
       let mut chest = vec![10, 20, 30, 40, 50];
       chest.push(60);
       println!("The chest has {} slots: {chest:?}", chest.len());
       println!("Slot 2 holds {}", chest[2]);

       let mut inventory: HashMap<String, u32> = HashMap::new();
       let found = ["dirt", "stone", "dirt", "diamond", "dirt", "stone"];
       for item in found {
           *inventory.entry(item.to_string()).or_insert(0) += 1;
       }
       let mut names: Vec<&String> = inventory.keys().collect();
       names.sort();
       for name in names {
           println!("{name}: {}", inventory[name]);
       }
       match inventory.get("gold") {
           Some(count) => println!("{count} gold"),
           None => println!("No gold yet."),
       }

       println!("Slot 7 holds {}", chest[7]);
   }
   ```
   **They should see:**
   ```
   The chest has 6 slots: [10, 20, 30, 40, 50, 60]
   Slot 2 holds 30
   diamond: 1
   dirt: 3
   stone: 2
   No gold yet.
   ```
   and then the panic from slot 7, now on line 24.

5. **Reading it.**
   - `use std::collections::HashMap;` brings `HashMap` in from the
     standard library's `collections` **module** (a module is a named
     section of code, like a folder).
   - `HashMap<String, u32>`: the **keys** are Strings, the **values** are
     counts.
   - `inventory.entry(...).or_insert(0)` finds the count for that item,
     putting in a 0 first if it isn't there yet. The `*` in front means
     "the number it points to", like C's `*` in Lesson 8.2, so `+= 1`
     adds to the count inside the map.
   - A HashMap has no order, so we collect the keys into a Vec and `sort`
     them, to print them in alphabetical order.
   - `get` gives an `Option`, like the Vec's `get`.

   **Say:** "Remove the last line now, so the program finishes properly."
   Commit.

### Session 3: Strings, and Rustlings

6. **String or &str?** **Say:** "Rust has two kinds of text. A `String`
   is owned, lives on the heap, and can grow. A `&str` is a borrowed
   slice of some text, like `"dirt"` in the program. `.to_string()` makes
   an owned `String` from a `&str`, and `&` borrows a `&str` from a
   String." Write a short table in the notebook:

   | | `String` | `&str` |
   |---|---|---|
   | Owns its text? | Yes | No: it borrows |
   | Can grow? | Yes: `push_str` | No |
   | Example | `String::from("dirt")` | `"dirt"` |

7. **Rustlings.** This is a big batch, so spread it out: `strings`,
   `modules`, `hashmaps`, and `quiz2`. For the `modules` exercises,
   **say:** "`mod` makes a module in your own program, and `pub` makes
   something in it visible from outside. Lesson 9.12 uses them for
   real."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `index out of bounds: the len is 6 but the index is 7` | Reading past the end of a Vec | Use an index less than `len()`, or `get`. |
| `error[E0433]: cannot find type \`HashMap\` in this scope` | `HashMap` wasn't brought in | Add `use std::collections::HashMap;` at the top. |
| `error[E0596]: cannot borrow \`chest\` as mutable` | `push` on a Vec without `mut` | `let mut chest`. |
| `error[E0308]: mismatched types` ... `expected \`String\`, found \`&str\`` | A `"text"` where a `String` is wanted | Add `.to_string()`. |
| A HashMap prints in a strange order | HashMaps have no order | Sort the keys, as in step 4. |

## Talk about it

- What's the difference between a Vec and an array in C?
- What does Rust do when you read past the end of a Vec? What did C do?
- What is a HashMap good for? What does `entry().or_insert()` do?
- What's the difference between `String` and `&str`?

## Challenge *(if there's time, or for next time)*

- Count the letters in a sentence with a HashMap of `char` to `u32`.
  Which letter is most common in a Captain Underpants title?
- `chest.iter().sum::<i32>()` adds up a Vec. What's the total?
- Use `chest.retain(|n| *n > 25)` to keep only the slots over 25. (The
  `|n|` is a closure: Lesson 9.14.)

## Checkpoint

The learner can, without help:
- [ ] Make a Vec, push to it, read by index, and use `get`
- [ ] Explain the bounds check, and compare it with C
- [ ] Count things with a HashMap
- [ ] Explain `String` and `&str`, and finish the Rustlings batch

## Lab notebook

Draw a Vec: a pointer, a length and a capacity on the stack, and the
items on the heap. Copy the `String`/`&str` table. Commit. Add *Vec*,
*HashMap*, *key*, *value*, *bounds check* and *module* to
`dictionary.md`.

## Guide's background *(optional reading)*

This follows Chapter 8 of the Book. A `Vec<T>` is a growable array on
the heap; when it's full, `push` allocates a bigger block (usually
double) and moves the items, which is why pushing is fast on average. A
`String` is a `Vec<u8>` that's guaranteed to hold valid UTF-8 text,
which is why you can't index a String by number (`s[0]`): one letter may
be several bytes. `.chars()` goes through it letter by letter.

`HashMap` uses a hash function to place each key; Rust's default
(SipHash) is designed to resist attackers who craft keys to make it
slow. The bounds check costs a compare and a jump per index, and the
compiler removes it when it can prove the index is in range, such as in
a `for` loop over the Vec itself (Lesson 9.14).
