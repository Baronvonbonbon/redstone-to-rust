# Lesson 12.1: The Rules of a Language

**Time:** 2 sessions of 45 min · **You need:** a terminal; a text editor;
index cards and coloured pens; a die · **New words:** language,
grammar, rule, syntax, meaning (semantics), parse tree, interpreter,
compiler

## Goal *(read this to the learner)*

> Python, Rust, Bash, Jack, SQL: you've used lots of languages. This
> stage, you'll design and build your own. Every language starts with
> its **grammar**: the rules for what a sentence can look like. Today
> you'll write a grammar that makes silly sentences by itself, then
> look at how grammar decides what `1 + 2 * 3` means.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] Glance at Lesson 8.14 (the Jack parser): the learner has met
      grammars and parse trees before. This stage builds on it.
- [ ] Write these six cards, one rule per card, in big letters:
      ```
      SENTENCE  →  THING  DOES  THING
      THING     →  the DESCRIBED   |   Captain Underpants   |   my teacher
      DESCRIBED →  NOUN   |   ADJECTIVE DESCRIBED
      NOUN      →  creeper | pickaxe | sandwich | dragon
      ADJECTIVE →  green | sneaky | enormous | soggy
      DOES      →  eats | tickles | explodes near | builds
      ```

## Warm-up (5 min)

"How many languages have you programmed in?" List them: Bash, Python,
Hack assembly, HDL, C, Jack, VM code, Rust, SQL. "What's the same about
all of them?" *(They have rules: brackets must match, words go in a
certain order, and the computer complains if you break them.)*

## Activity

### Session 1: grammars that make sentences

1. **Sentences from cards.** Lay the cards out. **Say:** "These are the
   **rules** of a tiny language. Words in capitals are 'make one of
   these', and `|` means 'or': choose one." Start with `SENTENCE` written
   on paper. Replace it, using its card, with `THING DOES THING`. Then
   replace each capital word using its card: roll the die to choose
   when there's a choice (count along the choices, going round again if
   needed). Keep going until there are no capitals left. **They should
   see** something like `the sneaky sandwich tickles my teacher`. Make
   three more.

