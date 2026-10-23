# Lesson 9.13: Traits and Generics

**Time:** 3 sessions of 45 min · **You need:** a terminal; a text
editor; `~/lab/rust` · **New words:** trait, implement, default method,
`Box`, `dyn`, generic, type parameter, trait bound

## Goal *(read this to the learner)*

> Creepers, zombies and spiders are all different, but they're all
> mobs: each has a name and makes a noise. Rust's way of saying "these
> different types can all do the same things" is a **trait**. And
> sometimes you want one function that works for numbers, words *and*
> anything else that can be compared: that's a **generic** function.
> Together they let you write code once and use it for many types.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.

## Warm-up (5 min)

"What does `#[derive(Debug)]` give a struct?" *(The ability to be
printed with `{:?}`.)* "And `PartialEq`?" *(The ability to be compared
with `==`.)* **Say:** "Those are traits. Today you'll make your own."

## Activity

### Session 1: a trait

1. **Three mobs.**
   ```
   cd ~/lab/rust
   cargo new traits
   cd traits
   ```
   ```rust
   trait Mob {
       fn name(&self) -> String;
       fn noise(&self) -> String;
   }

   struct Creeper;

   struct Zombie;

   impl Mob for Creeper {
       fn name(&self) -> String {
           String::from("creeper")
       }

       fn noise(&self) -> String {
           String::from("sssss... BOOM")
       }
   }

   impl Mob for Zombie {
       fn name(&self) -> String {
           String::from("zombie")
       }

       fn noise(&self) -> String {
           String::from("uuurgh")
       }
   }

   fn main() {
       let creeper = Creeper;
       let zombie = Zombie;
       println!("The {} says {}", creeper.name(), creeper.noise());
       println!("The {} says {}", zombie.name(), zombie.noise());
   }
   ```
   **They should see:**
   ```
   The creeper says sssss... BOOM
   The zombie says uuurgh
   ```
   **Say:** "`trait Mob` is a promise: anything that's a `Mob` has a
   `name` and a `noise`. It only lists the methods' first lines. `impl Mob
   for Creeper` keeps the promise for creepers: it **implements** the
   trait. `struct Creeper;` is a struct with no fields at all; it doesn't
   need any yet."

2. **Breaking the promise.** Delete the zombie's `noise` method, and
   `cargo run`. **They should see:**
   ```
   error[E0046]: not all trait items implemented, missing: `noise`
   ```
   **Say:** "Rust holds you to it." Put it back.

### Session 2: default methods, and a Vec of mobs

3. **Defaults.** Add two methods to the trait itself, *with* bodies:
   ```rust
   trait Mob {
       fn name(&self) -> String;
       fn noise(&self) -> String;

       fn health(&self) -> i32 {
           20
       }

       fn describe(&self) -> String {
           format!("The {} ({} health) says \"{}\"", self.name(), self.health(), self.noise())
       }
   }
   ```
   **Say:** "These are **default methods**. Every mob gets them for free,
   and they can use the other methods. `\"` puts a quote mark inside a
   string."

4. **A spider that's different.** Add a third mob:
   ```rust
   struct Spider;

   impl Mob for Spider {
       fn name(&self) -> String {
           String::from("spider")
       }

       fn noise(&self) -> String {
           String::from("hiss")
       }

       fn health(&self) -> i32 {
           16
       }
   }
   ```
   **Say:** "Spiders have less health, so the spider replaces the default
   `health` with its own."

5. **All the mobs together.** Replace `main` with:
   ```rust
   fn main() {
       let mobs: Vec<Box<dyn Mob>> = vec![Box::new(Creeper), Box::new(Zombie), Box::new(Spider)];
       for mob in &mobs {
           println!("{}", mob.describe());
       }
   }
   ```
   **They should see:**
   ```
   The creeper (20 health) says "sssss... BOOM"
   The zombie (20 health) says "uuurgh"
   The spider (16 health) says "hiss"
   ```
   **Say:** "A Vec can only hold one type. But a creeper and a spider are
   different types, and could be different sizes. So each one goes in a
   **`Box`**: a pointer to something on the heap, which is always the
   same size. `dyn Mob` means 'some type that implements `Mob`; we'll
   find out which when the program runs'." Commit.

### Session 3: generics

