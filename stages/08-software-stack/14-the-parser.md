# Lesson 8.14: The Parser (Project 10)

**Time:** 4–5 sessions of 45 min · **You need:** a terminal; Thonny;
`~/lab/n2t`; the Jack card; squared paper · **New words:** grammar,
parse, parser, parse tree, recursive descent

## Goal *(read this to the learner)*

> A pile of tokens isn't a program yet. The **parser** works out how
> they fit together: this `let` has a name, an `=`, an expression and a
> `;`; this expression is a term, a `+`, and another term. It follows
> the rules of the language, its **grammar**, and builds a tree. Each
> grammar rule becomes one function in your parser, and the functions
> call each other, and even themselves. It's recursion from Lesson 7.5,
> doing real work.

## Before the lesson *(guide, 15 min)*

- [ ] Read this whole lesson once.
- [ ] All seven `check-xml tokens` checks should pass (Lesson 8.13).
- [ ] Practise drawing the parse tree in step 2 yourself.

## Warm-up (5 min)

"What does the tokenizer give back?" *(A list of tokens, each with its
kind.)* "In a sentence, which words go together?" Try "the big creeper
blew up the house": *(the big creeper / blew up / the house.)*

## Activity

### Session 1: grammar and trees

1. **The grammar.** **Say:** "A grammar is a list of rules that say what
   each part of the language is made of. Here are Jack's." Read the table
   together. `name` means an identifier, `?` means 'maybe', and `*` means
   'any number of times, even none'.

   | Rule | Made of |
   |---|---|
   | class | `class` name `{` classVarDec\* subroutineDec\* `}` |
   | classVarDec | `static` or `field`, a type, a name, then (`,` name)\*, `;` |
   | subroutineDec | `constructor`, `function` or `method`; `void` or a type; a name; `(` parameterList `)` subroutineBody |
   | parameterList | maybe: type name, then (`,` type name)\* |
   | subroutineBody | `{` varDec\* statements `}` |
   | varDec | `var` type name, then (`,` name)\*, `;` |
   | statements | statement\*, where a statement is a let, if, while, do or return |
   | letStatement | `let` name, maybe `[` expression `]`, `=` expression `;` |
   | ifStatement | `if` `(` expression `)` `{` statements `}`, maybe `else` `{` statements `}` |
   | whileStatement | `while` `(` expression `)` `{` statements `}` |
   | doStatement | `do` subroutineCall `;` |
   | returnStatement | `return`, maybe an expression, `;` |
   | expression | term, then (op term)\*, where op is one of `+ - * / & \| < > =` |
   | term | a number, a string, `true`/`false`/`null`/`this`, a name, name `[` expression `]`, a subroutineCall, `(` expression `)`, or `-` or `~` then a term |
   | subroutineCall | name `(` expressionList `)`, or name `.` name `(` expressionList `)` |
   | expressionList | maybe: expression, then (`,` expression)\* |

   **Ask:** "Which rules mention themselves, or each other in a circle?"
   *(statements contain if, which contains statements; an expression
   contains terms, and a term can contain an expression in brackets.)*

2. **A tree on paper.** Draw the **parse tree** for `let x = (y + 2) - z;`:
   ```
   letStatement
   ├── let
   ├── x
   ├── =
   ├── expression
   │   ├── term
   │   │   ├── (
   │   │   ├── expression
   │   │   │   ├── term: y
   │   │   │   ├── +
   │   │   │   └── term: 2
   │   │   └── )
   │   ├── -
   │   └── term: z
   └── ;
   ```
   **Say:** "To **parse** is to build this tree. Every box is a grammar
   rule; every leaf is a token."

