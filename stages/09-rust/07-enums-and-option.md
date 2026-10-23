# Lesson 9.7: Enums, Match and Option

**Time:** 2 sessions of 45 min · **You need:** a terminal; a text
editor; `~/lab/rust` · **New words:** enum, variant, `match`, pattern,
exhaustive, `Option`, `Some`, `None`, null

## Goal *(read this to the learner)*

> A block in your world is air, or dirt, or stone, or water, or lava:
> exactly one of those, never two, never something else. Rust has a
> type for exactly that, the **enum**, and a way to handle every case
> that won't let you forget one: `match`. You'll also meet `Option`,
> Rust's answer to the crash you caused in Lesson 8.3 with a null
> pointer.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.

## Warm-up (5 min)

"In Lesson 8.3, what happened when a program used a null pointer?" *(It
crashed: a segmentation fault.)* **Say:** "The man who invented null
pointers called them his 'billion-dollar mistake'. Rust doesn't have
them. Let's see what it has instead."

## Activity

### Session 1: an enum and match

1. **The blocks.**
   ```
   cd ~/lab/rust
   cargo new blocks
   cd blocks
   ```
   ```rust
   #[derive(Debug, Clone, Copy, PartialEq)]
   enum Block {
       Air,
       Dirt,
       Stone,
       Water,
       Lava,
   }

   impl Block {
       fn can_walk_through(self) -> bool {
           match self {
               Block::Air | Block::Water => true,
               Block::Dirt | Block::Stone | Block::Lava => false,
           }
       }
   }

   fn main() {
       let here = Block::Water;
       println!("{here:?}: walk through? {}", here.can_walk_through());
       let there = Block::Stone;
       println!("{there:?}: walk through? {}", there.can_walk_through());
   }
   ```
   **They should see:**
   ```
   Water: walk through? true
   Stone: walk through? false
   ```
   (There's also a warning that some variants are never constructed:
   that's fine, they're used later.)
   **Say:** "An **enum** lists every possible value. Each one is a
   **variant**. A `Block` is always exactly one of the five. `match` is
   like a row of ifs: each line is a **pattern**, then `=>`, then the
   answer. `|` means *or*. The `derive` line lets blocks be printed,
   copied, and compared with `==`."

2. **Forgetting one.** Take `| Block::Lava` out of the second arm, and
   `cargo run`. **They should see:**
   ```
   error[E0004]: non-exhaustive patterns: `Block::Lava` not covered
   ```
   **Say:** "A `match` must be **exhaustive**: it must handle every
   possibility. If you add a new block one day, say `Block::Ice`, Rust
   will show you every `match` that needs to know about it. In Python,
   you'd find out when the program went wrong." Put `Lava` back.

### Session 2: Option

3. **Maybe a value.** **Say:** "Sometimes there might be a value, or
   might not. 'Which block is this letter?' has no answer for `?`. In C,
   you'd return a null pointer and hope people check it. Rust has an
   enum for it":
   ```rust
   enum Option<T> {
       Some(T),
       None,
   }
   ```
   **Say:** "It's already built in. Either `Some(something)`, with the
   value inside, or `None`. You can't use the value without opening the
   box and checking which it is."

4. **The whole program.** Replace `main.rs` with:
   ```rust
   #[derive(Debug, Clone, Copy, PartialEq)]
   enum Block {
       Air,
       Dirt,
       Stone,
       Water,
       Lava,
   }

   impl Block {
       fn from_char(c: char) -> Option<Block> {
           match c {
               '.' => Some(Block::Air),
               'd' => Some(Block::Dirt),
               '#' => Some(Block::Stone),
               '~' => Some(Block::Water),
               '!' => Some(Block::Lava),
               _ => None,
           }
       }

       fn can_walk_through(self) -> bool {
           match self {
               Block::Air | Block::Water => true,
               Block::Dirt | Block::Stone | Block::Lava => false,
           }
       }

       fn seconds_to_mine(self) -> Option<u32> {
           match self {
               Block::Dirt => Some(1),
               Block::Stone => Some(8),
               Block::Air | Block::Water | Block::Lava => None,
           }
       }
   }

   fn main() {
       let row = ".d#~!?";
       for c in row.chars() {
           match Block::from_char(c) {
               Some(block) => {
                   print!("{c} is {block:?}. Walk through? {}. ", block.can_walk_through());
                   match block.seconds_to_mine() {
                       Some(seconds) => println!("Mining takes {seconds} s."),
                       None => println!("Can't be mined."),
                   }
               }
               None => println!("{c} isn't a block I know."),
           }
       }
   }
   ```
   **They should see:**
   ```
   . is Air. Walk through? true. Can't be mined.
   d is Dirt. Walk through? false. Mining takes 1 s.
   # is Stone. Walk through? false. Mining takes 8 s.
   ~ is Water. Walk through? true. Can't be mined.
   ! is Lava. Walk through? false. Can't be mined.
   ? isn't a block I know.
   ```

