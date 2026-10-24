# The Net Lab: the Guide's Handbook

Stage 11 (Networks & Security) happens in the learner's `~/lab/net`
folder, plus the Sandbox. This lab gives the learner two things:

| File | What it is | Lessons |
|---|---|---|
| `secrets/` | Three secret messages to crack | 11.9 |
| `words.txt` | 216 child-friendly words, one for each roll of three dice (`111 acorn` to `666 wizard`) | 11.11 |

This folder also has, for **you**, an example puzzle trail and its
tested riddle-door server (`riddle-door.rs`), for Lesson 11.16. It
isn't copied to the learner: designing their own trail is the project.

## Setting it up

From your own account:
```
./scripts/give-lab.sh LEARNER net
```
It puts `secrets/` and `words.txt` in the learner's `~/lab/net/`. It never
touches anything else there (the learner's projects live there too), so
it's safe to run again, for example to get fresh copies of the messages.

Stage 11 also needs:

- **The Sandbox, rebuilt** with the network tools and permission to run a
  firewall. Online, in `labs/sandbox`: `./sandbox.sh build LEARNER`, then
  `./sandbox.sh reset`. In the learner's account:
  `ssh-keygen -R '[localhost]:2222'`. See the [Sandbox
  handbook](../sandbox/README.md).
- **The networking packages** on the family computer: `./scripts/install-packages.sh
  --later` (it includes `dig` and `tracepath`; `tcpdump` is only
  needed inside the Sandbox, which has it).
- The Stage 5 SQL lab, for Lesson 11.14 (`give-lab.sh LEARNER sql`), and
  Rust from Stage 9.

## The answers (Lesson 11.9)

Don't show these to the learner: cracking them is the lesson.

| File | Cipher | Key | Message |
|---|---|---|---|
| `message1.txt` | Caesar | +7 | MEET ME BY THE TREEHOUSE AFTER LUNCH. BRING THE BANANA. |
| `message2.txt` | Caesar | +19 | A story: a school inspector slips on a banana, falls in the pond and is chased by the goose patrol. It begins THE SCHOOL INSPECTOR ARRIVED ON MONDAY MORNING. |
| `message3.txt` | Keyword | OCELOT | THE SECRET DIAMOND STASH IS UNDER THE THIRD SPRUCE TREE NORTH OF THE VILLAGE WELL. DIG DOWN SEVEN BLOCKS AND WATCH OUT FOR LAVA. |

`crack.py` finds the first two by scoring every key; the second is long,
so letter counting works too. The third needs the dictionary attack
with `keys.txt`, which must include `OCELOT` (the lesson's list does).

To make new messages for a sibling, use the learner's own `clock.py`
(Caesar) or `wordlock.py` (keyword) from Lessons 11.8 and 11.9.

## About `words.txt`

Written for this course: 216 short, concrete, easy-to-spell words, so
that a six-word passphrase from it has 216⁶ (about 10¹⁴) possibilities.
That's plenty for the Sandbox and for a family computer login, where
each guess is slow. For anything important, use eight words from it, or
six from a full Diceware list (the EFF's long list has 7776 words, for
five dice). Lesson 11.11's Guide's background explains why.

## An example puzzle trail

For Lesson 11.16. Use it to judge whether the learner's plan is the
right size, or as a hint if they're stuck. Four steps:

1. **The note** (Caesar, Lesson 11.8). `START.txt` in the player's home
   folder tells a short story and ends with a code made with `clock.py`'s
   `shift`, key 3: `WKH GRRU LV RQ SRUW IRXU WZR IRXU WZR` ("THE DOOR IS
   ON PORT FOUR TWO FOUR TWO").
2. **The riddle door** (a server, Lessons 11.5 and 11.14). `riddle-door.rs`
   listens on `127.0.0.1:4242`. `nc 127.0.0.1 4242` asks "What has keys
   but can't open locks?". The answer `piano` (any capitals, spaces
   ignored) gets the next clue; anything else gets "Not quite. Try
   again!". It survives the rude visitor and empty lines.
3. **The locked file** (Lesson 11.12). The clue leads to a book, and in
   it, a slip of paper: `openssl enc -d -aes-256-cbc -pbkdf2 -in
   treasure-map.enc -pass pass:piano`. Unlocking it gives a map to the
   treasure file.
4. **The treasure** (Lessons 11.10 and 11.13). `treasure.txt`, with
   `treasure.txt.sig` and a `signers.txt` holding the learner's public
   key. The player runs `ssh-keygen -Y verify` and sees `Good "file"
   signature`, proving it's the real treasure.

To try the riddle door:
```
cd ~/lab/net
cargo new riddle-door
cp /path/to/redstone-to-rust/labs/net/riddle-door.rs riddle-door/src/main.rs
cd riddle-door
cargo run
```
and, in a second terminal, `nc 127.0.0.1 4242`. It's the Shouty server
from Lesson 11.5, with a riddle and a check of each line, and its
`visit` function uses `?` (Lesson 9.9) to stop quietly if the visitor
leaves or sends bytes that aren't text.

## Good to know

- **Everything stays on this computer.** The learner's servers listen on
  `127.0.0.1`, so nothing else on the home network can reach them; the
  Sandbox is reachable only from this computer; and `tcpdump` is only
  used inside the Sandbox, on the Sandbox's own traffic. The Hacker's
  Pledge ([docs/HACKER-PLEDGE.md](../../docs/HACKER-PLEDGE.md)) is read
  before the first `tcpdump` (Lesson 11.4) and before Lesson 11.14.
- **Internet.** Only some steps need it (`dig`, `tracepath`, `curl` to
  real websites, `apt update`), and each lesson marks them as optional.
- **Firewalls.** If the family computer runs `ufw`, the Sandbox can't
  connect to servers on it; no lesson needs that. Lesson 11.15's
  firewall is inside the Sandbox only.
