# Lesson 12.13: Build a Database: The Chest

**Time:** 2–3 sessions of 45 min · **You need:** a terminal with two
tabs; a text editor; `~/lab/lang`; paper · **New words:** key-value
store, persistence, log, append, replay, crash, `fsync`, compaction,
atomic

## Goal *(read this to the learner)*

> SQLite remembers things even after the computer is switched off. How?
> Today you'll build your own small database in Rust, the Chest: put
> things in, get them out, and keep them safe in a file, even if the
> program is killed halfway. Then you'll tidy the file up without ever
> risking the data.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] The Diamond Vault (Lesson 11.6) had a protocol of one-line
      commands; the Chest's commands are like it.

## Warm-up (5 min)

"When a Pickaxe program ends, what happens to its variables?" *(They're
gone: they were only in memory.)* "How could a program remember things
for next time?" *(Write them to a file.)* **Say:** "Remembering after
the program stops is called **persistence**. Today: how to do it
safely."

## Activity

### Session 1: a chest in memory

1. **What it does.** **Say:** "The Chest is a **key-value store**: every
   thing has a name (the key) and a value, like a Python dictionary or
   a Rust `HashMap`. Four commands:" Write them:
   ```
   put KEY VALUE     store a value (the value may have spaces)
   get KEY           show it
   del KEY           remove it
   list              show every key
   ```

2. **The first chest.**
   ```
   cd ~/lab/lang
   cargo new chest
   cd chest
   ```
   `src/main.rs`:
   ```rust
   use std::collections::BTreeMap;
   use std::io::{self, BufRead, Write};

   // Do one command to the chest, and say what happened.
   fn command(items: &mut BTreeMap<String, String>, line: &str) -> String {
       let mut words = line.splitn(3, ' ');
       match (words.next(), words.next(), words.next()) {
           (Some("put"), Some(key), Some(value)) => {
               items.insert(key.to_string(), value.to_string());
               "OK".to_string()
           }
           (Some("get"), Some(key), None) => match items.get(key) {
               Some(value) => value.clone(),
               None => format!("there's no {key}"),
           },
           (Some("del"), Some(key), None) => match items.remove(key) {
               Some(_) => "OK".to_string(),
               None => format!("there's no {key}"),
           },
           (Some("list"), None, None) => {
               let keys: Vec<&str> = items.keys().map(|k| k.as_str()).collect();
               keys.join(" ")
           }
           _ => "try: put KEY VALUE, get KEY, del KEY or list".to_string(),
       }
   }

   fn main() {
       let mut items = BTreeMap::new();
       print!("chest> ");
       io::stdout().flush().unwrap();
       for line in io::stdin().lock().lines() {
           let Ok(line) = line else { break };
           println!("{}", command(&mut items, line.trim()));
           print!("chest> ");
           io::stdout().flush().unwrap();
       }
       println!();
   }
   ```
   Read it together:
   - "`splitn(3, ' ')` splits at spaces, but into at most 3 pieces, so
     the value keeps its spaces."
   - "`match` on all three pieces at once: the pattern says exactly
     what each command needs."
   - "A **`BTreeMap`** is like a `HashMap`, but kept in order, in a tree
     (Lesson 7.13), so `list` comes out alphabetical."

3. **Try it.** `cargo run`:
   ```
   chest> put diamonds 12
   OK
   chest> put motto Ssssss! said the creeper
   OK
   chest> get motto
   Ssssss! said the creeper
   chest> get gold
   there's no gold
   chest> put diamonds 13
   OK
   chest> list
   diamonds motto
   chest> del motto
   OK
   chest> dig
   try: put KEY VALUE, get KEY, del KEY or list
   ```
   Press Ctrl+D, and `cargo run` again. `list`. **Ask:** "Where did
   everything go?" *(It was only in memory.)* Commit.

### Session 2: a log that remembers

4. **The idea: write down every change.** **Say:** "Instead of saving
   the whole chest, we'll write each *change* on a new line at the end
   of a file, like a diary. That's called a **log**. Adding to the end
   is called **appending**. To open the chest, read the diary from the
   start and do every change again: that's **replaying**." Act it out:
   the learner writes `put diamonds 12`, `put torches 64`, `put diamonds
   13`, `del torches` on paper. **Ask:** "What's in the chest at the
   end?" *(Just `diamonds 13`.)*

