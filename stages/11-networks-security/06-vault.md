# Lesson 11.6: The Diamond Vault: a Protocol of Your Own

**Time:** 3 sessions of 45 min · **You need:** a terminal with three
tabs; a text editor; paper; `~/lab/net` · **New words:** protocol
design, command, reply, input validation, overflow, poisoned lock,
denial of service

## Goal *(read this to the learner)*

> You'll design a **protocol**, a language for a client and a server,
> and build a server that keeps diamonds in a vault for everyone who
> visits. Then you'll put on a disguise and be the sneakiest visitor
> you can, against your own vault, and see one cheeky message break it
> for everybody. Then you'll make it unbreakable.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Session 3 is "attack your own program". The Pledge says that's
      fine: it's yours. Say so out loud.

## Warm-up (5 min)

"What did the rude visitor do to the Shouty Server?" *(Sent bytes that
weren't text, and its thread crashed.)* "Why didn't the whole server
crash?" *(Each visitor had their own thread.)*

## Activity

### Session 1: design it, build it

1. **Design on paper first.** **Say:** "A protocol is an agreement. Both
   sides have to know exactly what can be said, and what comes back.
   Let's write ours down before any code." Make this table together:

   | The client sends | The server replies | Meaning |
   |---|---|---|
   | `LOOK` | `OK 10` | How many diamonds are in the vault? |
   | `PUT 5` | `OK 15` | Put 5 in; here's the new total |
   | `TAKE 3` | `OK 12` | Take 3 out; here's the new total |
   | anything else | `NO I don't understand` | |

   **Say:** "Every command is one line. Every reply is one line,
   starting with `OK` or `NO`, so a program can easily tell which. The
   vault starts with 10 diamonds, and everybody shares the same vault."

2. **Build it.** `cargo new vault` in `~/lab/net`. `src/main.rs`:
   ```rust
   use std::io::{BufRead, BufReader, Write};
   use std::net::{TcpListener, TcpStream};
   use std::sync::{Arc, Mutex};
   use std::thread;

   fn answer(command: &str, vault: &Mutex<u32>) -> String {
       let mut diamonds = vault.lock().unwrap();
       let words: Vec<&str> = command.split_whitespace().collect();
       match words.as_slice() {
           ["LOOK"] => format!("OK {diamonds}"),
           ["PUT", number] => {
               let number: u32 = number.parse().unwrap();
               *diamonds += number;
               format!("OK {diamonds}")
           }
           ["TAKE", number] => {
               let number: u32 = number.parse().unwrap();
               *diamonds -= number;
               format!("OK {diamonds}")
           }
           _ => "NO I don't understand".to_string(),
       }
   }

   fn visit(mut stream: TcpStream, vault: Arc<Mutex<u32>>) {
       let who = stream.peer_addr().unwrap();
       println!("{who} came in.");
       let reader = BufReader::new(stream.try_clone().unwrap());
       for line in reader.lines() {
           let line = line.unwrap();
           let reply = answer(&line, &vault);
           println!("{who}: {line} -> {reply}");
           writeln!(stream, "{reply}").unwrap();
       }
       println!("{who} left.");
   }

   fn main() {
       let vault = Arc::new(Mutex::new(10));
       let listener = TcpListener::bind("127.0.0.1:7879").unwrap();
       let address = listener.local_addr().unwrap();
       println!("The Diamond Vault is open on {address}");
       for stream in listener.incoming() {
           let stream = stream.unwrap();
           let vault = Arc::clone(&vault);
           thread::spawn(move || visit(stream, vault));
       }
   }
   ```
   **Say:**
   - "The diamonds live in an `Arc<Mutex<u32>>`, like Lesson 10.6's
     counter: every visitor's thread shares it, and the lock stops two
     of them changing it at once."
   - "`split_whitespace` cuts the command into words. `match` on
     `words.as_slice()` checks the *shape*: `["PUT", number]` matches
     exactly two words, the first being `PUT`, and calls the second one
     `number`."
   - "`answer` is the protocol table, in Rust."

3. **Visit.** Tab 1: `cargo run`. Tab 2: `nc 127.0.0.1 7879`, and type
   `LOOK`, `PUT 5`, `TAKE 3`, `LOOK` and `DANCE`, each with Enter. **They
   should see:**
   ```
   OK 10
   OK 15
   OK 12
   OK 12
   NO I don't understand
   ```
   Open a second visitor in tab 3 and `LOOK`. **Ask:** "Does tab 3 see
   the same 12?" *(Yes: one shared vault.)* Commit.

### Session 2: a robot

4. **A robot client.** **Say:** "Let's check the lock really works, with
   robots putting diamonds in, very fast, all at once." `cargo new
   robot`, and:
   ```rust
   use std::io::{BufRead, BufReader, Write};
   use std::net::TcpStream;

   fn main() {
       let mut stream = TcpStream::connect("127.0.0.1:7879").unwrap();
       let mut reader = BufReader::new(stream.try_clone().unwrap());
       let mut answer = String::new();
       for _ in 0..1000 {
           writeln!(stream, "PUT 1").unwrap();
           answer.clear();
           reader.read_line(&mut answer).unwrap();
       }
       print!("After 1000 diamonds, the vault said: {answer}");
   }
   ```
   `cargo build`. Restart the vault (Ctrl+C, `cargo run`), so it has 10
   again. Then, in `~/lab/net/robot`, run three robots at once:
   ```
   for i in 1 2 3; do ./target/debug/robot & done; wait
   ```
   **They should see** something like:
   ```
   After 1000 diamonds, the vault said: OK 3008
   After 1000 diamonds, the vault said: OK 3009
   After 1000 diamonds, the vault said: OK 3010
   ```
   **Ask:** "10, plus three robots times 1000: what should it be?"
   *(3010.)* "Did any get lost, like the race in Lesson 10.6?" *(No: the
   `Mutex` kept them in order.)* **Say:** "`&` runs each robot in the
   background, and `wait` waits for them all." Commit.

### Session 3: the sneaky visitor

5. **Think like a sneak.** **Say:** "Now you're a sneaky visitor, at your
   own vault. What could you send that the protocol table didn't
   expect?" Let them suggest, and write a list. Good ideas: take more
   than there is; put in a word instead of a number; a negative number;
   a gigantic number. **Ask:** "What *should* the vault say to each?"

6. **Take too many.** Restart the vault. Tab 2: `nc 127.0.0.1 7879`,
   then `TAKE 99`. **They should see:** no reply, and `nc` may end. Tab 1
   shows:
   ```
   127.0.0.1:50476 came in.

   thread '<unnamed>' (239) panicked at src/main.rs:18:13:
   attempt to subtract with overflow
   ```
   **Ask:** "What's 10 take away 99?" *(−89.)* "Can a `u32` hold that?"
   *(No: `u` means unsigned, never negative.)* **Say:** "Rust caught it
   and stopped that thread. Only that visitor's thread, so... is the
   vault fine?" Visit again in tab 3, and `LOOK`. **They should see:**
   nothing, and in tab 1:
   ```
   127.0.0.1:50484 came in.

   thread '<unnamed>' (243) panicked at src/main.rs:7:37:
   called `Result::unwrap()` on an `Err` value: PoisonError { .. }
   ```
   Every visitor from now on gets the same. **Say:** "The sneaky thread
   crashed while it was *holding the lock*, in the middle of changing
   the diamonds. Rust can't know if the number inside is half-changed,
   so it marks the lock as **poisoned**, and `unwrap` panics for every
   visitor after. One message broke the vault for everyone, until
   someone restarts it. That's called a **denial of service**: nobody
   can use it."

7. **More sneaks.** Restart the vault each time, and try `PUT lots`, then
   `PUT 4294967295`. **They should see**, in tab 1:
   ```
   called `Result::unwrap()` on an `Err` value: ParseIntError { kind: InvalidDigit }
   ```
   and:
   ```
   attempt to add with overflow
   ```
   **Ask:** "Why does a huge number break it?" *(10 + 4,294,967,295 is
   too big for a `u32`: its biggest is 2³² − 1, which is exactly
   4,294,967,295.)*

8. **The rule.** **Say:** "Every one of those was the server *trusting*
   what the visitor sent. The rule of every server ever written:
   **never trust the input**. Check everything: is it a number? Is it
   too big? Is it more than there is? Then say `NO`, politely, instead
   of crashing." That's **input validation**. Write the rule in big
   letters in the notebook.

9. **Make it unbreakable.** Change the `PUT` part of `answer` to:
   ```rust
           ["PUT", number] => {
               let Ok(number) = number.parse::<u32>() else {
                   return "NO that's not a number".to_string();
               };
               match diamonds.checked_add(number) {
                   Some(total) => {
                       *diamonds = total;
                       format!("OK {diamonds}")
                   }
                   None => "NO the vault is full".to_string(),
               }
           }
   ```
   and the `TAKE` part to:
   ```rust
           ["TAKE", number] => {
               let Ok(number) = number.parse::<u32>() else {
                   return "NO that's not a number".to_string();
               };
               if number > *diamonds {
                   return format!("NO there are only {diamonds}");
               }
               *diamonds -= number;
               format!("OK {diamonds}")
           }
   ```
   **Say:**
   - "`let Ok(number) = ... else { ... }` means: if it's an `Ok`, take
     the number out; otherwise, do the `else` part, which must leave
     (here, `return`). It's a short `match` with one good case."
   - "`checked_add` adds, but gives `None` instead of overflowing."
   - "`TAKE` checks there are enough *before* taking."

   And in `visit`, don't trust the line, or the visitor still being
   there:
   ```rust
       for line in reader.lines() {
           let Ok(line) = line else {
               println!("{who} sent something that isn't text.");
               break;
           };
           let reply = answer(&line, &vault);
           println!("{who}: {line} -> {reply}");
           if writeln!(stream, "{reply}").is_err() {
               break;
           }
       }
   ```
   and in `main`, `let stream = stream.unwrap();` becomes:
   ```rust
           let Ok(stream) = stream else { continue };
   ```

10. **Attack it again.** Restart the vault, and send every sneaky thing in
    one visit: `TAKE 99`, `PUT lots`, `PUT 4294967295`, `PUT -5`, `TAKE`
    and `LOOK`. **They should see:**
    ```
    NO there are only 10
    NO that's not a number
    NO the vault is full
    NO that's not a number
    NO I don't understand
    OK 10
    ```
    Then the rude visitor from Lesson 11.5:
    ```
    printf 'caf\xe9\n' | nc -N 127.0.0.1 7879
    ```
    **They should see**, in tab 1, `127.0.0.1:50518 sent something that
    isn't text.`, and the vault still works for the next visitor. Run
    the robots again too: still 3010. Run `cargo clippy`. Commit.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| Every reply is `NO I don't understand` | Lower-case commands: `look` isn't `LOOK` | Use capitals (or see the Challenge). |
| `PoisonError { .. }` for everyone | Step 6: an earlier visitor crashed while holding the lock | Restart the vault (Ctrl+C, `cargo run`). Step 9 fixes it for good. |
| The robots say `ConnectionRefused` | The vault isn't running | Start it in tab 1 first. |
| The robots end with less than 3010 | The vault didn't start at 10 (it was used before) | Restart it, then run the robots. |
| `error[E0308]: \`else\` clause of \`let...else\` does not diverge` | The `else` part doesn't leave | It must `return` (or `break`, or `continue`). |
| `warning: unused \`Result\` that must be used` | `writeln!` without `.unwrap()` or `.is_err()` | Use `if writeln!(...).is_err() { break; }`. |

## Talk about it

- What's in our protocol? Why does every reply start with `OK` or `NO`?
- How did one visitor break the vault for everybody?
- What's a poisoned lock, and why does Rust poison it?
- What does "never trust the input" mean? Give three examples from today.

## Challenge *(if there's time, or for next time)*

- Make commands work in lower case too (`command.to_uppercase()`, before
  splitting).
- Add `HELP`, which replies with a list of the commands, on one line.
- Add a limit: the vault holds at most 1,000,000 diamonds.
- Make a `thief` robot that sends `TAKE 1` 1000 times. Run it with two
  `robot`s. What's left?

## Checkpoint

The learner can, without help:
- [ ] Design a small protocol on paper, with commands and replies
- [ ] Build a server with a shared `Arc<Mutex<...>>`
- [ ] Find at least three inputs that broke the first vault, and explain
      why
- [ ] Fix them with checks, `checked_add` and `let ... else`

## Lab notebook

Copy the protocol table. List every sneaky input you tried, what it did
to the first vault, and what the fixed vault says. Write NEVER TRUST
THE INPUT. Commit. Add *protocol*, *input validation*, *overflow*,
*poisoned lock* and *denial of service* to `dictionary.md`.

## Guide's background *(optional reading)*

Real protocols are designed the same way: SMTP (email) and FTP use
one-line text commands and replies that start with a number (`250 OK`),
and HTTP (Lesson 11.7) is similar. Writing the table first is what the
internet's standards documents, the RFCs, do: each one says exactly
what may be sent and what must come back.

The bugs in step 6 and 7 are real classes of security bug.
**Integer overflow**: Rust panics in debug builds and, by default,
silently wraps in release builds, so a release-built `TAKE 99` would
have left 4,294,967,207 diamonds: a thief's dream. (C behaves like the
release build, which is why integer overflows have been behind many
real attacks.) **Denial of service** is making a service unusable for
others; here, by poisoning a shared lock. Rust's lock poisoning is a
safety feature: it refuses to let other threads see data that may have
been left half-changed.

Lesson 11.14 comes back to input validation with two famous examples,
SQL injection and path traversal, against the learner's own programs.