3. **The answer, as XML.**
   ```
   cd ~/lab/n2t/projects/10
   head -30 ExpressionLessSquare/Main.xml
   ```
   **They should see:** tags like `<class>`, `<subroutineDec>`,
   `<statements>`, each with tokens and more tags inside, indented. **Say:**
   "That's a tree, written as XML: every rule's tag wraps what it's made
   of. Your parser must print this."

   Four details, which the XML files show:
   - `<parameterList>` and `<expressionList>` are always printed, even
     when there's nothing inside.
   - `<statements>` is always printed, even when empty.
   - subroutineCall has *no* tag of its own: its tokens go straight into
     whatever holds it (a `<term>` or a `<doStatement>`).
   - `type`, `name` and `op` have no tags either: they're just tokens.

### Session 2: the starting program

4. **The parser's tools.** In Thonny, make
   `~/lab/n2t/projects/10/parser.py`:
   ```python
   import sys
   from tokenizer import tokenize, xml_escape

   OPS = "+-*/&|<>="


   class Parser:
       def __init__(self, tokens):
           self.tokens = tokens
           self.pos = 0
           self.lines = []
           self.depth = 0

       def peek(self, ahead=0):
           """The word of the next token (or one further on), without eating it."""
           return self.tokens[self.pos + ahead][1]

       def eat(self, expected=None):
           """Writes out the next token and moves past it. Checks it, if asked."""
           kind, word = self.tokens[self.pos]
           if expected is not None and word not in expected.split():
               raise SyntaxError(f"expected {expected} but found {word}")
           self.lines.append("  " * self.depth + f"<{kind}> {xml_escape(word)} </{kind}>")
           self.pos += 1

       def open(self, tag):
           self.lines.append("  " * self.depth + f"<{tag}>")
           self.depth += 1

       def close(self, tag):
           self.depth -= 1
           self.lines.append("  " * self.depth + f"</{tag}>")

       def compile_class(self):
           self.open("class")
           self.eat("class")
           self.eat()                  # the class's name
           self.eat("{")
           while self.peek() in ("static", "field"):
               self.compile_class_var_dec()
           while self.peek() in ("constructor", "function", "method"):
               self.compile_subroutine()
           self.eat("}")
           self.close("class")

       def compile_class_var_dec(self):
           self.open("classVarDec")
           self.eat("static field")
           self.eat()                  # the type
           self.eat()                  # a name
           while self.peek() == ",":
               self.eat(",")
               self.eat()              # another name
           self.eat(";")
           self.close("classVarDec")


   if __name__ == "__main__":
       parser = Parser(tokenize(open(sys.argv[1]).read()))
       parser.compile_class()
       print("\n".join(parser.lines))
   ```
   **Say:**
   - "`peek` looks at the next token without using it up. `eat` writes
     it out and moves on. `eat("{")` also checks that it really *is* a
     `{`, so mistakes are caught straight away. `eat("static field")`
     accepts either word.
   - `open` and `close` write a tag, and indent everything between.
   - `OPS` holds the nine operators, for `compile_expression` later.
   - Look at `compile_class`: it's the grammar rule for class, almost word
     for word! A `*` in the grammar became a `while` loop."

5. **One rule at a time.** Write `compile_subroutine` next, then
   `compile_parameter_list`, `compile_var_dec` and `compile_statements`.
   For now, make `compile_statements` just open and close
   `<statements>` and eat nothing; ExpressionLessSquare has statements,
   so it won't pass yet, but you can see how far it gets:
   ```
   check-xml parse ExpressionLessSquare/Main.jack
   ```
   The line it reports should move further down each time you add a rule.

### Sessions 3 and 4: statements and expressions

6. **Statements.** `compile_statements` loops while the next token isn't
   `}`, and calls `compile_let`, `compile_if` and so on, chosen by the
   first word. Write each from its grammar row.

7. **Expressions, for now.** ExpressionLessSquare is the same game as
   Square, with every expression made simple: just one name or
   constant. So write `compile_expression` as "open, `compile_term`,
   close", and `compile_term` as "open, eat one token, close". Then:
   ```
   check-xml parse ExpressionLessSquare/Main.jack
   check-xml parse ExpressionLessSquare/Square.jack
   check-xml parse ExpressionLessSquare/SquareGame.jack
   ```
   **They should see:** `ALL GOOD!` three times. Commit.

