# Lesson 9.6: Structs and Methods

**Time:** 2 sessions of 45 min · **You need:** a terminal; a text
editor; `~/lab/rust`; squared paper · **New words:** struct, field,
method, `impl`, `self`, associated function, derive

## Goal *(read this to the learner)*

> A creeper has a name, some health, and a place in the world. In Python
> and Jack you made classes for things like that. In Rust, you make a
> **struct** for the data, and an `impl` block for what it can do.
> You'll build a `Mob` that can be hit, can die, and can tell how far
> away another mob is.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.

## Warm-up (5 min)

"In Lesson 8.12, what did Diamond Dash's `Player` class hold?" *(Its x
and y, and so on.)* "In Lesson 8.4, what did a C `struct` hold?" *(Named
fields, side by side in memory.)*

## Activity

### Session 1: a struct

1. **The data.**
   ```
   cd ~/lab/rust
   cargo new mobs
   cd mobs
   ```
   ```rust
   #[derive(Debug)]
   struct Mob {
       name: String,
       health: i32,
       x: i32,
       y: i32,
   }

   fn main() {
       let creeper = Mob {
           name: String::from("creeper"),
           health: 20,
           x: 3,
           y: 4,
       };
       println!("{creeper:?}");
       println!("The {} is at {}, {}", creeper.name, creeper.x, creeper.y);
   }
   ```
   **They should see:**
   ```
   Mob { name: "creeper", health: 20, x: 3, y: 4 }
   The creeper is at 3, 4
   ```
   and a warning above them, `field \`health\` is never read`: that's
   fine, the methods in Session 2 will read it.
   **Say:** "A **struct** groups **fields** together, like a C struct.
   `creeper.name` reads one field. `#[derive(Debug)]` asks Rust to write
   the code for printing the whole thing with `{:?}`, for debugging. That
   writing-code-for-you is called **deriving**."

2. **Every field.** Take out the `health: 20,` line. `cargo run`.
   **They should see:**
   ```
   error[E0063]: missing field `health` in initializer of `Mob`
   ```
   **Say:** "In C, a field you forgot would just be whatever junk was in
   memory. Rust insists on all of them." Put it back.

### Session 2: methods

3. **An `impl` block.** Replace the whole of `main.rs` with this. The
   struct is the same; the `impl` block is new.
   ```rust
   #[derive(Debug)]
   struct Mob {
       name: String,
       health: i32,
       x: i32,
       y: i32,
   }

   impl Mob {
       fn new(name: &str, x: i32, y: i32) -> Mob {
           Mob {
               name: name.to_string(),
               health: 20,
               x,
               y,
           }
       }

       fn hit(&mut self, damage: i32) {
           self.health = (self.health - damage).max(0);
       }

       fn is_alive(&self) -> bool {
           self.health > 0
       }

       fn distance_to(&self, other: &Mob) -> i32 {
           (self.x - other.x).abs() + (self.y - other.y).abs()
       }
   }

   fn main() {
       let mut creeper = Mob::new("creeper", 3, 4);
       let zombie = Mob::new("zombie", 10, 1);
       println!("{creeper:?}");
       creeper.hit(7);
       println!("{} has {} health", creeper.name, creeper.health);
       creeper.hit(50);
       println!("Is the {} alive? {}", creeper.name, creeper.is_alive());
       println!("The {} is {} blocks from the {}", zombie.name, zombie.distance_to(&creeper), creeper.name);
       println!("{zombie:#?}");
   }
   ```
   **They should see:**
   ```
   Mob { name: "creeper", health: 20, x: 3, y: 4 }
   creeper has 13 health
   Is the creeper alive? false
   The zombie is 10 blocks from the creeper
   Mob {
       name: "zombie",
       health: 20,
       x: 10,
       y: 1,
   }
   ```

4. **Reading it.** Go through the `impl` block together:
   - `new` has no `self`: it's an **associated function**, called with
     `Mob::new(...)`, like Jack's constructors. `new` is only a habit;
     Rust has no special constructors. `x, y` is short for `x: x, y: y`.
   - `hit(&mut self, ...)` is a **method** that changes the mob, so it
     borrows it with `&mut`. `.max(0)` stops health going below 0.
   - `is_alive(&self)` only looks, so `&self` is enough.
   - `distance_to` borrows *two* mobs to look at. **Ask:** "How far is
     the zombie, counting blocks, if you can only walk along rows and
     columns?" Draw them on squared paper at (3, 4) and (10, 1) and
     count: 7 across and 3 down. *(10.)* That's called the **Manhattan
     distance**, like walking round city blocks.
   - `{zombie:#?}` prints the debug view spread over several lines.

5. **`mut` matters.** Change `let mut creeper` to `let creeper`.
   `cargo run`. **They should see:**
   ```
   error[E0596]: cannot borrow `creeper` as mutable, as it is not declared as mutable
   ```
   **Say:** "`hit` needs `&mut self`, so the creeper must be `mut`. You
   can tell from a method's first line whether it can change things."
   Put the `mut` back. Commit.

6. **Rustlings.** Do the `structs` exercises (1 to 3).

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `error[E0063]: missing field` | A field was left out when making the struct | Add it. |
| `error[E0596]: cannot borrow ... as mutable` | Calling a `&mut self` method on a variable without `mut` | `let mut`. |
| `` `Mob` doesn't implement `Debug` `` | `{:?}` was used without `#[derive(Debug)]` | Add the `#[derive(Debug)]` line above the struct. |
| `error[E0599]: no method named ... found` | A typo, or the method is outside the `impl Mob` block | Check the name, and the `{ }` of the `impl`. |
| `error[E0425]: cannot find value \`health\`` | Inside a method, a field without `self.` | `self.health`. |

## Talk about it

- What's the difference between a struct and an `impl` block?
- What's the difference between `Mob::new(...)` and `creeper.hit(...)`?
- When does a method take `&self`, and when `&mut self`?
- What does `#[derive(Debug)]` do?

## Challenge *(if there's time, or for next time)*

- Add `fn heal(&mut self, amount: i32)` that never goes over 20.
- Add `fn step_towards(&mut self, other: &Mob)` that moves one block
  closer. Make the zombie chase the creeper in a loop, printing the
  distance each step.
- Make a `struct Point { x: i32, y: i32 }`, and use one inside `Mob`
  instead of `x` and `y`.

## Checkpoint

The learner can, without help:
- [ ] Define a struct, make one, and read its fields
- [ ] Write an `impl` block with `new`, a `&self` method and a `&mut
      self` method
- [ ] Explain Manhattan distance on squared paper
- [ ] Finish the `structs` Rustlings

## Lab notebook

Draw a `Mob` as a box with its four fields, and list its methods with
`&self` or `&mut self` next to each. Commit. Add *struct*, *field*,
*method*, *associated function* and *derive* to `dictionary.md`.

## Guide's background *(optional reading)*

This follows Chapter 5 of the Book. Rust has no classes or inheritance:
data lives in structs, behaviour in `impl` blocks, and sharing behaviour
between types is done with traits (Lesson 9.13). `self` is the same idea
as Jack's `this` or Python's `self`, but Rust makes you say how it's
borrowed: `self` (take ownership), `&self` (look) or `&mut self`
(change).

`derive` asks the compiler to generate an implementation of a trait
(here, `Debug`) from the struct's fields. Later lessons derive `Clone`,
`Copy`, `PartialEq` and serde's `Serialize`.
