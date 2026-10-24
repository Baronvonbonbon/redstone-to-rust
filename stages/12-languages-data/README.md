# Stage 12: Languages & Data

**Badge:** Language Designer · **Needs first:** Stage 11; discrete math
begun (see [MATH-TRACK.md](../../docs/MATH-TRACK.md)) · **Lessons:** 14

The learner builds the two kinds of program that every other program
depends on: a programming language, and a database. The first half
follows *Crafting Interpreters*: grammars, then a taste of Scheme from
SICP, then a tiny Scheme in Python, then **Pickaxe**, the learner's own
language, with a scanner, parser and tree-walking interpreter in Rust,
growing over six lessons from a calculator to recursive functions. The
second half is data: the mathematics of sets and logic, designing a
real database with keys, joins and indexes, and building one from
scratch that survives a crash.

- **Languages** (Lessons 12.1–12.4): a grammar that writes silly
  sentences; syntax and meaning; compilers and interpreters; Scheme's
  prefix brackets, recursion and lists; `lambda`; code that is data; a
  70-line Scheme interpreter in Python.
- **Pickaxe** (12.5–12.10): designing a language on paper; a scanner;
  a recursive-descent parser that prints its trees as Scheme; values
  and friendly runtime errors; variables and scope, acted out with
  boxes; `if`, `while`, `and` and `or`; functions, `return` and
  recursion, with induction to show why it works.
- **Data** (12.11–12.13): sets, Venn diagrams, truth tables and De
  Morgan's law, in Python and SQL; designing the Creeper Club's
  database, with keys, constraints, joins, `NULL` and transactions; an
  index that makes a 131,072-block world ten times faster to search;
  the Chest, a key-value database in Rust with a crash-proof log.
- **The project** (12.14): a feature of the learner's own design for
  Pickaxe, with tests and documentation, and the Stage 12 checkpoint.

Every program in the lessons was run, every error message is a real one,
and every terminal output is from a real run. Each Pickaxe lesson's code
was built and checked with `cargo fmt` and `cargo clippy`, and
`check-pickaxe` was tested against each stage of the interpreter.

## Tools

- **MIT Scheme** (Lessons 12.2 and 12.3): from your own account, while
  online, `./scripts/install-packages.sh --later`. Check with
  `mit-scheme --version`.
- **The language lab**, from your own account, before Lesson 12.5:
  `./scripts/give-lab.sh LEARNER lang`. It puts `check-pickaxe` and its
  tests in `~/lab/lang`. The [language lab
  handbook](../../labs/lang/README.md) explains them, and holds the
  finished Pickaxe interpreter for you.
- Rust and Cargo from Stage 9; Python 3; `sqlite3`, with `minecraft.db`
  from the Stage 5 SQL lab (`./scripts/give-lab.sh LEARNER sql`).
- **(Free, in the offline library)** *Crafting Interpreters*, by Robert
  Nystrom (`repos/crafting-interpreters/book/`, as Markdown; the text is
  CC BY-NC-ND); *Structure and Interpretation of Computer Programs*
  (`repos/sicp/html/index.xhtml`, CC BY-SA); and *Let's Build a Simple
  Database* (`repos/db-tutorial/_parts/`, MIT). Each lesson's "Guide's
  background" says which chapter it follows. They're written for older
  readers, so they're for the guide, or for reading together.
- **(Optional)** Index cards, a die, dominoes, small boxes and sticky
  notes, and two hoops or loops of string, for the act-outs.

## A note on the internet

None of the lessons need the internet once MIT Scheme is installed and
the offline library is mirrored.

## Lessons

