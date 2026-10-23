# Lesson 9.14: Iterators and Closures

**Time:** 2–3 sessions of 45 min · **You need:** a terminal; a text
editor; `~/lab/rust`; paper · **New words:** iterator, closure, `map`,
`filter`, `sum`, `collect`, chain, lazy

## Goal *(read this to the learner)*

> So far, every time you wanted to do something to a list, you wrote a
> `for` loop. Rust has a neater way: an **iterator**, a conveyor belt of
> values, with machines along it that change them (`map`), throw some
> away (`filter`), and add them up at the end (`sum`). The machines are
> small functions with no names, called **closures**. You'll find prime
> numbers, the longest word in a poem, and redo the Collatz hunt in one
> line.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] Draw a conveyor belt on a big sheet, with room for three machines
      (step 2).

## Warm-up (5 min)

"In Numberblocks, which numbers are square?" *(1, 4, 9, 16...)* "What are
the first ten square numbers added up?" Let them guess. *(Today Rust
will tell us.)*

## Activity

### Session 1: map, sum, filter

1. **Squares.**
   ```
   cd ~/lab/rust
   cargo new iterators
   cd iterators
   ```
   ```rust
   fn main() {
       let squares: Vec<u32> = (1..=10).map(|n| n * n).collect();
       println!("Squares: {squares:?}");
       let total: u32 = squares.iter().sum();
       println!("They add up to {total}");
       let even: Vec<&u32> = squares.iter().filter(|n| *n % 2 == 0).collect();
       println!("The even ones: {even:?}");
   }
   ```
   **They should see:**
   ```
   Squares: [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
   They add up to 385
   The even ones: [4, 16, 36, 64, 100]
   ```

2. **The conveyor belt.** On the big sheet, draw the belt for the first
   line: the numbers 1 to 10 go in at the left; the `map` machine
   squares each one; `collect` packs them into a Vec at the end. **Say:**
   - "`(1..=10)` is an **iterator**: it gives out values one at a time."
   - "`|n| n * n` is a **closure**: a tiny function with no name. Between
     the bars is what it takes, and after them what it gives back. In
     Python, that's `lambda n: n * n`."
   - "`map` runs the closure on every value. `filter` keeps only the
     values where the closure says `true`. `sum` adds them all up.
     `collect` packs them into a collection, here a Vec."
   - "`.iter()` makes an iterator from a Vec, lending each item (that's
     why `even` holds `&u32`s)."

3. **Chains.** Add:
   ```rust
       let odd_squares: u32 = (1..20).filter(|n| n % 2 == 1).map(|n| n * n).sum();
       println!("Odd squares below 20 add up to {odd_squares}");
   ```
   **They should see:** `Odd squares below 20 add up to 1330`. **Say:**
   "Several machines in a row are a **chain**. Read it left to right:
   numbers 1 to 19, keep the odd ones, square them, add them up." Draw it
   on the belt. Commit.

### Session 2: primes, words and closures

4. **Primes.** Add this function above `main`:
   ```rust
   fn is_prime(n: u32) -> bool {
       n >= 2 && (2..n).take_while(|d| d * d <= n).all(|d| !n.is_multiple_of(d))
   }
   ```
   and in `main`:
   ```rust
       let primes: Vec<u32> = (1..50).filter(|&n| is_prime(n)).collect();
       println!("Primes under 50: {primes:?}");
   ```
   **They should see:**
   ```
   Primes under 50: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
   ```
   **Say:** "Read `is_prime` aloud: n is at least 2, and, trying every d
   from 2 while d times d is no more than n, *all* of them don't divide
   n." **Ask:** "Where have you seen `d * d <= n` before?" *(Prime
   Hunters, Lesson 3.6: you only need to check up to the square root.)*

5. **Closures remember.** Add:
   ```rust
       let bonus = 5;
       let add_bonus = |score: u32| score + bonus;
       println!("10 with the bonus is {}", add_bonus(10));
   ```
   **They should see:** `10 with the bonus is 15`. **Say:** "A closure
   can use variables from around it: this one *captured* `bonus`. A
   normal `fn` can't do that."

6. **Words.** Add:
   ```rust
       let poem = "Creepers are green they go boom and they ruin your cool house";
       let longest = poem.split_whitespace().max_by_key(|word| word.len()).unwrap();
       let c_words = poem
           .split_whitespace()
           .filter(|word| word.to_lowercase().starts_with('c'))
           .count();
       println!("Longest word: {longest}. Words starting with c: {c_words}");
   ```
   **They should see:** `Longest word: Creepers. Words starting with c:
   2`. **Say:** "`max_by_key` finds the biggest by some measure, here the
   length. It gives an `Option`, because an empty poem has no longest
   word; `unwrap` takes the value out, because we know there's one. A
   long chain can go one machine per line, which is how `cargo fmt` lays
   it out."

