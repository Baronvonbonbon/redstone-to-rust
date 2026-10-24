# Lesson 11.14: Trust No Input

**Time:** 2 sessions of 45 min · **You need:** a terminal with two tabs;
a text editor; `~/lab/net/web` from Lesson 11.7; `~/lab/sql/minecraft.db`
from Lesson 5.14; the Hacker's Pledge · **New words:** vulnerability,
path traversal, SQL injection, placeholder, 403, defence in depth

## Goal *(read this to the learner)*

> In Lesson 11.6, sneaky messages broke the Diamond Vault, and you
> fixed it by checking every input. Today you'll hunt for two more
> famous kinds of bug, in programs you wrote yourself: a web server
> that shows files it shouldn't, and a database that runs words you
> typed as if they were commands. Then you'll fix them both.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] `~/lab/net/web` works (`cargo run` there, from Lesson 11.7).
- [ ] `~/lab/sql/minecraft.db` exists. If not: `./scripts/give-lab.sh
      LEARNER sql`, then, as the learner, `cd ~/lab/sql && sqlite3
      minecraft.db < minecraft.sql`.
- [ ] Read the Hacker's Pledge together again
      ([docs/HACKER-PLEDGE.md](../../docs/HACKER-PLEDGE.md)). Today is
      exactly what rule 1 is for: these are the learner's own programs,
      on the learner's own computer, listening only on `127.0.0.1`.

## Warm-up (5 min)

"What did the sneaky vault visitors send?" *(`TAKE 99`, `PUT lots`, a
giant number.)* "What was the rule that fixed them all?" *(Check every
input before using it; never trust what a visitor sends.)* **Say:** "A
bug that lets someone do something they shouldn't is called a
**vulnerability**. Finding them in your *own* programs is one of the
most useful things a programmer can do."

## Activity

### Session 1: escaping the site folder

1. **Where does the server look?** In `~/lab/net/web`, open
   `src/main.rs`, and find:
   ```rust
   format!("site{target}")
   ```
   **Ask:** "If Firefox asks for `/rules.html`, which file does it
   open?" *(`site/rules.html`.)* "What does `..` mean in a path?"
   *(The folder above: Stage 1.)* "So what would `/../Cargo.toml`
   open?" *(`site/../Cargo.toml`, which is `Cargo.toml`, outside the
   site!)*

2. **Try it, on your own server.** Tab 1: `cargo run`. Tab 2:
   ```
   curl -i http://127.0.0.1:7880/../Cargo.toml
   ```
   **They should see** `HTTP/1.0 404 Not Found`. **Say:** "Interesting!
   `curl` tidies up the `..` before sending, like Firefox does. But a
   sneaky visitor doesn't have to use a tidy program." Tell `curl` to
   send the path exactly as written:
   ```
   curl -i --path-as-is http://127.0.0.1:7880/../Cargo.toml
   ```
   **They should see:**
   ```
   HTTP/1.0 200 OK
   Content-Type: text/plain; charset=utf-8
   Content-Length: 74

   [package]
   name = "web"
   version = "0.1.0"
   edition = "2024"

   [dependencies]
   ```
   Then `curl --path-as-is http://127.0.0.1:7880/../src/main.rs`. **They
   should see** the server's own program. **Ask:** "What else could a
   visitor read, with enough `../`?" *(Any file the server's user can
   read: other projects, notes, maybe secrets.)* **Say:** "This is
   called **path traversal**: walking out of the folder you're meant to
   stay in. It's been found in real web servers many times." Look at tab
   1's log: **they should see** the sneaky requests,
   `GET /../Cargo.toml HTTP/1.1`.

3. **Fix it.** Stop the server (Ctrl+C). Under `NOT_FOUND`, add:
   ```rust
   const FORBIDDEN: &[u8] = b"<h1>403: nice try!</h1>";
   ```
   and change the `let (status, kind, body) = match ...` part to:
   ```rust
   let (status, kind, body) = if target.contains("..") {
       ("403 Forbidden", "text/html", FORBIDDEN.to_vec())
   } else {
       match fs::read(&path) {
           Ok(body) => ("200 OK", content_type(&path), body),
           Err(_) => ("404 Not Found", "text/html", NOT_FOUND.to_vec()),
       }
   };
   ```
   `cargo run`, and try the sneaky request again. **They should see:**
   ```
   HTTP/1.0 403 Forbidden
   Content-Type: text/html
   Content-Length: 23

   <h1>403: nice try!</h1>
   ```
   Check the real pages still work in Firefox. **Say:** "`403` means 'I
   understood, and the answer's no.'" **Ask:** "This also refuses a page
   called `a..b.html`. Is that bad?" *(Not really: we don't have one. When
   in doubt, refuse. It's much safer than trying to allow exactly the
   bad things through.)* Commit: "Refuse paths with .. in them".

