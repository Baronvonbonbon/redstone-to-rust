# Lesson 8.13: The Tokenizer (Project 10)

**Time:** 3 sessions of 45 min · **You need:** a terminal; Thonny;
`~/lab/n2t`; the Jack card; index cards or strips of paper ·
**New words:** compiler, token, tokenizer, keyword, symbol, identifier,
XML

## Goal *(read this to the learner)*

> Now you'll write your own Jack compiler: the program that turned your
> games into VM code. It's the biggest program in the course so far, so
> it's built in three parts. The first part, the **tokenizer**, does what
> your eyes do when you read: it splits the text into words and
> punctuation, called **tokens**, and says what kind each one is.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] Cut a short line of Jack into tokens on strips of paper (step 1).

## Warm-up (5 min)

"In `let total = total + 1;`, how many pieces are there?" *(Seven: let,
total, =, total, +, 1, ;.)* "Which are words of the language, and which
are names you chose?"

## Activity

### Session 1: tokens by hand

1. **The compiler's plan.** **Say:** "A compiler has three jobs.
   1. **Tokenize:** split the text into tokens (this lesson).
   2. **Parse:** work out how the tokens fit together, like the grammar
      of a sentence (Lesson 8.14).
   3. **Generate code:** write the VM code (Lessons 8.15 and 8.16)."

   Write `if (x < 10) { let x = x + 1; }` on a strip, and cut it into
   tokens. Sort them into five piles, using the Jack card:
   - **keyword**: a word of the language (`if`, `let`, `class`...)
   - **symbol**: one punctuation character (`( ) { } < = + ;`...)
   - **integerConstant**: a number (`10`, `1`)
   - **stringConstant**: text in quotes (none here)
   - **identifier**: a name the programmer chose (`x`)

   **Ask:** "Did spaces make tokens?" *(No: they only separate them.
   `x<10` and `x < 10` are the same tokens.)*

2. **What the answer looks like.**
   ```
   cd ~/lab/n2t/projects/10
   ls Square
   head -12 Square/MainT.xml
   ```
   **They should see:** `Main.jack`, `MainT.xml`, `Main.xml` and the
   same for `Square` and `SquareGame`. The `T.xml` file starts:
   ```
   <tokens>
   <keyword> class </keyword>
   <identifier> Main </identifier>
   <symbol> { </symbol>
   ...
   ```
   **Say:** "This is **XML**: each thing is wrapped in a start tag and an
   end tag, like brackets with names. Your tokenizer must print exactly
   this. XML uses `<`, `>`, `&` and `"` for itself, so inside a tag
   they're written as `&lt;`, `&gt;`, `&amp;` and `&quot;`."

### Session 2: the tokenizer

3. **The starting program.** In Thonny, make
   `~/lab/n2t/projects/10/tokenizer.py`:
   ```python
   import sys

   KEYWORDS = ["class", "constructor", "function", "method", "field", "static",
               "var", "int", "char", "boolean", "void", "true", "false", "null",
               "this", "let", "do", "if", "else", "while", "return"]
   SYMBOLS = "{}()[].,;+-*/&|<>=~"


   def strip_comments(text):
       """Gives back the text with every comment taken out."""
       while "/*" in text:
           start = text.index("/*")
           end = text.index("*/", start)
           text = text[:start] + " " + text[end + 2:]
       lines = []
       for line in text.split("\n"):
           lines.append(line.split("//")[0])
       return "\n".join(lines)


   def tokenize(text):
       """Gives back a list of (kind, word) pairs."""
       text = strip_comments(text)
       tokens = []
       # Your code goes here.
       return tokens


   def xml_escape(word):
       """XML uses < > & and " itself, so they're written another way."""
       return word.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


   if __name__ == "__main__":
       print("<tokens>")
       for kind, word in tokenize(open(sys.argv[1]).read()):
           print(f"<{kind}> {xml_escape(word)} </{kind}>")
       print("</tokens>")
   ```
   **Say:** "`strip_comments` takes out `/* ... */` comments (which can
   cover many lines, and include `/** ... */`), then `//` comments on each
   line. The `if __name__` part from Lesson 7.3 means the parser can
   `from tokenizer import tokenize` later, without printing anything."