### Session 3: sorting, and Collatz again

7. **Sorting mobs.** Add:
   ```rust
       let mut mobs = vec![("zombie", 20), ("spider", 16), ("creeper", 20), ("bat", 6)];
       mobs.sort_by_key(|&(_, health)| health);
       println!("Weakest first: {mobs:?}");
   ```
   **They should see:** `Weakest first: [("bat", 6), ("spider", 16),
   ("zombie", 20), ("creeper", 20)]`. **Say:** "Each mob is a tuple. The
   closure takes it apart, ignores the name (`_`) and gives back the
   health to sort by." **Ask:** "Why is the zombie still before the
   creeper?" *(They have the same health, and the sort keeps their old
   order.)*

8. **The Collatz hunt in one line.** Copy `collatz_steps` from Lesson
   9.3 (the Clippy-fixed version from Lesson 9.12) above `main`, and add:
   ```rust
       let best = (1..10000).max_by_key(|&n| collatz_steps(n)).unwrap();
       println!("Under 10000, {best} takes the most Collatz steps: {}", collatz_steps(best));
   ```
   **They should see:** `Under 10000, 6171 takes the most Collatz steps:
   261`. **Ask:** "How many lines was it in Lesson 9.3?" *(Six.)* Commit.

9. **Rustlings.** Do the `iterators` exercises (1 to 5).

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `error[E0282]: type annotations needed` at `collect` | Rust doesn't know what to collect into | Say the type: `let squares: Vec<u32> = ...`. |
| `error[E0277]: a value of type \`Vec<u32>\` cannot be built from an iterator over elements of type \`&u32\`` | `.iter()` lends items, so they're `&u32` | Collect into `Vec<&u32>`, or add `.copied()` before `collect`. |
| `error[E0369]: cannot calculate the remainder of \`&&u32\` divided by \`{integer}\`` (or similar) | `filter` gives the closure a reference to each item | Use `*n` (as in step 1), or the pattern `\|&n\|`. |
| `called \`Option::unwrap()\` on a \`None\` value` | `max_by_key` found nothing, because the list was empty | Check the list isn't empty, or `match` on it. |
| Nothing happens and nothing is printed from a `map` | Iterators are lazy: nothing runs until something like `sum`, `collect` or `for` pulls the values | End the chain with one of those. |

## Talk about it

- What's an iterator? Use the conveyor belt.
- What's a closure? How is it different from a `fn`?
- What do `map`, `filter`, `sum` and `collect` each do?
- Which is easier to read: the loop in Lesson 9.3, or the chain?

## Challenge *(if there's time, or for next time)*

- The sum of the first n odd numbers is always a square number. Check it
  for n up to 20 with iterators. (Numberblocks fans may already know
  why!)
- Find all the three-letter words in a sentence, in capitals.
- `(1..=5).fold(1, |product, n| product * n)` works out 5 × 4 × 3 × 2 ×
  1. What's 10 the same way? What's 30? *(Use `u64`, then `u128`.)*

## Checkpoint

The learner can, without help:
- [ ] Explain an iterator chain with the conveyor belt
- [ ] Write closures for `map`, `filter` and `max_by_key`
- [ ] Use `sum`, `count` and `collect`
- [ ] Finish the `iterators` Rustlings

## Lab notebook

Draw the conveyor belt for the odd squares chain, with the values after
each machine. Write the list of primes under 50. Commit. Add *iterator*,
*closure*, *map*, *filter*, *collect*, *chain* and *lazy* to
`dictionary.md`.

## Guide's background *(optional reading)*

This follows Chapter 13 of the Book. Iterators in Rust are **lazy**:
`map` and `filter` build up a description of the work, and nothing runs
until a *consuming* method (`sum`, `collect`, `count`, `for`) pulls the
values through. The compiler then fuses the whole chain into one loop,
usually as fast as the hand-written `for`, and with no bounds checks:
these are called *zero-cost abstractions*.

The `&` patterns (`|&n|`, `|&(_, health)|`) appear because `filter`,
`max_by_key` and `sort_by_key` pass references to the items. Rustlings'
`iterators` exercises practise this. `is_multiple_of` is a recent
addition to Rust (1.87); on older versions, write `n % d != 0`.
