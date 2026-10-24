# Lesson 11.5: The Shouty Server

**Time:** 2–3 sessions of 45 min · **You need:** a terminal with three
tabs; a text editor; `~/lab/net`; the Sandbox (step 8) · **New words:**
server, client, socket, `TcpListener`, `TcpStream`, bind, `127.0.0.1`
vs `0.0.0.0`

## Goal *(read this to the learner)*

> So far, `nc` has done the talking. Now you'll write your own
> **server**: a program that waits at a door for visitors, in Rust. It's
> the Shouty Server: whatever you say to it, it SHOUTS BACK!!! Then
> you'll write a **client** that visits it, make it handle lots of
> visitors at once, and find out who's allowed to knock.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Stage 9's Rust and Stage 10's threads (Lesson 10.6) are used here.

## Warm-up (5 min)

"What does `nc -l 7000` do?" *(Listens at door 7000.)* "And `nc
172.17.0.4 7000`?" *(Knocks on that door, on that computer.)* "Which one
is waiting for visitors?" *(The `-l` one.)* **Say:** "A program that
waits for visitors is a **server**. A program that visits is a
**client**."

## Activity

### Session 1: a server

1. **A new project:**
   ```
   cd ~/lab/net
   cargo new shouty
   cd shouty
   ```
   `src/main.rs`:
   ```rust
   use std::io::{BufRead, BufReader, Write};
   use std::net::TcpListener;

   fn main() {
       let listener = TcpListener::bind("127.0.0.1:7878").unwrap();
       println!("Listening on {}", listener.local_addr().unwrap());
       for stream in listener.incoming() {
           let mut stream = stream.unwrap();
           let who = stream.peer_addr().unwrap();
           println!("{who} knocked!");
           let reader = BufReader::new(stream.try_clone().unwrap());
           for line in reader.lines() {
               let line = line.unwrap();
               println!("{who} said: {line}");
               writeln!(stream, "{}!!!", line.to_uppercase()).unwrap();
           }
           println!("{who} left.");
       }
   }
   ```
   Read it together, line by line. **Say:**
   - "`bind` asks the kernel for door 7878, at the address `127.0.0.1`.
     A `TcpListener` is a door with someone listening behind it."
   - "`incoming()` waits for knocks. Each visitor arrives as a
     `TcpStream`: a two-way pipe to that visitor. It's like a file you
     can read *and* write, except the other end is another program."
   - "We read their lines with a `BufReader`, like reading a file in
     Stage 9. `try_clone` makes a second handle on the same stream, so
     we can read with one and write with the other."
   - "`writeln!` works on streams just like `println!` works on the
     screen. `peer_addr` is the visitor's address and door."

2. **Run it, and visit.** Tab 1: `cargo run`. **They should see:**
   `Listening on 127.0.0.1:7878`. Tab 2:
   ```
   nc 127.0.0.1 7878
   ```
   Type `hello`, Enter, then `tra-la-laaa`, Enter. **They should see**,
   in tab 2:
   ```
   HELLO!!!
   TRA-LA-LAAA!!!
   ```
   and in tab 1:
   ```
   127.0.0.1:44632 knocked!
   127.0.0.1:44632 said: hello
   127.0.0.1:44632 said: tra-la-laaa
   ```
   Ctrl+C in tab 2. **They should see** `127.0.0.1:44632 left.` in tab 1.

3. **One door, one server.** Leave it running in tab 1, and in tab 2,
   start a second copy: `cargo run`. **They should see:**
   ```
   called `Result::unwrap()` on an `Err` value: Os { code: 98, kind: AddrInUse, message: "Address already in use" }
   ```
   **Say:** "Only one program can listen at a door. The kernel said no,
   and `unwrap` turned that into a panic."

### Session 2: lots of visitors

4. **Two at once.** Server running in tab 1. Tab 2: `nc 127.0.0.1 7878`,
   and type `i am first`. Tab 3: `nc 127.0.0.1 7878`, and type `i am
   second`. **They should see:** tab 2 gets `I AM FIRST!!!`, but tab 3
   gets **nothing**. **Ask:** "Why?" *(The server is stuck in the
   `for line` loop, talking to the first visitor. It won't go back to
   `incoming()` until they leave.)* Ctrl+C in **tab 2** (the first
   visitor). **They should see** `I AM SECOND!!!` arrive in tab 3 at
   once. **Say:** "The second visitor was waiting at the door all along.
   The kernel even kept their message safe."

   (If you Ctrl+C the *second* visitor instead, the server may crash
   with `Broken pipe` later, when it tries to shout back to someone who
   has gone. That's the next fix's job too.)

5. **A thread for each visitor.** Change `main.rs` to:
   ```rust
   use std::io::{BufRead, BufReader, Write};
   use std::net::{TcpListener, TcpStream};
   use std::thread;

   fn talk(mut stream: TcpStream) {
       let who = stream.peer_addr().unwrap();
       println!("{who} knocked!");
       let reader = BufReader::new(stream.try_clone().unwrap());
       for line in reader.lines() {
           let line = line.unwrap();
           println!("{who} said: {line}");
           writeln!(stream, "{}!!!", line.to_uppercase()).unwrap();
       }
       println!("{who} left.");
   }

   fn main() {
       let listener = TcpListener::bind("127.0.0.1:7878").unwrap();
       println!("Listening on {}", listener.local_addr().unwrap());
       for stream in listener.incoming() {
           let stream = stream.unwrap();
           thread::spawn(move || talk(stream));
       }
   }
   ```
   **Say:** "Now `main` only answers the door. Each visitor gets their
   own thread, running `talk`, and `main` goes straight back to wait
   for the next knock. Like Lesson 10.6's miners." Stop the old server
   (Ctrl+C), `cargo run`, and do step 4 again. **They should see:** both
   visitors get shouted at, straight away. Commit.

6. **A rude visitor.** **Say:** "What if a visitor sends something that
   isn't text?" Tab 2:
   ```
   printf 'caf\xe9\n' | nc -N 127.0.0.1 7878
   ```
   (`\xe9` is a single byte, 233, that isn't allowed on its own in
   UTF-8, from Stage 4.) **They should see**, in tab 1:
   ```
   127.0.0.1:32980 knocked!

   thread '<unnamed>' (406) panicked at src/main.rs:10:25:
   called `Result::unwrap()` on an `Err` value: Error { kind: InvalidData, message: "stream did not contain valid UTF-8" }
   ```
   Now visit normally with `nc 127.0.0.1 7878`. **Ask:** "Is the server
   still working?" *(Yes! Only that visitor's thread crashed.)* "What
   would have happened with the first version, without threads?" *(The
   whole server would have crashed, for everybody, because of one rude
   visitor.)* **Say:** "Remember that. A server must never trust what
   visitors send. We'll come back to it."

### Session 3: a client, and who can knock

7. **A client in Rust.** In a new project, `~/lab/net/knock`:
   ```rust
   use std::io::{BufRead, BufReader, Write};
   use std::net::TcpStream;

   fn main() {
       let mut stream = TcpStream::connect("127.0.0.1:7878").unwrap();
       let mut reader = BufReader::new(stream.try_clone().unwrap());
       for words in ["hello", "tra-la-laaa", "creepers are green"] {
           writeln!(stream, "{words}").unwrap();
           let mut answer = String::new();
           reader.read_line(&mut answer).unwrap();
           print!("I said {words:?}. It said {answer}");
       }
   }
   ```
   With the server running, `cargo run`. **They should see:**
   ```
   I said "hello". It said HELLO!!!
   I said "tra-la-laaa". It said TRA-LA-LAAA!!!
   I said "creepers are green". It said CREEPERS ARE GREEN!!!
   ```
   **Say:** "`connect` is the client's half: it knocks, the handshake
   happens, and we get a stream. `print!`, not `println!`, because the
   answer already ends with a newline." Stop the server and run `knock`
   again. **They should see** `kind: ConnectionRefused`. Commit.

8. **Who can knock?** Start the server again. Log in to the Sandbox, and
   try to visit the family computer's server from there:
   ```
   nc -v -w 3 172.17.0.1 7878
   ```
   **They should see** it fail: either `Connection refused`, or (if the
   family computer has a firewall switched on) `timed out`. **Say:** "We
   told `bind` to listen at `127.0.0.1`: the loopback, the door that
   only leads back inside. Nobody outside this computer can reach it,
   not even the Sandbox. That's exactly what we want for programs we're
   still building."

   **Ask:** "What if we used `0.0.0.0:7878`?" **Say:** "`0.0.0.0` means
   'every door this computer has', Wi-Fi included. Then any device in
   the house could visit, and if the router let them, people outside.
   Real servers do that on purpose. Ours never will, unless a grown-up
   has helped check it's safe." Write that rule in the notebook.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `kind: AddrInUse, message: "Address already in use"` | Another copy of the server (or `nc`) is using 7878 | Ctrl+C the other one. `ss -tlnp` shows who has it. |
| `kind: ConnectionRefused` | The server isn't running, or the port's wrong | Start it in another tab; check both say 7878. |
| `kind: BrokenPipe, message: "Broken pipe"` in the first version | It shouted back to a visitor who had already gone | The threads version (step 5) only loses that visitor's thread. |
| `nc` waits, and nothing comes back | The first version, busy with another visitor | That's step 4: leave with the first visitor, or use threads. |
| `error[E0599]: no method named \`lines\` found for struct \`BufReader<R>\` in the current scope` | `BufRead` isn't in the `use` line | `use std::io::{BufRead, BufReader, Write};`. |
| `error[E0599]: cannot write into \`TcpStream\`` | `Write` isn't in the `use` line | As above. |