6. **One function, many types.** Add this function, and three lines at
   the end of `main`:
   ```rust
   fn largest<T: PartialOrd>(items: &[T]) -> &T {
       let mut best = &items[0];
       for item in items {
           if item > best {
               best = item;
           }
       }
       best
   }
   ```
   ```rust
       println!("{}", largest(&[3, 7, 2]));
       println!("{}", largest(&["dirt", "stone", "diamond"]));
       println!("{}", largest(&[2.5, 9.75, 4.0]));
   ```
   **They should see**, after the mobs:
   ```
   7
   stone
   9.75
   ```
   **Say:** "`<T>` makes `largest` **generic**: `T` is a **type
   parameter**, a stand-in for whatever type it's used with: numbers,
   words, decimals. `&[T]` is a slice of a list of `T`s." **Ask:** "Why
   is `stone` the largest word?" *(Words are compared in alphabetical
   order, and `s` comes after `d`.)*

7. **The trait bound.** Take out `: PartialOrd`, so it's just
   `fn largest<T>(...)`, and `cargo run`. **They should see:**
   ```
   error[E0369]: binary operation `>` cannot be applied to type `&T`
   ```
   with a suggestion to restrict `T` with `PartialOrd`. **Say:** "Not
   every type can be compared with `>`. `T: PartialOrd` is a **trait
   bound**: it says 'any type `T`, as long as it implements `PartialOrd`'.
   That's exactly the types that `>` works on." Put it back. Commit.

8. **Rustlings.** A big batch, over several sittings: `generics`,
   `traits`, `quiz3`, `lifetimes` and `tests`. For `lifetimes`,
   **say:** "Lesson 9.5's dangling-reference error asked for a 'lifetime
   specifier'. These exercises show how to write one: `'a` is a name for
   how long a reference lasts."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `error[E0046]: not all trait items implemented, missing: \`noise\`` | An `impl` block leaves out a method the trait needs | Add it. |
| `error[E0369]: binary operation \`>\` cannot be applied to type \`&T\`` | A generic type is compared with no trait bound | `T: PartialOrd`. |
| `error[E0599]: no method named \`describe\` found` | The method isn't in the trait, or the trait isn't implemented for that type | Check the trait, and the `impl Mob for ...`. |
| `error[E0308]: mismatched types` in `vec![...]` of mobs | The Vec's type is missing, so Rust expects every item to be the first one's type | `let mobs: Vec<Box<dyn Mob>> = ...`. |
| `error[E0407]: method \`roar\` is not a member of trait \`Mob\`` | An `impl Mob for` block has an extra method | Put extra methods in a separate `impl Spider` block, or add them to the trait. |

## Talk about it

- What's a trait? How is it like a promise?
- What's a default method? When would a type replace one?
- Why do the mobs need a `Box` to share a Vec?
- What does `<T: PartialOrd>` mean?

## Challenge *(if there's time, or for next time)*

- Add an `Enderman` that says nothing at all (an empty noise), and a
  `describe` of its own that says so.
- Implement `std::fmt::Display` for `Creeper`, so `println!("{}",
  creeper)` works. Read the example in the standard library's docs for
  `Display` (`rustup doc --std`, then search).
- Write a generic `fn smallest<T: PartialOrd>(items: &[T]) -> &T`.

## Checkpoint

The learner can, without help:
- [ ] Define a trait, and implement it for two structs
- [ ] Explain default methods, and replace one
- [ ] Explain `Vec<Box<dyn Mob>>`
- [ ] Write a generic function with a trait bound

## Lab notebook

Draw the trait as a box of method names, with arrows from each mob that
implements it. Draw `Vec<Box<dyn Mob>>`: same-size boxes on the stack,
pointing to different-sized mobs on the heap. Commit. Add *trait*,
*implement*, *default method*, *Box*, *generic* and *trait bound* to
`dictionary.md`.

## Guide's background *(optional reading)*

This follows Chapters 10 and 17 of the Book. Traits are Rust's
interfaces. There are two ways to use them: **generics** (`T:
PartialOrd`), where the compiler makes a separate copy of the function
for each type it's used with (*monomorphisation*: fast, but more code),
and **trait objects** (`dyn Mob`), where one copy of the code looks up
the right method at run time through a table of function pointers (a
*vtable*, much like the Jack compiler's method calls, but with the table
stored next to the pointer).

`Box<T>` is the simplest smart pointer: it owns a value on the heap and
frees it when dropped. The `box`, `rc`, `arc` and `cow` Rustlings in
Lesson 9.18 cover the others.

`largest` panics on an empty slice (`items[0]`). A better version
returns `Option<&T>`: that's a good discussion with an older learner.