5. **The chest, with a log.** Replace `src/main.rs`:
   ```rust
   use std::collections::BTreeMap;
   use std::fs::{self, File, OpenOptions};
   use std::io::{self, BufRead, Write};

   const LOG: &str = "chest.log";

   struct Chest {
       items: BTreeMap<String, String>,
       log: File,
   }

   impl Chest {
       // Open the chest: replay every change in the log, in order.
       fn open() -> io::Result<Chest> {
           let mut items = BTreeMap::new();
           if let Ok(text) = fs::read_to_string(LOG) {
               for line in text.lines() {
                   change(&mut items, line);
               }
           }
           let log = OpenOptions::new().create(true).append(true).open(LOG)?;
           Ok(Chest { items, log })
       }

       // Write the change to the log first, then make it.
       fn record(&mut self, line: &str) -> io::Result<String> {
           writeln!(self.log, "{line}")?;
           self.log.sync_all()?;
           Ok(change(&mut self.items, line))
       }

       // Write a fresh log with only what's in the chest now.
       fn compact(&mut self) -> io::Result<String> {
           let mut fresh = File::create("chest.new")?;
           for (key, value) in &self.items {
               writeln!(fresh, "put {key} {value}")?;
           }
           fresh.sync_all()?;
           fs::rename("chest.new", LOG)?;
           self.log = OpenOptions::new().append(true).open(LOG)?;
           Ok(format!("OK, {} lines", self.items.len()))
       }

       fn command(&mut self, line: &str) -> io::Result<String> {
           let mut words = line.splitn(3, ' ');
           Ok(match (words.next(), words.next(), words.next()) {
               (Some("put"), Some(_), Some(_)) | (Some("del"), Some(_), None) => self.record(line)?,
               (Some("get"), Some(key), None) => match self.items.get(key) {
                   Some(value) => value.clone(),
                   None => format!("there's no {key}"),
               },
               (Some("list"), None, None) => {
                   let keys: Vec<&str> = self.items.keys().map(|k| k.as_str()).collect();
                   keys.join(" ")
               }
               (Some("compact"), None, None) => self.compact()?,
               _ => "try: put KEY VALUE, get KEY, del KEY, list or compact".to_string(),
           })
       }
   }

   // Make one change (a put or a del) to the items.
   fn change(items: &mut BTreeMap<String, String>, line: &str) -> String {
       let mut words = line.splitn(3, ' ');
       match (words.next(), words.next(), words.next()) {
           (Some("put"), Some(key), Some(value)) => {
               items.insert(key.to_string(), value.to_string());
               "OK".to_string()
           }
           (Some("del"), Some(key), None) => match items.remove(key) {
               Some(_) => "OK".to_string(),
               None => format!("there's no {key}"),
           },
           _ => format!("I don't understand: {line}"),
       }
   }

   fn main() {
       let mut chest = match Chest::open() {
           Ok(chest) => chest,
           Err(problem) => {
               eprintln!("I can't open the chest: {problem}");
               return;
           }
       };
       println!("The chest has {} things in it.", chest.items.len());
       print!("chest> ");
       io::stdout().flush().unwrap();
       for line in io::stdin().lock().lines() {
           let Ok(line) = line else { break };
           match chest.command(line.trim()) {
               Ok(answer) => println!("{answer}"),
               Err(problem) => println!("Oops: {problem}"),
           }
           print!("chest> ");
           io::stdout().flush().unwrap();
       }
       println!();
   }
   ```
   Read it in this order:
   - "`change` is the old `put` and `del`. The log is just a list of the
     commands you typed, so the same function both does a command and
     replays the log."
   - "`open` replays the log, then opens it for **appending**."
   - "`record` writes the line to the log *first*, then changes the
     chest. `sync_all` tells the operating system: 'really write this to
     the disk, now'. (Stage 10: the kernel normally keeps writes in
     memory for a while.)"
   - "`get` and `list` don't change anything, so they aren't logged."
   - "Ignore `compact` for now."

6. **It remembers.** `cargo run`:
   ```
   The chest has 0 things in it.
   chest> put diamonds 12
   OK
   chest> put motto Ssssss! said the creeper
   OK
   chest> put diamonds 13
   OK
   chest> del motto
   OK
   chest> put torches 64
   OK
   chest> list
   diamonds torches
   ```
   Ctrl+D, then `cat chest.log`. **They should see:**
   ```
   put diamonds 12
   put motto Ssssss! said the creeper
   put diamonds 13
   del motto
   put torches 64
   ```
   `cargo run` again. **They should see** `The chest has 2 things in
   it.`, and `get diamonds` gives `13`. **Say:** "It remembered, by
   replaying the diary."

