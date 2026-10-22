# Lesson 3.1: Silly Sentences

**Time:** 45 min · **You need:** Thonny · **New words:** string, f-string,
method, index

## Goal *(read this to the learner)*

> Welcome to Stage 3, where you start making games! Every game needs
> words: names, messages, stories, scores. Today you'll learn the tricks
> Python knows for working with words, and build a silly story machine
> that turns your friends into superheroes.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] In a terminal, make this stage's folder: `mkdir -p ~/lab/python/stage3`

## Warm-up (5 min)

"What's a string? What's the difference between `"7"` and `7`? What does
`int()` do?" *(Words in quotes; one is text and one is a number; it turns
text into a number.)*

## Activity

1. **Joining strings.** In the Shell:
   ```python
   name = "Steve"
   "Hello " + name
   name * 3
   len(name)
   ```
   **They should see:** `'Hello Steve'`, `'SteveSteveSteve'` and `5`.

   **Say:** "`+` glues strings together, and `len` counts how many letters
   (and spaces) a string has. *len* is short for *length*."

2. **f-strings: the easy way to fill in blanks.**
   ```python
   age = 9
   f"{name} is {age} years old"
   f"7 times 8 is {7 * 8}"
   ```
   **Say:** "Put an `f` before the quote mark, and anything in curly
   brackets `{ }` gets filled in, even sums. No more `str()` and lots of
   `+`. Curly brackets are Shift and the `[` and `]` keys."

3. **Strings know tricks: methods.**
   ```python
   name.upper()
   name.lower()
   "the creeper exploded".title()
   "I like cheese".replace("cheese", "underpants")
   ```
   **Say:** "A **method** is a trick that belongs to a thing. You've used
   them before: `t.forward()` was a turtle's trick. These are string
   tricks. The brackets at the end are important, even when they're empty."

   And checking:
   ```python
   "ee" in "creeper"
   "z" in "creeper"
   ```
   *(`True`, then `False`.)*

4. **Letters by number.**
   ```python
   name[0]
   name[1]
   name[-1]
   ```
   **They should see:** `'S'`, `'t'`, `'e'`.

   **Say:** "Each letter has a number, called its **index**. Counting
   starts at 0, like `range`. And `-1` means the last letter, `-2` the
   one before. Handy when you don't know how long a word is."

5. **The superhero name machine.** New file, `~/lab/python/stage3/hero.py`:
   ```python
   print("=== SUPERHERO NAME MACHINE ===")
   name = input("What's your first name? ")
   food = input("What's your favourite food? ")
   animal = input("Name an animal: ")

   hero = f"Captain {food.title()}pants"
   sidekick = f"{name[0].upper()}-{animal.title()}"

   print(f"From now on, {name} is known as... {hero.upper()}!")
   print(f"Their trusty sidekick is {sidekick}.")
   print(f"Your hero name has {len(hero)} letters.")
   ```
   Run it. Try it with everyone's names.

6. **The silly story machine.** New file, `story.py`. The learner writes a
   short story (4 or 5 sentences) with blanks, then asks for the words.
   For example:
   ```python
   print("Give me some words, and I'll write a story!")
   person = input("A person's name: ")
   thing = input("Something smelly: ")
   number = input("A big number: ")
   place = input("A place: ")
   noise = input("A silly noise: ")

   print()
   print(f"One day, {person} found {number} {thing}s in {place}.")
   print(f'"{noise.upper()}!" shouted {person}.')
   print(f"Nobody went to {place} ever again.")
   print("THE END")
   ```
   **Say:** "`print()` with nothing in it prints an empty line. And look
   at the second story line: it starts with a single quote `'`, so it can
   have double quotes `"` inside it."

   Let them write their own story. Then play it with someone else, who
   doesn't get to see the story first.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| The output shows `{name}` instead of the name | The `f` is missing before the quote | Put `f` right before the opening quote: `f"Hello {name}"`. |
| `IndexError: string index out of range` | Asked for a letter number past the end | The last letter is `len(name) - 1`, or just use `-1`. |
| `AttributeError: 'str' object has no attribute 'uper'. Did you mean: 'upper'?` | Spelling | Python even suggests the right word. |
| `<built-in method upper of str object at 0x...>` | Forgot the brackets | `name.upper()`, with `()`. |
| `SyntaxError: f-string: expecting '}'` | A curly bracket isn't closed | Every `{` needs a `}`. |
| The text stops early, or a `SyntaxError` with quotes inside a sentence | A `"` inside a string that started with `"` | Start the string with `'` instead, or the other way round. |

## Talk about it

- What's the difference between `"Hi " + name` and `f"Hi {name}"`?
  *(They do the same thing; the f-string is easier to read.)*
- What's `name[0]`? What about `name[-1]`?
- What's a method? Can you name a turtle method and a string method?

## Challenge *(if there's time, or for next time)*

- **Slices:** `name[0:3]` gives the first three letters. What's
  `"underpants"[5:]`? Make a name mash-up: the first half of one name plus
  the second half of another.
- **Backwards:** `name[::-1]` reverses a string. Is `"racecar"` the same
  backwards? Words like that are called **palindromes**. Write a program
  that checks.
- Count the letter `e` in a sentence: `"creeper".count("e")`.

## Checkpoint

The learner can, without help:
- [ ] Use an f-string to put variables and sums into a sentence
- [ ] Use at least three string methods (`upper`, `lower`, `title`,
      `replace`)
- [ ] Get a letter by its index, including the last one with `-1`

## Lab notebook

Copy your story's best line. Make a list of string methods with an example
of each. Add *f-string*, *method* and *index* to the dictionary.

## Guide's background *(optional reading)*

Most programs spend a lot of their time handling text: names, messages,
web pages, files. Python's strings come with dozens of built-in methods;
`help(str)` in the Shell lists them all.

**f-strings** ("formatted strings") are the modern way to build text from
pieces. They're easier to read than gluing with `+`, and they convert
numbers to text automatically, so the `str()` from Lesson 2.9 is rarely
needed now.

Indexing strings from 0, and from the end with negative numbers, is the
same system lists use in Lesson 3.3. Learning it on short words first
makes lists much easier.
