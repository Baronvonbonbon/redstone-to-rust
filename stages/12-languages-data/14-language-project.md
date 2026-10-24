# Lesson 12.14: Project: Make Pickaxe Yours

**Time:** 4–5 sessions of 45 min · **You need:** a terminal; a text
editor; `~/lab/lang`; paper · **New words:** feature, extension,
regression, test, documentation

## Goal *(read this to the learner)*

> You've built a language, a Scheme, and a database. Now make something
> new with them: a feature for Pickaxe that you designed yourself, from
> grammar to interpreter, with tests and a page explaining it to other
> people. At the end, you'll show it off, and earn the **Language
> Designer** badge.

## Before the lesson *(guide, 15 min)*

- [ ] Read this whole lesson once.
- [ ] Read the ideas in step 1 with the learner a day early.
- [ ] Plan a demo day for the last session, with someone to show it to.
- [ ] `check-pickaxe 12.10` passes. It's the safety net for the whole
      project.

## Warm-up (5 min)

"Which part of Pickaxe was hardest? What's missing from it that Python
or Rust has?" Write the list: it's the start of today's ideas.

## Activity

### Session 1: choosing and planning

1. **Choose a feature.** Some ideas, easiest first:
   - **`repeat 5 { ... }`**: a loop that counts for you. New grammar, a
     new `Stmt`, and an arm in `exec`.
   - **`ask`**: `let name = ask("What's your name? ");` reads a line from
     the keyboard. Then Pickaxe can make games: a number guesser, a quiz.
   - **Built-in functions**: `len("creeper")`, `upper("hello")`,
     `random(6)`. Add them in `call`, before looking in `functions`.
   - **`for i in 1 to 10 { ... }`**: turned into a `let` and a `while` by
     the parser, so the interpreter doesn't change at all.
   - **Lists**: `let mobs = ["creeper", "zombie"]; say mobs[0];` A new
     `Value::List`, new tokens `[` and `]`, and indexing. (Bigger.)
   - **Pickaxe meets the Chest**: `store "diamonds" = 12;` and
     `fetch("diamonds")`, which read and write `chest.log` from Lesson
     12.13, so Pickaxe programs remember things between runs. (Bigger.)
   - **Something of your own.** Changing `say` to rainbow colours?
     Error messages with line numbers? A `#!` line so that `./game.pick`
     runs by itself?

   **Say:** "Choose something you'd *use*. Big enough to be proud of,
   small enough to finish in about three sessions."

2. **A specification.** On paper:
   - Three example programs that use the feature, and exactly what each
     should print.
   - The new grammar rule(s), in the style of Lessons 12.6 and 12.8.
   - Which parts change: the scanner (new symbols?), the parser (new
     `Expr` or `Stmt`?), the interpreter (new arms? a new `Value`?).
   - At least two mistakes a user could make, and the friendly message
     each one gets.
   - Three **milestones**, each one working: (1) it parses, and `show`
     or a test proves it; (2) it runs the first example; (3) all
     examples, the mistakes, and the documentation.

### Sessions 2 to 4: building

3. **Build in milestones.** For each:
   - Change the grammar on paper first, then the code: scanner, parser,
     interpreter.
   - Write the example programs as `.pick` files in the project.
   - After every change, run `~/lab/lang/check-pickaxe 12.10`. **Say:**
     "If an old test breaks, that's called a **regression**: something
     that used to work, broken by something new. The tests catch it
     straight away, while you still remember what you changed."
   - `cargo fmt`, `cargo clippy`, commit at the end of every session.

