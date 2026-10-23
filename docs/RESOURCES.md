# Resources

Everything the course uses, which stage uses it, and whether it works
offline. **Account** means the learner needs to sign up for something;
every row here is "no", except where marked *(optional)*.

Key: **apt** = installed by `scripts/install-packages.sh`.
**lib** = downloaded by `scripts/mirror-library.sh`. **hand** = download
by hand once. **web** = needs the internet each time.

## Games and practice

| Resource | Stage | What it teaches | Offline | License |
|---|---|---|---|---|
| GCompris | 0 | Mouse, keyboard, logic, math, early reading | apt | GPL |
| Tux Typing, Klavaro, GNU Typist | 0–1 | Touch typing | apt | GPL |
| Tux Paint | 0 | Drawing; saving files | apt | GPL |
| cowsay, sl, figlet, lolcat | 1 | Fun with the terminal (we skip `fortune`: its default quotes include adult topics) | apt | various free |
| bashcrawl | 1 | Terminal dungeon crawler | lib | GPL |
| Terminus | 1 | Terminal adventure (web page, opens offline) | lib | GPL-2.0 |
| **Treasure Cave** (this repo) | 1 | `find`, wildcards, `tree` | built in | MIT |
| **The Great Underpants Heist** (this repo) | 1 | `grep`, pipes, `head`/`tail` | built in | MIT |
| **Mineshaft** (this repo) | 1, 5, 8 | 20-level Bandit-style wargame | built in (Docker) | MIT |
| **The Sandbox** (this repo) | 5 | A breakable Linux computer where the learner is admin | built in (Docker) | MIT |
| **Minecraft database** (this repo) | 5 | SQL practice (`give-lab sql`) | built in | MIT |
| bsdgames, moon-buggy, ninvaders | any | Terminal games for free play | apt | BSD/GPL |
| Luanti (Minetest) + Mesecons | 4 | Redstone-style logic circuits | apt | LGPL |
| Digital (hneemann) | 4, 6 | Logic circuit simulator | lib | GPL |
| nandgame.com | 4 | Build a computer from NAND (puzzle game) | web, no account | free |
| Oh My Git! | 5 | Git, as a card game | hand (ohmygit.org) | Blue Oak |
| Learn Git Branching | 5 (optional) | Git branches, visually | web (learngitbranching.js.org, no account) | MIT |
| Command Line Murder Mystery | 5 (optional) | grep practice; **murder theme, so preview it** | lib | free |
| SQL Murder Mystery | 5 (optional) | SQL; **murder theme, so preview it** | lib | MIT |
| Rustlings | 9 | Small Rust exercises in the terminal | `setup-rust.sh` (online once) | MIT |
| Project Euler | 3, 7 | Math programming problems | web to read, no account | CC BY-NC-SA |
| OWASP Juice Shop | 11 | A deliberately hackable web shop, run locally | Docker (online once) | MIT |
| OverTheWire (Bandit, Natas, Krypton, Narnia...) | 11 *(optional)* | Real online wargames, shared public logins, **no personal account** | web | free |

**Left out on purpose:** picoCTF, pwn.college, Exercism, Advent of Code,
Codewars and CodeCombat all need personal accounts. They're excellent,
so you might reconsider them when the learner is old enough for an
account of their own.

## Books and courses