4. **Walk through the text.** **Say:** "`tokenize` reads the text one
   character at a time, with a position `i`, like a finger moving along
   the line. The first character of a token tells you what kind it is."
   The plan:
   ```
   i = 0
   while i is inside the text:
       c = the character at i
       a space or a newline?      skip it
       in SYMBOLS?                one symbol token
       a digit?                   keep going while there are digits: an integerConstant
       a quote?                   find the next quote: everything between is a stringConstant
       anything else?             keep going while there are letters, digits or _:
                                  a keyword if it's in KEYWORDS, otherwise an identifier
   ```
   Hints:
   - `c.isspace()`, `c.isdigit()` and `c.isalnum()` (a letter or a digit)
     are Python's tests.
   - "Keep going while..." is a second position, `j`, that starts at `i`
     and moves on. Then the token is `text[i:j]`, and `i` jumps to `j`.
   - `text.index('"', i + 1)` finds the next quote after `i`.
   - A string constant doesn't keep its quotes.

5. **Test it.**
   ```
   python3 tokenizer.py Square/Main.jack > tokens.xml
   head tokens.xml
   check-xml tokens Square/Main.jack
   ```
   **They should see:** the first tokens, then `ALL GOOD! All 126 lines
   match.` Commit.

### Session 3: every file

6. **All seven.**
   ```
   for f in */*.jack; do check-xml tokens $f; done
   ```
   **They should see:** seven `ALL GOOD!` lines (the `ArrayTest`,
   `ExpressionLessSquare` and `Square` folders). `ArrayTest` has a string
   constant with spaces, and `Square.jack` has `<`. Commit.

   **Ask:** "What would go wrong with `"Don't // stop"` in a Jack program?"
   *(`strip_comments` would cut the string at `//`. None of the test
   files do this. Fixing it is a challenge.)*

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `Comparison failure in line 1, counting from 0`, with `<identifier>class</identifier>` | Keywords come out as identifiers | Check the word against `KEYWORDS`. |
| `<stringConstant>&quot;HOWMANYNUMBERS?&quot;</stringConstant>` (ArrayTest) | The quotes were kept | Take the text *between* the quotes. (The checker ignores spaces, so they vanish in its message.) |
| `<symbol><</symbol>` where `<symbol>&lt;</symbol>` should be | The symbol wasn't escaped | Print every word through `xml_escape`. |
| `<symbol>/</symbol>` where `<keyword>class</keyword>` should be | A comment wasn't taken out | Run the text through `strip_comments` first. |
| The program never stops | `i` doesn't move on for some character | Every branch must change `i`. |
| `ValueError: substring not found` | A quote or `/*` with no partner | Check the `.jack` file, or the `index` call. |

## Talk about it

- What are the three jobs of a compiler?
- What are the five kinds of token? Give an example of each.
- How does the tokenizer know where a token ends?
- Why do `<` and `&` need escaping in XML?

## Challenge *(if there's time, or for next time)*

- Make `strip_comments` skip over strings, so `"Don't // stop"` works.
  *(Walk through the text one character at a time, remembering whether
  you're inside quotes.)*
- Tokenize your own game from Lesson 8.12. How many tokens is it?
- Make the tokenizer stop with a friendly message for a character Jack
  doesn't have, like `#` or `'`.

## Checkpoint

The learner can, without help:
- [ ] Explain the three jobs of a compiler
- [ ] Sort a line of Jack into the five kinds of token
- [ ] Explain how their tokenizer finds where each token ends
- [ ] Pass `check-xml tokens` for all seven files

## Lab notebook

Stick in the paper tokens, sorted into piles. Commit. Add *compiler*,
*token*, *tokenizer*, *keyword*, *identifier* and *XML* to
`dictionary.md`.

## Guide's background *(optional reading)*

This is the first half of Nand to Tetris Project 10. Tokenizing (also
called **lexical analysis** or **lexing**) turns a stream of characters
into a stream of tokens, so the parser never has to think about spaces,
comments or how long a name is. Jack's tokens are simple: every symbol is
one character, and the first character always decides the kind.

The XML output is only for testing: it lets `check-xml` compare the
learner's tokens with the official answer (`*T.xml`), using the
official TextComparer, which ignores all spaces. That's why its messages
show `HOWMANYNUMBERS?` without spaces, and why indentation never
matters. The comparer counts lines from 0, so "line 1" is the first
token after `<tokens>`.

The starting program gives `strip_comments`, the keyword and symbol
lists, and the output; the learner writes `tokenize` from the plan and
hints. The simple `strip_comments` can be fooled by `//` inside a
string, which no test file has (the challenge fixes it).