### Session 2: words that become commands

4. **A mob finder.** Copy the database, so the original stays safe:
   ```
   cp ~/lab/sql/minecraft.db ~/lab/net/python/
   cd ~/lab/net/python
   ```
   Make `mobs.py`:
   ```python
   import sqlite3

   db = sqlite3.connect("minecraft.db")
   name = input("Which mob? ")
   query = f"SELECT name, health FROM mobs WHERE name = '{name}'"
   print("The query is:", query)
   for row in db.execute(query):
       print(row)
   ```
   `python3 mobs.py`, and type `creeper`. **They should see:**
   ```
   Which mob? creeper
   The query is: SELECT name, health FROM mobs WHERE name = 'creeper'
   ('creeper', 20)
   ```

5. **A quote mark.** Run it again, and type `creeper's`. **They should
   see:**
   ```
   The query is: SELECT name, health FROM mobs WHERE name = 'creeper's'
   Traceback (most recent call last):
     ...
   sqlite3.OperationalError: near "s": syntax error
   ```
   **Ask:** "Look at the query. Where does the name end now?" *(The `'`
   in `creeper's` ended it early, and SQL didn't understand the `s'`
   left over.)* **Say:** "The words we typed became part of the
   *command*. Lesson 5.16's `mob` tool had the same problem."

6. **A clever input.** Run it again and type exactly:
   ```
   nobody' OR '1'='1
   ```
   **They should see:**
   ```
   The query is: SELECT name, health FROM mobs WHERE name = 'nobody' OR '1'='1'
   ('chicken', 4)
   ('cow', 10)
   ('pig', 10)
   ...
   ```
   and every mob in the database. **Ask:** "Read the query out loud.
   Why did every mob come back?" *(It now says "where the name is
   nobody, OR one equals one", and one always equals one.)* **Say:**
   "That's **SQL injection**: sneaking your own SQL into someone else's
   query. On a website, the same trick could show other people's
   accounts, or change things. It's one of the most common web bugs ever
   found, and you just found it in your own program."

7. **Fix it with a placeholder.** Change the two `query` lines to:
   ```python
   query = "SELECT name, health FROM mobs WHERE name = ?"
   for row in db.execute(query, (name,)):
   ```
   (and delete the `print("The query is:" ...)` line). Try all three
   inputs again. **They should see** `('creeper', 20)` for `creeper`, and
   nothing at all for the other two: no error, no extra mobs. **Say:**
   "The `?` is a **placeholder**. The query and the name now travel
   separately, so SQL treats the name only as a name, never as
   commands, whatever's in it." *(`(name,)` is a tuple with one thing in
   it: the comma makes it a tuple.)* Commit: "Use a placeholder".

8. **The same idea everywhere.** On paper, make a table with three
   rows, and fill it in together:

   | Bug | The input | What went wrong | The fix |
   |---|---|---|---|
   | The vault (11.6) | `TAKE 99` | The number wasn't checked | Check it, refuse with `NO` |
   | Path traversal | `/../Cargo.toml` | The path left the folder | Refuse `..` |
   | SQL injection | `nobody' OR '1'='1` | Words became commands | Use a placeholder |

   **Say:** "The rule is always the same: **trust no input**. Check it,
   or keep it separate from commands."

9. **Memory bugs, and why Rust helps.** **Ask:** "Remember Lesson 8.3,
   when `strcpy` wrote past the end of a C array, and the stack guard
   noticed?" **Say:** "If an attacker chooses what's written past the
   end, they might change where the program goes next. To make that
   harder, Linux uses several defences at once: the stack guard, which
   notices the overwrite; and moving programs to a different address
   every time they run (Lesson 8.2), so an attacker can't know where
   anything is. Using several defences, so one mistake isn't enough, is
   called **defence in depth**." **Ask:** "What did Rust do in Lesson
   11.6, when the vault went below zero?" *(It stopped with `attempt to
   subtract with overflow`, instead of carrying on with a wrong
   number.)* "And when you use an index past the end of a `Vec`?" *(It
   stops with `index out of bounds`.)* **Say:** "Rust checks, every
   time, so a whole family of attacks can't happen in safe Rust. That's
   one of the biggest reasons it was invented."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| The sneaky `curl` gets `404`, even with `--path-as-is` | The server was started somewhere else, or `Cargo.toml` isn't one folder above `site` | Run `cargo run` in `~/lab/net/web`. |
| ``error[E0308]: `if` and `else` have incompatible types`` | The `if` and `else` give back different kinds of things | Both sides must give `(&str, &str, Vec<u8>)`: check `.to_vec()` on both. |
| The real pages are `403` after the fix | `contains("..")` is checking `path`, not `target` | It should be `target`. |
| `sqlite3.OperationalError: no such table: mobs` | `minecraft.db` isn't in this folder, so Python made a new, empty one | `ls -l minecraft.db`; copy it again from `~/lab/sql`. |
| `sqlite3.ProgrammingError: Incorrect number of bindings supplied. The current statement uses 1, and there are 7 supplied.` | `(name)` without the comma: Python sees the 7 letters of `creeper`, not a tuple | Write `(name,)`. |

## Talk about it

- What's a vulnerability? Why is it good to find them in your own
  programs?
- How did `..` get out of the site folder? Why does refusing it work?
- Why did `'` break the query? What does a placeholder do differently?
- What's "defence in depth"? Name two defences against memory bugs.
- Why is it only OK to try these tricks on your own programs? (The
  Pledge.)

## Challenge *(if there's time, or for next time)*

- Make the web server safer still: only serve names made of letters,
  digits, `-`, `_` and `.`, with `target[1..].chars().all(...)`. That's
  an **allow list**: say what's allowed, and refuse everything else.
- Fix Lesson 5.16's `mob` tool, if you made it, by rewriting it in
  Python with a `?`. *(Pasting `$1` into a command in Bash has no easy
  safe version.)*
- Look back at the vault from Lesson 11.6: is there any input you
  haven't tried? Write a list of five sneaky inputs and test them all.

## Checkpoint

The learner can, without help:
- [ ] Show path traversal on their own server, and explain the fix
- [ ] Show SQL injection in `mobs.py`, and fix it with a placeholder
- [ ] Say the rule, "trust no input", with three examples
- [ ] Explain defence in depth, and why Rust's checks help
- [ ] Say why these tricks are only for their own programs

## Lab notebook

Copy the table from step 8. Draw the query from step 6, with the part
that came from the user in a different colour. Commit. Add
*vulnerability*, *path traversal*, *SQL injection*, *placeholder*, *403*
and *defence in depth* to `dictionary.md`.

## Guide's background *(optional reading)*

Path traversal, SQL injection and memory-safety bugs are all in the
**OWASP Top Ten** and the **CWE Top 25**, the lists the industry uses
for its most common serious weaknesses. The underlying lesson,
**separate code from data**, also covers cross-site scripting (a web
page showing a visitor's text as HTML), command injection (pasting
input into a shell command, as `$1` in Stage 5's tools could) and
format-string bugs in C.

`contains("..")` is a blunt fix that works here because the server never
decodes `%2e%2e` or follows links; real servers resolve the full path
(`fs::canonicalize`) and check that it still starts with the site
folder, because attackers try encoded and doubled forms. The
`OR '1'='1` input is the textbook demonstration; the comic **xkcd 327**
("Exploits of a Mom") is a famous joke about it, for the guide to
judge. Parameterised queries (`?`) are the real fix in every language,
and Rust's database crates use them too.

Linux's memory defences: stack protectors (the "stack smashing
detected" guard from Lesson 8.3), **ASLR** (address space layout
randomisation, the moving addresses of Lesson 8.2), and
non-executable stacks. Each one alone can sometimes be got round;
together they're much stronger, which is the sense of defence in depth.
Lesson 7.12's randomised hash tables are the same thinking: unpredictable
on purpose, so an attacker can't plan ahead. **OWASP Juice Shop** (in
the resources list) is a deliberately vulnerable shop for practising
these bugs legally on your own computer, in Docker (downloaded once),
for an older learner with the guide.