| # | Lesson | What happens | Key ideas |
|---|---|---|---|
| 12.1 | [The Rules of a Language](01-grammar.md) | Grammar cards; a silly-sentence maker; syntax and meaning; parse trees; compilers and interpreters | grammars, recursion |
| 12.2 | [Brackets First: Scheme](02-scheme-1.md) | The REPL; prefix sums; `define`; recursion with huge numbers; `boom.scm` | Scheme, prefix |
| 12.3 | [Lists, Lambdas, and Code That Is Data](03-scheme-2.md) | `car`, `cdr` and `cons` with boxes; `map`, `filter`, `lambda`; `my-map`; `eval` | lists, higher-order |
| 12.4 | [A Tiny Scheme, in Python](04-tiny-scheme.md) | Tokenize, read, evaluate; environments; `fact` in the learner's own Scheme | interpreters |
| 12.5 | [Pickaxe, Part 1](05-pickaxe-scanner.md) | Designing Pickaxe on paper; a scanner in Rust; `check-pickaxe` | specification, tokens |
| 12.6 | [Pickaxe, Part 2](06-pickaxe-parser.md) | The stickiness ladder; recursive descent; `Box`; trees printed as Scheme | parsing, precedence |
| 12.7 | [Pickaxe, Part 3](07-pickaxe-eval.md) | Values; walking the tree; friendly runtime errors | evaluation |
| 12.8 | [Pickaxe, Part 4](08-pickaxe-statements.md) | `say`, `let`, `=`, blocks; scope with boxes; programs from files | statements, scope |
| 12.9 | [Pickaxe, Part 5](09-pickaxe-control.md) | `if`, `else if`, `while`; short-circuit `and` and `or`; Creeper Boom and hailstones | control flow |
| 12.10 | [Pickaxe, Part 6](10-pickaxe-functions.md) | `fun` and `return`; a call with boxes; recursion and induction | functions |
| 12.11 | [Sets and Logic](11-sets-and-logic.md) | Mob hoops; Python sets; truth tables and De Morgan's law; `INTERSECT` and `EXCEPT` | discrete math |
| 12.12 | [Designing a Database](12-designing-databases.md) | The Creeper Club's tables; keys, joins, `NULL`, transactions; an index on a block world | relational design |
| 12.13 | [Build a Database: The Chest](13-chest-database.md) | A key-value store in Rust; a log that survives `kill -9`; safe compaction | persistence |
| 12.14 | [Project: Make Pickaxe Yours](14-language-project.md) | A feature of the learner's own design, with tests and documentation; Stage 12 checkpoint | language design |

## Setup notes

- The learner's Stage 12 work lives in `~/lab/lang`: `python` and
  `scheme` (git repositories made in Lessons 12.1 and 12.2), `pickaxe`
  and `chest` (from `cargo new`), and `data` (Lesson 12.12); plus
  `check-pickaxe` and `tests` from the lab.
- Pickaxe is built up over six lessons, and each one changes code from
  the one before. If a lesson's code won't build and the cause can't be
  found, compare it with the finished version in `labs/lang/pickaxe`,
  file by file; but run `check-pickaxe` first, which usually points
  straight at the problem.
- Never commit the `.db` files or `chest.log`: they're made by the
  programs, and `world.db` is several megabytes.

## Free play for this stage

- Silly-sentence grammars for anything: superhero names, Minecraft
  commands, school reports.
- Scheme: the exercises at the end of SICP Section 1.1 and 1.2, with the
  guide.
- Pickaxe programs: games, quizzes, number puzzles; and new features.
- The Creeper Club database: a real list of the family's books, games or
  Lego sets.
- For an older learner: the rest of *Crafting Interpreters* Part II
  (closures, classes), or Part III (a bytecode VM in C).

## Habits to build now

- **Grammar first.** Change the rules on paper before changing the
  parser.
- **Show the tree.** When a program does something strange, look at what
  the parser understood.
- **Friendly errors.** Every mistake a user can make deserves a message
  that says what went wrong.
- **Tests as a safety net.** `check-pickaxe` after every change; a
  regression caught at once is easy to fix.
- **One fact, one place.** In tables, and in code.
- **Write it down before saying OK.** For anything that must survive a
  crash.

## Checkpoint

The learner can, without help:
- [ ] Write a grammar, and explain how precedence lives in it
- [ ] Use Scheme's lists, `lambda` and recursion, and explain why code
      is data
- [ ] Explain tokenize, parse and evaluate, with Pickaxe's files
- [ ] Explain scope and function calls with boxes, and recursion with
      induction
- [ ] Prove De Morgan's law with a truth table, and use set operations
- [ ] Design tables with keys, join them, and explain an index
- [ ] Explain how the Chest survives a crash and compacts safely

They can also:
- [ ] Pass `check-pickaxe 12.10` with their own interpreter
- [ ] Show a Pickaxe feature they designed, with tests and documentation
      (Lesson 12.14)