5. **Reading it.**
   - `_ => None`: `_` matches anything that's left. **Ask:** "Why does
     `from_char` need it, when `can_walk_through` didn't?" *(There are
     only five blocks, but there are thousands of possible characters.)*
   - `Some(block) =>` opens the box and names what's inside `block`.
   - `print!` (no `ln`) prints without starting a new line.
   - `row.chars()` goes through the string one character at a time.

   **Ask:** "What if we wrote `Block::from_char(c).can_walk_through()`?"
   Try it. **They should see:** `error[E0599]: no method named
   \`can_walk_through\` found for enum \`Option<T>\``. **Say:** "Rust won't
   let you use the block until you've checked it's really there. That's
   what makes null-pointer crashes impossible." Undo it. Commit.

6. **Rustlings.** Do the `enums` exercises (1 to 3).

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `error[E0004]: non-exhaustive patterns` | A `match` doesn't handle every case | Add the missing variant, or a `_ =>` arm. |
| `error[E0599]: no method named ... found for enum \`Option<T>\`` | Using the value without checking it's `Some` | `match` on it first. |
| `error[E0308]: mismatched types` ... `expected \`Option<Block>\`, found \`Block\`` | Returning a block from `from_char` without `Some(...)` | Wrap it: `Some(Block::Air)`. |
| `error[E0425]: cannot find value \`Air\`` | A variant without the enum's name | `Block::Air`. |
| `warning: unreachable pattern` | An arm after `_ =>` can never match | Put `_` last. |

## Talk about it

- What's an enum? How is it different from a struct?
- Why must a `match` be exhaustive? How does that help when the program
  changes?
- What is `Option`? Why is it better than a null pointer?
- What does `_` mean in a pattern?

## Challenge *(if there's time, or for next time)*

- Add `Block::Diamond` (letter `*`, 15 seconds to mine), and follow the
  compiler's errors to every place that needs it.
- Read a whole map, several rows of characters, and count the blocks you
  can walk through.
- Variants can carry data: `enum Item { Sword(u32), Food { hunger: u32 },
  Nothing }`. Write a `match` that prints each kind.

## Checkpoint

The learner can, without help:
- [ ] Define an enum, and `match` on it
- [ ] Explain "exhaustive", and fix an E0004 error
- [ ] Use `Option`, with `Some` and `None`, and explain why Rust has no
      null
- [ ] Finish the `enums` Rustlings

## Lab notebook

Draw `Option<Block>` as a box that's either empty or holds a block.
Write the five blocks and what `can_walk_through` says for each. Commit.
Add *enum*, *variant*, *match*, *pattern*, *exhaustive* and *Option* to
`dictionary.md`.

## Guide's background *(optional reading)*

This follows Chapter 6 of the Book. Rust's enums are **sum types**
(**tagged unions**): each value carries a tag saying which variant it
is, plus that variant's data. Combined with exhaustive `match`, they
replace null pointers (`Option`), error codes (`Result`, Lesson 9.9) and
many uses of inheritance. Tony Hoare called null references his
"billion-dollar mistake" in a 2009 talk.

`Option<&T>` is the same size as a plain pointer: Rust uses the null
address to mean `None`, so the safety costs nothing at run time.
