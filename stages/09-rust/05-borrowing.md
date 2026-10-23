# Lesson 9.5: Borrowing

**Time:** 2 sessions of 45 min · **You need:** a terminal; a text
editor; `~/lab/rust`; a book, and a pencil · **New words:** reference,
borrow, mutable reference, slice, `&str`, borrow checker, dangling

## Goal *(read this to the learner)*

> Moving things all the time would be annoying: you'd never get your
> sword back from a function. So Rust lets you **lend** a value instead.
> There are two kinds of loan: lots of people can *look* at once, or
> one person can *change* it, but never both at the same time. That
> one rule stops a whole family of bugs.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] Find a book to lend in step 1 (a Captain Underpants book is ideal).

## Warm-up (5 min)

"What happens to a `String` you give to a function?" *(It moves, and the
function drops it at the end.)* "What if you want it back?" *(Clone it,
or give it back. Today: a better way.)*

## Activity

### Session 1: looking and changing

1. **Act it out.** Hold up the book. **Say:** "I can lend this book to
   lots of people at once, to *read*: you, me and a teddy can all look at
   the same page. But if someone wants to *write* in it with a pencil,
   everyone else has to stop reading first, or the page would change
   under them. And I can't throw the book away while anyone has
   borrowed it." Act out each part.

2. **Lending to look.**
   ```
   cd ~/lab/rust
   cargo new borrowing
   cd borrowing
   ```
   ```rust
   fn letters(word: &String) -> usize {
       word.len()
   }

   fn main() {
       let mut name = String::from("Steve");
       let n = letters(&name);
       println!("{name} has {n} letters");
   }
   ```
   **They should see:** `Steve has 5 letters`. **Say:** "`&name` makes a
   **reference**: a pointer, like Lesson 8.2, that *borrows* `name`
   without taking it. The function's argument type is `&String`, a
   reference to a String. We still own `name` afterwards." (`usize` is
   the type Rust uses for sizes and counting.)

3. **Lending to change.** Add a second function above `main`:
   ```rust
   fn shout(word: &mut String) {
       word.push_str("!!!");
   }
   ```
   and at the end of `main`:
   ```rust
       shout(&mut name);
       println!("{name}");
   ```
   **They should see:** `Steve!!!`. **Say:** "`&mut` is a **mutable
   reference**: a loan that's allowed to change the value. The variable
   has to be `let mut` for that."

4. **Breaking the rule.** Replace `shout(&mut name);` with:
   ```rust
       let first = &name;
       shout(&mut name);
       println!("{first}");
   ```
   `cargo run`. **They should see:**
   ```
   error[E0502]: cannot borrow `name` as mutable because it is also borrowed as immutable
   ```
   and a picture with three labels: `immutable borrow occurs here`,
   `mutable borrow occurs here`, `immutable borrow later used here`.
   **Say:** "`first` was still looking when `shout` tried to write. That
   is the book being scribbled on while someone reads. The part of Rust
   that checks this is the **borrow checker**."

   **Ask:** "Move `println!("{first}");` up, above `shout`. Does it
   work now?" *(Yes! `first` has finished looking before the change.)*
   Then put it back to `shout(&mut name);` alone.

### Session 2: slices, and the rule against dangling

5. **A slice.** Add this function:
   ```rust
   fn first_word(text: &str) -> &str {
       match text.find(' ') {
           Some(space) => &text[..space],
           None => text,
       }
   }
   ```
   and at the end of `main`:
   ```rust
       let book = String::from("Captain Underpants and the Attack of the Talking Toilets");
       println!("The first word is {}", first_word(&book));
   ```
   **They should see:** `The first word is Captain`. **Say:** "`&str` is a
   **slice** of text: a reference to part of a string, with its start
   and length. `&text[..space]` means from the start up to the space. No
   copying: it points into the original. `match` checks whether `find`
   found a space; Lesson 9.7 explains it fully."

   **Say:** "Notice `first_word` takes `&str`, and we gave it `&book`, a
   `&String`. Rust turns one into the other by itself. Taking `&str` is
   better, because it works for both."

6. **Dangling.** **Say:** "In C, you could return a pointer to a local
   variable, and use it after the function ended: a **dangling** pointer.
   Let's try it in Rust." Add above `main`:
   ```rust
   fn make_name() -> &String {
       let s = String::from("Alex");
       &s
   }
   ```
   `cargo run`. **They should see:**
   ```
   error[E0106]: missing lifetime specifier
   ```
   with `this function's return type contains a borrowed value, but there
   is no value for it to be borrowed from`, and further down, `help:
   instead, you are more likely to want to return an owned value`.
   **Say:** "`s` is dropped when `make_name` ends, so a reference to it
   would point at freed memory. Rust won't allow it. The fix it suggests:
   return the `String` itself, and the caller owns it." Change it to
   `fn make_name() -> String` returning `s`, then delete the function.
   Commit.

7. **Rustlings.** Do `move_semantics4` and `move_semantics5`.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `error[E0502]: cannot borrow ... as mutable because it is also borrowed as immutable` | Someone is still looking while something changes it | Finish using the `&` reference before the `&mut` one. |
| `error[E0499]: cannot borrow ... as mutable more than once at a time` | Two `&mut` loans at once | Use one, finish with it, then make the next. |
| `error[E0596]: cannot borrow ... as mutable, as it is not declared as mutable` | `&mut` of a variable without `mut` | `let mut`. |
| `error[E0106]: missing lifetime specifier` | A function returns a reference to something it made | Return the owned value (`String`, not `&String`). |
| `error[E0308]: mismatched types` ... `expected \`&String\`, found \`String\`` | The `&` was forgotten in the call | `letters(&name)`. |

## Talk about it

- What's the difference between `&` and `&mut`?
- What's the borrowing rule? Use the book to explain it.
- What's a slice? Why doesn't it copy anything?
- Which C bug does the dangling rule stop?

## Challenge *(if there's time, or for next time)*

- Write `fn last_word(text: &str) -> &str`. *(Hint: `rfind`.)*
- Write `fn double(n: &mut i32)` that doubles a number in place. Call it
  with `double(&mut x);`.
- Why does `first_word` need no lifetime, when `make_name` did? Read the
  start of Chapter 10.3 of the Book for the answer.

## Checkpoint

The learner can, without help:
- [ ] Pass a value to a function by `&` or `&mut`, and explain the
      difference
- [ ] Explain the borrowing rule with the book
- [ ] Use a `&str` slice
- [ ] Read an E0502 error and fix it

## Lab notebook

Draw `name` on the stack, its letters on the heap, and two `&` arrows
pointing at it. Draw a `&str` slice pointing at part of the book's title.
Write the borrowing rule. Commit. Add *reference*, *borrow*, *slice*,
*borrow checker* and *dangling* to `dictionary.md`.

## Guide's background *(optional reading)*

This follows Chapters 4.2 and 4.3 of the Book. The rule "many readers or
one writer" is what makes Rust references safe: no one can change or
free data while someone else has a pointer into it. It also stops
**data races** between threads (Lesson 9.18), which is why Rust calls
this "fearless concurrency".

The borrow checker works out how long each reference is used (its
**lifetime**). Since 2018 it uses *non-lexical lifetimes*: a borrow ends
at its last use, not at the end of the block, which is why moving the
`println!` in step 4 fixes the error. Functions that take one reference
and return one, like `first_word`, get their lifetimes filled in
automatically; Lesson 9.13 and the `lifetimes` Rustlings show the cases
that need writing out.

`&String` as an argument works, but Clippy (Lesson 9.12) suggests `&str`,
which accepts more. The lesson uses `&String` first because it's easier
to explain.