8. **Real expressions.** Now the full rules. `compile_expression`: a
   term, then while the next token is an op, eat it and parse another
   term. `compile_term` must choose between the kinds of term. Hints:
   - `(`: eat it, `compile_expression`, eat the `)`.
   - `-` or `~`: eat it, then `compile_term` (just one term!).
   - A name is the hard one. Look *one token further* with `peek(1)`:
     `[` means an array, `(` or `.` means a subroutine call, anything
     else means a plain variable.
   - Write `compile_call` once, and use it from `compile_term` and
     `compile_do`. Remember: it opens no tag.
   - `compile_expression_list`: maybe an expression, then (`,`
     expression)\*. Stop at `)`.

   **Say:** "`compile_expression` calls `compile_term`, which can call
   `compile_expression` again for brackets, as deep as the brackets go.
   That's called **recursive descent**: each rule's function calls the
   rules inside it."

### Session 5: everything

9. **All seven.**
   ```
   for f in */*.jack; do check-xml parse $f; done
   ```
   **They should see:** seven `ALL GOOD!` lines. Then try your own game:
   ```
   python3 parser.py ~/lab/n2t/projects/9/DiamondDash/DashGame.jack > dash.xml
   head -40 dash.xml
   ```
   Commit. Project 10 is done!

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `<symbol>)</symbol>` where `<parameterList>` should be | An empty parameter list wasn't printed | Always open and close `parameterList` (and `expressionList`). |
| `<expression>` where `<identifier>` should be, in a `do` | The `do`'s call was wrapped in expression tags | `compile_do` calls `compile_call` directly. |
| `<expression>` where `<term>` should be, after a `-` or `~` | `-x` parsed an expression, not a term | After `-` or `~`, call `compile_term`. |
| `SyntaxError: expected ; but found ...` | The parser and the file disagree: usually a rule eating one token too many or too few | The message names the token. Find it in the `.jack` file, and check that rule. |
| `IndexError: list index out of range` | The parser ran off the end of the tokens | A loop that doesn't stop at `}` or `)`. |
| `RecursionError` | Two functions call each other for ever without eating a token | Every rule must eat at least one token before calling another rule. |

## Talk about it

- What's a grammar? What's a parse tree?
- Why does each grammar rule become one function?
- How does the parser tell a variable from an array or a call?
- What's recursive about recursive descent?

## Challenge *(if there's time, or for next time)*

- Make the `SyntaxError` say which line of the `.jack` file it was on.
  *(The tokenizer would need to remember each token's line.)*
- Draw the parse tree for `if (x < 3) { do Output.printInt(x); }`.
- Add a `<` to a test file by mistake, like `let x = < 3;`. What does your
  parser say?

## Checkpoint

The learner can, without help:
- [ ] Explain grammar, parsing and parse trees
- [ ] Draw the parse tree of a short `let` statement
- [ ] Explain how their parser decides which rule comes next
- [ ] Pass `check-xml parse` for all seven files

## Lab notebook

Draw the parse tree from step 2. Write three grammar rules next to the
functions they became. Commit. Add *grammar*, *parse*, *parser*, *parse
tree* and *recursive descent* to `dictionary.md`. Tick Project 10 on the
passport.

## Guide's background *(optional reading)*

This completes Nand to Tetris Project 10. Jack's grammar is designed so
that the parser can always decide what comes next by looking at the next
token, or in one place (a name inside a term) at the token after it:
an **LL(1)** grammar, apart from that one place, which needs LL(2). That
makes a hand-written **recursive descent** parser, one function per
rule, straightforward. Real compilers for C, Go and Rust use the same
technique.

The grammar table in this lesson is the book's grammar, written in
words. The starting program gives the helper methods and two worked
rules; the learner writes the other fourteen. The parser's XML output
is thrown away in Lesson 8.15, where each function writes VM code
instead, but the structure stays exactly the same, which is why this
lesson matters.

ExpressionLessSquare exists so the learner can test statements before
writing expressions, as step 7 does.