## Talk about it

- What's the difference between a server and a client?
- Why did the second visitor have to wait, and how did threads fix it?
- One rude visitor: what happened with threads, and what would have
  happened without?
- What's the difference between `127.0.0.1` and `0.0.0.0`?

## Challenge *(if there's time, or for next time)*

- Make the server count visitors, and greet each one: `You are visitor
  number 3!` *(An `AtomicU32`, from Lesson 10.6, shared by all the
  threads.)*
- Make it whisper instead: lowercase, with `...` at the end.
- Make `knock` take the words from the command line
  (`std::env::args`), so `cargo run -- hi there` sends `hi there`.

## Checkpoint

The learner can, without help:
- [ ] Write a server with `TcpListener`, and a client with `TcpStream`
- [ ] Explain why the first version made visitors wait
- [ ] Give each visitor a thread
- [ ] Explain `127.0.0.1` and `0.0.0.0`, and which one to use

## Lab notebook

Draw the server, its door at `127.0.0.1:7878`, and two visitors with a
thread each. Write the rule from step 8. Commit. Add *server*, *client*,
*socket*, *bind*, *TcpListener* and *TcpStream* to `dictionary.md`.

## Guide's background *(optional reading)*

These are **sockets**, the programming interface for networks since
1983 (from BSD Unix): `bind` claims an address and port, `listen` and
`accept` wait for connections (Rust's `TcpListener::bind` and
`incoming` do those), and `connect` dials out. Each accepted connection
is a file descriptor, like a file or a pipe in Stage 10, which is why
reading and writing it looks the same. *The Rust Programming Language*,
Chapter 21 (`rustup doc --book`), builds a web server the same way, and
Lesson 11.7 does too. *Beej's Guide to Network Programming* explains the
same calls in C.

A thread per connection is the simplest way to serve many clients, and
fine for dozens; big servers use thread pools or `async` code to handle
thousands. Step 6 is the first appearance of a theme of the security
half of this stage: a server is a program that strangers can send
input to, so every assumption about that input is a possible bug. One
thread's panic doesn't stop the others; a panic in `main`, or in the
first version, stops everything, which is called a **denial of service**.

Step 8's result depends on the family computer: with no firewall, the
Sandbox's knock is refused (nothing is listening on that address);
with a firewall, the knock is silently dropped and times out. Either
way, binding to `127.0.0.1` keeps the program private.