| Resource | Stage | Offline | License |
|---|---|---|---|
| *The Linux Command Line*, William Shotts | 1, 5 | lib (PDF) | CC BY-NC-ND |
| OpenStax *Introduction to Python Programming* | 2–3 | hand (PDF) | CC BY |
| *Invent Your Own Computer Games with Python*, Al Sweigart | 3 | web, free to read | CC BY-NC-SA |
| *The Big Book of Small Python Projects*, Al Sweigart | 3 | web, free to read | CC BY-NC-SA |
| *Think Python 2e*, Allen Downey | 3, 7 | lib (PDF) | CC BY-NC |
| Pygame Zero docs | 3 | `pydoc` / web | LGPL |
| CS Unplugged (activity ideas) | 0 | web | CC BY-NC-SA |
| *The Missing Semester of Your CS Education* (MIT) | 5 | lib | CC BY-NC-SA |
| *The Elements of Computing Systems* (Nand to Tetris book) | 6, 8 | **optional purchase**; free project specs at nand2tetris.org | book: (c) MIT Press |
| Nand to Tetris software suite (desktop, 2.7) | 6, 8 | lib (automatic; hand if it fails) | GPL |
| Nand to Tetris web IDE | 6, 8 (optional) | web (nand2tetris.github.io/web-ide, no account) | MIT |
| **HDL card, Hack card, practice chips** (this repo) | 6 | built in (`labs/n2t`) | CC BY-SA / MIT |
| *Code*, Charles Petzold | 4–6 | **optional purchase**; great bedtime reading | (c) |
| OpenStax *Introduction to Computer Science* | 7 | hand (PDF) | CC BY |
| *Book of Proof*, Richard Hammack | 7 | lib (PDF) | Creative Commons |
| *Open Data Structures* (Python edition), Pat Morin | 7 | lib (PDF) | CC BY |
| *Algorithms*, Jeff Erickson | 7+ | lib (PDF) | CC BY |
| **Algorithms checker and mazes** (this repo) | 7 | built in (`labs/algo`) | MIT |
| *Beej's Guide to C Programming* | 8 | web (PDF free) | CC BY-NC-ND |
| **VM card, Jack card, Stage 8 check scripts, compiler tests, Diamond Dash** (this repo) | 8 | built in (`labs/n2t`, `labs/n2t/stack`) | CC BY-SA / MIT |
| *The Rust Programming Language* | 9 | `rustup doc --book` | MIT/Apache |
| *Rust by Example* | 9 | `rustup doc --rust-by-example` | MIT/Apache |
| *Comprehensive Rust* (Google) | 9 | lib | Apache |
| *Rust Cookbook* | 9 | lib | CC0 |
| Crate kit: rand, regex, lazy_static, serde, serde_json, crossterm | 9 | `setup-rust.sh` (online once) | MIT / MIT-Apache |
| **Rust lab: setup script, check-hack, Creeper Chase** (this repo) | 9 | built in (`labs/rust`) | MIT |
| *Operating Systems: Three Easy Pieces* (OSTEP) | 10 | hand (free chapter PDFs) | free to read |
| *Writing an OS in Rust*, Philipp Oppermann | 10 | lib | free to read; code MIT/Apache |
| xv6 (MIT teaching OS) | 10 *(optional)* | lib | MIT |
| Arch Wiki | 10 | `arch-wiki-docs` in Arch, or web | GFDL |
| *Computer Networks: A Systems Approach* | 11 | lib | CC BY |
| *Beej's Guide to Network Programming* | 11 | web (PDF free) | CC BY-NC-ND |
| *Crafting Interpreters*, Robert Nystrom | 12 | lib (source); web | CC BY-NC-ND (text) |
| *Structure and Interpretation of Computer Programs* | 12 | web | CC BY-SA |
| *Let's Build a Simple Database* (cstack) | 12 | web | free |
| *The Embedded Rust Book* | 13 | lib | MIT/Apache |
| Linux From Scratch | 13 | web (free) | CC BY-NC-SA / MIT |
| OSSU Computer Science | 13 | lib | MIT |
| teachyourselfcs.com | 13 | web | free |

## Hardware (optional)

| Item | Stage | Why |
|---|---|---|
| Raspberry Pi (any model 3 or newer) + 2 microSD cards | 5+ | The breakable computer. A spare card means instant recovery. |
| Raspberry Pi Pico (about $5) | 13 | Embedded Rust; blinking lights and buttons |
| Breadboard, LEDs, resistors, buttons | 4, 13 | Real logic and real circuits |
| An old, unused PC | 4 | Take it apart in Lesson 0.2! |