2. **A rule that uses itself.** Look at `DESCRIBED`. **Ask:** "What
   happens if you keep choosing the second choice?" *(`ADJECTIVE
   DESCRIBED` → `soggy DESCRIBED` → `soggy ADJECTIVE DESCRIBED` → `soggy
   green DESCRIBED`...)* **Say:** "That rule is **recursive**: it uses
   itself, like the recursive functions of Stage 7. Six cards, and you
   can make sentences of any length. A whole language is just a few
   rules like these. The rules are called its **grammar**."

3. **A grammar in Python.** Make the stage's folders:
   ```
   mkdir -p ~/lab/lang/python
   cd ~/lab/lang/python
   git init
   ```
   Make `grammar.py`:
   ```python
   import random

   # Each rule says what a part can be made of.
   # Words in CAPITALS are other rules; anything else is a real word.
   grammar = {
       "SENTENCE": [["THING", "DOES", "THING"]],
       "THING": [["the", "DESCRIBED"], ["Captain Underpants"], ["my teacher"]],
       "DESCRIBED": [["NOUN"], ["ADJECTIVE", "DESCRIBED"]],
       "NOUN": [["creeper"], ["pickaxe"], ["sandwich"], ["dragon"]],
       "ADJECTIVE": [["green"], ["sneaky"], ["enormous"], ["soggy"]],
       "DOES": [["eats"], ["tickles"], ["explodes near"], ["builds"]],
   }


   def make(part):
       if part not in grammar:
           return part
       choice = random.choice(grammar[part])
       words = []
       for piece in choice:
           words.append(make(piece))
       return " ".join(words)


   for n in range(5):
       print(make("SENTENCE"))
   ```
   `python3 grammar.py`. **They should see** five sentences, different
   every time, like:
   ```
   Captain Underpants tickles my teacher
   the pickaxe tickles Captain Underpants
   Captain Underpants eats the pickaxe
   Captain Underpants builds Captain Underpants
   Captain Underpants tickles Captain Underpants
   ```
   **Ask:** "Where's the recursion in the program?" *(`make` calls
   `make` for each piece, just like replacing each capital word with
   its card.)* "When does it stop?" *(When a piece isn't a rule: a real
   word.)* Try `print(make("DESCRIBED"))` a few times: sometimes just
   `pickaxe`, sometimes `soggy soggy sneaky green pickaxe`.

4. **Make it yours.** The learner adds words and rules: more nouns, a
   `PLACE` rule (`in the Nether | on the flagpole | under the bed`) and
   a change to `SENTENCE` so that it can end with a place. Commit.

### Session 2: grammar and meaning

5. **Right shape, no sense.** **Ask:** "Is 'the soggy pickaxe eats
   Captain Underpants' a correct sentence?" *(It follows every rule.
   But it's nonsense!)* **Say:** "Following the rules is called
   **syntax**. What it means is called **meaning** (or semantics). A
   sentence can have perfect syntax and silly meaning." Now in code:
   **Ask:** "Which of these breaks the syntax, and which has a meaning
   problem?"
   - Python `print("hi"` *(syntax: the bracket isn't closed)*
   - Python `print(1 / 0)` *(meaning: fine shape, but you can't divide
     by zero)*
   - Rust `let x: u8 = 300;` *(meaning: the shape is fine, but 300
     doesn't fit in a `u8`)*

   **Say:** "Syntax errors are found before the program runs. Meaning
   problems are found by checking types, like Rust does, or when it
   runs."

6. **A grammar for sums.** On paper, write this grammar (the same shape
   as Jack's, from Lesson 8.14):
   ```
   SUM     →  PRODUCT  ( + PRODUCT  |  - PRODUCT )*
   PRODUCT →  NUMBER   ( * NUMBER   |  / NUMBER  )*
   ```
   **Say:** "`*` after brackets means 'zero or more times'." Draw the
   **parse tree** for `1 + 2 * 3` together: `SUM` at the top, with two
   `PRODUCT`s below it, joined by `+`; the first `PRODUCT` is just `1`,
   the second is `2 * 3`. **Ask:** "What's the answer, working up from
   the bottom of the tree?" *(2 × 3 = 6 first, then 1 + 6 = 7.)* **Say:**
   "The grammar puts `*` lower down, so it happens first. That's how a
   language knows that `*` goes before `+`: it's in the grammar." Draw
   the tree for `8 - 2 - 1` too. **Ask:** "Is it 5 or 7?" *(5: the
   `( ... )*` goes left to right, so `(8 − 2) − 1`.)*

7. **Two ways to run a language.** **Ask:** "When you ran your Jack
   programs in Stage 8, what happened to them first?" *(The compiler
   turned them into VM code, then Hack.)* "When you run `python3
   grammar.py`, does Python make a Hack-like file first?" *(No: it reads
   and runs it straight away.)* **Say:** "A **compiler** translates the
   whole program into another language first, like a translator writing
   a whole book in French. An **interpreter** reads the program and
   does what it says straight away, like a translator speaking out
   loud. Rust and Jack use compilers. Python, Bash and SQL use
   interpreters. This stage, you'll build interpreters: a tiny one for
   Scheme in Python, and a bigger one, for a language of your own, in
   Rust." Draw both as pictures.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| A word in capitals appears in a sentence, like `the DESCRIBD tickles my teacher` | That rule's name is spelled differently where it's used, so `make` thinks it's an ordinary word | Check the spelling in both places. |
| `RecursionError: maximum recursion depth exceeded` | A rule that *only* uses itself, like `"DESCRIBED": [["ADJECTIVE", "DESCRIBED"]]` | Every recursive rule needs a choice that stops, like `["NOUN"]`. |
| Every sentence comes out the same | Each rule has only one choice | Add more choices to the lists. |
| The words run together with no spaces | `"".join` instead of `" ".join` | Use `" ".join(words)`. |

## Talk about it

- What's a grammar? What's a recursive rule?
- What's the difference between syntax and meaning? Give an example of
  each, in English and in code.
- How does a grammar make `*` happen before `+`?
- What's the difference between a compiler and an interpreter?

## Challenge *(if there's time, or for next time)*

- Make a grammar for Minecraft commands: `/give PLAYER ITEM NUMBER`,
  `/tp PLAYER X Y Z`. Make it print ten random commands.
- Make a grammar for silly superhero names (`Captain` / `Professor` /
  `The Incredible` + adjective + noun).
- Add brackets to the sum grammar: `NUMBER` can also be `( SUM )`. Draw
  the tree for `(1 + 2) * 3`.

## Checkpoint

The learner can, without help:
- [ ] Make a sentence from grammar cards, and explain a recursive rule
- [ ] Write a grammar in Python that makes random sentences
- [ ] Explain syntax and meaning, with examples
- [ ] Draw the parse tree for a small sum, and explain why `*` goes first
- [ ] Explain the difference between a compiler and an interpreter

## Lab notebook

Copy your favourite three sentences. Draw the parse tree for `1 + 2 * 3`.
Draw the compiler and the interpreter. Commit. Add *grammar*,
*syntax*, *meaning*, *parse tree*, *interpreter* and *compiler* to
`dictionary.md`.

## Guide's background *(optional reading)*

This lesson follows *Crafting Interpreters*, Chapter 2 ("A Map of the
Territory") and the start of Chapter 5, in the offline library
(`repos/crafting-interpreters/book/a-map-of-the-territory.md` and
`representing-code.md`). Grammars written with rules like these are
**context-free grammars**, written in a notation called **BNF**; the
`( ... )*` form is the "extended" BNF that Nand to Tetris and *Crafting
Interpreters* both use. Using a grammar to *make* sentences, as here,
is the reverse of parsing, which *recognises* them; the recursive
function looks almost the same either way, which Lesson 12.6 uses.

The linguist Noam Chomsky's sentence "Colorless green ideas sleep
furiously" is the classic example of good syntax with no meaning.
Real systems mix compiling and interpreting: Python first compiles to
bytecode for its own virtual machine (like Stage 8's VM), and Java and
JavaScript compile to machine code while running. The difference is
still a good first picture.