7. **Pull the plug.** **Say:** "What if the program crashes, or the
   power goes off, in the middle?" In tab 1, `cargo run`, and `put pickaxe
   iron`. In tab 2, kill it without warning:
   ```
   pkill -9 -x chest
   ```
   Tab 1 stops dead (it may say `Killed`). `cargo run` again, and `get pickaxe`. **They
   should see:** `iron`. **Say:** "`-9` gives the program no chance to
   save anything. But the change was already on the disk, because
   `record` wrote and synced it *before* saying OK. That rule, 'write the
   log first', is how real databases survive crashes."

### Session 3: compaction

8. **The diary gets long.** **Ask:** "If you change `diamonds` 1000 times,
   how long is the log?" Try it, from the `chest` folder:
   ```
   for i in $(seq 1 1000); do echo "put diamonds $i"; done | cargo run -q
   wc -l chest.log
   ```
   **They should see** about `1005 chest.log`. **Ask:** "How many of
   those lines matter?" *(Only the last `diamonds`, and `torches`, and
   `pickaxe`.)*

9. **Tidy up, safely.** **Say:** "`compact` writes a fresh log with just
   what's in the chest now. But what if the power goes off *while*
   writing it? We'd have half a log, and lose things." Read `compact`:
   it writes to a *new* file, `chest.new`, syncs it, and only then
   `rename`s it over `chest.log`. **Say:** "A rename is **atomic**: it
   happens completely or not at all. At every moment, there's a whole,
   good `chest.log` on the disk: the old one, or the new one." `cargo
   run`:
   ```
   chest> compact
   OK, 3 lines
   chest> get diamonds
   1000
   ```
   `cat chest.log`: three `put` lines. Commit (add `chest.log` to
   `.gitignore`: it's data, not code).

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `put motto Ssssss!` stores only `Ssssss!`, and the rest is lost | `split(' ')` was used instead of `splitn(3, ' ')` | Use `splitn(3, ' ')`. |
| The chest forgets everything | `chest.log` is being read from a different folder | Always `cargo run` in `~/lab/lang/chest`; the log is in the folder you start from. |
| `get` commands appear in `chest.log` | `record` is called for every command | Only `put` and `del` are logged. |
| After `compact`, new `put`s are lost | `self.log` still points at the old file | Open `LOG` again after `rename`, as `compact` does. |
| `pkill -9 -x chest` does nothing | The project has a different name, so the program does too | `pgrep -l .` lists programs; use the chest's name. |

## Talk about it

- What's a key-value store? Which Rust and Python things are like it?
- How does the log make the chest remember? What's replaying?
- Why write the log *before* saying OK?
- Why does `compact` write a new file and rename it, instead of
  rewriting `chest.log` directly?

## Challenge *(if there's time, or for next time)*

- Add `count`, which says how many things are in the chest.
- Make the chest `compact` by itself when the log has more than 100
  lines.
- Make the Diamond Vault from Lesson 11.6 keep its diamonds in a log,
  so they survive a restart.

## Checkpoint

The learner can, without help:
- [ ] Explain a key-value store, and use the Chest's commands
- [ ] Explain the log: append, replay, and what `cat chest.log` shows
- [ ] Show the chest surviving `pkill -9`, and explain why
- [ ] Explain why `compact` uses a new file and an atomic rename

## Lab notebook

Draw the log as a diary, and the chest it replays into. Draw the two
files during `compact`, and say which one is safe at each moment.
Commit. Add *key-value store*, *persistence*, *log*, *append*,
*replay*, *compaction* and *atomic* to `dictionary.md`.

## Guide's background *(optional reading)*

This is a **log-structured** store, the design of Bitcask and the core
idea of the **write-ahead log** that SQLite (in WAL mode), PostgreSQL
and most other databases use: record the change durably first, then
apply it, so that a crash can be recovered by replaying. Compaction by
writing a new file and renaming it is the standard way to replace a
file safely on Linux; strictly, a fully crash-safe version also syncs
the directory after the rename.

Two simplifications are worth knowing. A crash *during* a write can
leave a half-written last line; `change` ignores lines it doesn't
understand, which covers most cases, and real databases add a checksum
(Lesson 11.10) to every record. And `sync_all` after every `put` is
slow on a real disk (which is why databases group writes into
transactions, Lesson 12.12). *Designing Data-Intensive Applications*
(Kleppmann, not free) Chapter 3 is the classic explanation; *Let's
Build a Simple Database* in the offline library takes the other road,
to B-trees.