4. **Your own tests.** Make a folder `tests` in the project, with each
   example as `name.pick` and its correct output as `name.out`. Run one
   with:
   ```
   cargo run -q -- tests/repeat.pick | diff tests/repeat.out -
   ```
   **They should see** nothing at all if the output matches exactly
   (`diff` only speaks when there's a difference). Add the mistakes too.

5. **When stuck.** In this order:
   - Use `show` (Lesson 12.6) to see the tree the parser made.
   - Add `eprintln!("{statement:?}");` in `exec` to watch it run, then
     remove it.
   - Read the matching chapter of *Crafting Interpreters* (in the offline
     library): Chapter 9 for loops, and Chapter 10 for built-in
     functions.
   - Then ask the guide.

### Session 5: documentation, demo day, and the checkpoint

6. **Documentation.** Write `PICKAXE.md` in the project: a page for
   someone who has never seen Pickaxe. What it is, how to run it, every
   statement and operator with an example, and the new feature, with
   its examples. **Say:** "A language nobody can learn is a language
   nobody uses. Documentation is part of the language."

7. **Demo day.** The learner shows Pickaxe to someone: runs an example
   program, shows the tree for one line with `show` (or explains it on
   paper), explains one piece of the interpreter, and shows the new
   feature and its tests.

8. **The Stage 12 checkpoint.** Without notes, the learner explains,
   with drawings if they like:
   - A grammar, and how precedence lives in it.
   - Scheme's lists, `lambda`, and why code is data.
   - The three jobs of an interpreter, with Pickaxe's files.
   - Scope, with boxes; and how a function call puts boxes aside.
   - Why recursion works, with dominoes (induction).
   - Union, intersection and De Morgan's law.
   - Keys, joins and an index, in the club database.
   - How the Chest survives a crash, and compacts safely.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `check-pickaxe 12.10` fails after a change | A regression | Read the `<` and `>` lines; undo the last change with `git diff` and `git checkout`, then try smaller steps. |
| `error[E0004]: non-exhaustive patterns` | A new `Expr`, `Stmt` or `Value` isn't handled in a `match` | Add an arm wherever the compiler points. |
| The new word is treated as a variable name | The parser checks for it too late | Check for the new keyword in `statement` (or `primary`) before the `else` part. |
| The feature works at the prompt but not in a file | A missing `;`, or a different line ending | Use `show` on the line from the file. |
| It's taking much longer than planned | The feature is too big | Finish milestone 1 or 2 properly; save the rest for "Pickaxe 2". |

## Talk about it

- What was harder than you expected? Easier?
- What's a regression? How did the tests help?
- Why does a language need documentation?
- If you were designing a whole new language, what would you change
  about Pickaxe?

## Challenge *(if there's time, or for next time)*

- Write a game in Pickaxe, using your feature: a number guesser, a
  times-tables quiz, a text adventure.
- Write a Pickaxe interpreter *in Pickaxe*... (only joking. Mostly.
  Scheme can do it: that's SICP Chapter 4.)
- Read *Crafting Interpreters* Part III's first chapter ("Chunks of
  Bytecode"): the faster way to run a language, with a virtual machine,
  like Stage 8's.

## Checkpoint

The learner can, without help:
- [ ] Plan a feature with examples, grammar and milestones
- [ ] Build it through the scanner, parser and interpreter, with no
      regressions in `check-pickaxe 12.10`
- [ ] Write tests and documentation for it
- [ ] Explain every item of the Stage 12 checkpoint in step 8

## Lab notebook

Glue in the specification. Copy one example program and its output.
Write what you'd add in Pickaxe 2. Commit. Add *feature*, *regression*
and *documentation* to `dictionary.md`. Stamp the Stage 12 badge,
**Language Designer**, on the passport.

## Guide's background *(optional reading)*

The `for`-loop idea is *desugaring*, in *Crafting Interpreters* Chapter
9; built-in functions are Chapter 10's "native functions"; lists are
not in Lox, so they're a genuinely new design problem (what does `+` do
to two lists? what if the index is too big?), which is good practice in
writing friendly errors. Line numbers in errors need the scanner to
record a line for each token, and the parser to carry it along; it's a
small change to every function, and teaches why real compilers keep
"spans".

For a learner who wants more after this stage, *Crafting Interpreters*
Parts II and III (a full tree-walking interpreter with classes, then a
bytecode virtual machine in C) are the natural next step, and SICP
Chapters 3 and 4 (state, streams, and the metacircular evaluator) take
the Scheme thread further. Stage 13 is where those paths can become the
learner's own specialisation.
