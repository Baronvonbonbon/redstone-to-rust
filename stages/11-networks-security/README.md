# Stage 11: Networks & Security

**Badge:** Net Ninja · **Needs first:** Stage 10; the [Hacker's
Pledge](../../docs/HACKER-PLEDGE.md) · **Lessons:** 16

The learner finds out how computers talk to each other, then how to keep
those conversations safe. The first half follows a packet from the
Sandbox to the other side of the world, and ends with the learner's
own servers in Rust. The second half is the secret-code thread's
finale: why the old codes break, and how the real ones work, all from
the clock arithmetic of Lesson 11.8. The stage ends with defences, and a
puzzle trail the learner builds for someone else.

- **Networks** (Lessons 11.1–11.4): packets and addresses, with the
  Sandbox as a second computer; routes, the gateway and TTL, with
  `tracepath`; DNS, from `/etc/hosts` to the root servers; ports, the TCP
  handshake, and the learner's own packets seen with `tcpdump`, inside
  the Sandbox.
- **Servers** (11.5–11.7): the Shouty server and a client in Rust, with a
  thread per visitor; the Diamond Vault, its protocol, and the sneaky
  inputs that break it; HTTP by hand, and the Creeper Club's web server
  in Rust.
- **Codes** (11.8–11.13): clock arithmetic and predictable "random"
  numbers; a Caesar and keyword code cracker; fingerprints (hashes);
  dice passphrases; a key exchange with paint and powers; public keys,
  signatures, `ssh` keys and certificates.
- **Defence** (11.14–11.16): path traversal and SQL injection found and
  fixed in the learner's own programs; open ports, a firewall and
  updates in the Sandbox; and the puzzle trail project, with the Stage
  11 checkpoint.

Every program in the lessons was run, every error message is a real one,
and every terminal output is from a real run (with your numbers, names
and addresses being different). The network lessons were tested between
a Sandbox and a family computer, and the web server in a real browser.

## Safety: everything stays at home

This stage teaches how attacks work, so it has firm edges, and the guide
should know them:

- **Only the learner's own things.** Every attack in the stage is on a
  program the learner wrote, on the family computer or the Sandbox. The
  Hacker's Pledge is read before Lesson 11.4 (the first `tcpdump`) and
  again before 11.14.
- **Servers listen on `127.0.0.1`.** Nothing the learner writes can be
  reached from elsewhere on the home network.
- **`tcpdump` only in the Sandbox,** on the Sandbox's own traffic.
- **No password cracking.** Passwords are taught as counting
  possibilities, dice passphrases, and the rules for keeping them
  (Lesson 11.11).
- **Online wargames are optional,** with the guide, and only ones that
  invite players (Lesson 11.16's Guide's background).

## Tools

- **The Sandbox, rebuilt for Stage 11.** It adds `ping`, `tracepath`,
  `dig`, `tcpdump`, `curl`, `ufw` and `openssl`, and `sandbox.sh` now starts
  it with permission to run its own firewall. Online, from
  `labs/sandbox`, before Lesson 11.1:
  ```
  ./sandbox.sh build LEARNER
  ./sandbox.sh reset
  ```
  then, in the learner's account, `ssh-keygen -R '[localhost]:2222'`
  (the rebuilt Sandbox has a new identity). The reset sets the password
  back to the learner's name.
- **The Stage 11 packages** on the family computer: `dig`, `tracepath`,
  `curl` and `openssl`. From your own account, while online:
  `./scripts/install-packages.sh --later`.
- **The net lab**, from your own account: `./scripts/give-lab.sh LEARNER
  net` (before Lesson 11.9). The [net lab handbook](../../labs/net/README.md)
  has the answers and an example puzzle trail.
- Rust and Cargo from Stage 9, Python 3, `nc` from Stage 5, and the
  Stage 5 SQL lab (`minecraft.db`, Lesson 11.14).
- **(Free, in the offline library)** *Computer Networks: A Systems
  Approach*, by Larry Peterson and Bruce Davie (CC BY). Each lesson's
  "Guide's background" says which section it follows. It's written for
  university students, so it's for the guide, or for reading together.
- **(Optional)** Dice: three per learner (Lesson 11.11). Food colouring
  and cups (Lesson 11.12). A padlock (Lesson 11.13).

## A note on the internet

Every lesson works offline, between the family computer and the
Sandbox. Some steps reach the real internet (`ping 1.1.1.1`,
`tracepath`, `dig`, the HTTPS and certificate steps, and `apt update`),
and each one is marked as optional.

## Lessons

| # | Lesson | What happens | Key ideas |
|---|---|---|---|
| 11.1 | [Messages in Envelopes](01-packets.md) | The envelope game; addresses in binary; `ping` between the family computer and the Sandbox | packets, layers, IP addresses |
| 11.2 | [Hop by Hop](02-routes.md) | Being routers; `ip route`; a little internet in Python that loops; `tracepath` | routing, gateway, TTL |
| 11.3 | [The Internet's Phone Book](03-names.md) | `/etc/hosts` in the Sandbox; `dig` and `+trace`; a pretend DNS with a cache | DNS, caching |
| 11.4 | [Ports, Handshakes and Spying on Yourself](04-conversations.md) | `nc` chats; the handshake act-out; `tcpdump` in the Sandbox; why `ssh` can't be read | ports, TCP, plaintext |
| 11.5 | [The Shouty Server](05-server.md) | A Rust server and client; one visitor at a time, then threads; the rude visitor | sockets, threads |
| 11.6 | [The Diamond Vault](06-vault.md) | A protocol; a shared vault with a `Mutex`; sneaky inputs; checking everything | protocols, input validation |
| 11.7 | [The Web, by Hand and in Rust](07-web.md) | HTTP typed into `nc`; the Creeper Club's site; a Rust web server in Firefox | HTTP, status codes |
| 11.8 | [Clock Arithmetic](08-clock-arithmetic.md) | Caesar as `% 26`; multiplying ciphers and inverses; predicting "random" codes | modular arithmetic |
| 11.9 | [The Code Cracker](09-code-cracker.md) | Trying every key; counting letters; a keyword cipher and a dictionary of guesses | brute force, frequency analysis |
| 11.10 | [Fingerprints: Hashes](10-fingerprints.md) | A toy hash and its clashes; SHA-256; catching a changed file; git's commit IDs | hashes, collisions |
| 11.11 | [Dice Passphrases](11-passphrases.md) | Counting possibilities; rolling a passphrase; the Sandbox's new password; the rules | randomness, passphrases |
| 11.12 | [A Secret in Front of Everyone](12-shared-secrets.md) | The paint trick; Diffie–Hellman in Python; AES with `openssl`; the man in the middle | key exchange |
| 11.13 | [Padlocks and Signatures](13-public-keys.md) | Tiny RSA from two primes; an `ssh` key; signing the club rules; certificates | public keys, signatures |
| 11.14 | [Trust No Input](14-trust-no-input.md) | Path traversal and SQL injection in the learner's own programs, and the fixes; memory defences | vulnerabilities |
| 11.15 | [Walls and Doors](15-walls-and-doors.md) | Open ports; a `ufw` firewall in the Sandbox; locking yourself out; changelogs and updates | firewalls, updates |
| 11.16 | [Project: The Puzzle Trail](16-puzzle-trail.md) | Design, build and play-test a trail for someone else; Stage 11 checkpoint | design, play-testing |

## Setup notes

- The learner's Stage 11 work lives in `~/lab/net`: `python` (a git
  repository, made in Lesson 11.2) for the Python programs; one folder
  per Rust project (`shouty`, `knock`, `vault`, `robot`, `web`), each its
  own repository from `cargo new`; plus `secrets` and `words.txt` from
  the net lab, and `signed` (Lesson 11.13).
- Lesson 11.1 asks for the Sandbox's address on a sticky note. It's
  usually `172.17.0.2`, but can change if other containers are running;
  `ip -br addr` in the Sandbox shows it.
- Changes inside the Sandbox (the passphrase of 11.11, the key of 11.13,
  `/etc/hosts` lines of 11.3) are lost by `./sandbox.sh reset`. That's
  fine: the learner can do them again.
- The family computer's own firewall, if it has one, may stop the Sandbox
  from reaching servers on the family computer. No lesson needs that
  direction except one demonstration in 11.5, which shows it *failing*
  either way.

## Free play for this stage

- More pages for the Creeper Club website, and more commands for the
  Diamond Vault.
- A chat server: everyone who connects sees everyone else's messages
  (threads plus a shared `Vec` of connections in a `Mutex`).
- Encode and crack messages for friends and siblings, with `clock.py` and
  `wordlock.py`.
- Sign the lab notebook's commits with the `ssh` key (`git config
  gpg.format ssh`; see `man git-config`).
- For an older learner: *Computer Networks: A Systems Approach*; *Beej's
  Guide to Network Programming* (C sockets, online); OWASP Juice Shop
  with the guide (Lesson 11.14's Guide's background).

## Habits to build now

- **Ask before you poke.** The Pledge, every time: is it mine, or was I
  invited?
- **Trust no input.** Check it, refuse what's odd, or keep it apart from
  commands.
- **Bind to `127.0.0.1`.** Open a door to the world only on purpose.
- **Let chance choose secrets.** Dice and `secrets`, never a favourite
  word or `random`.
- **`cargo fmt`, `cargo clippy`, commit** (as in Stage 9).

## Checkpoint

The learner can, without help:
- [ ] Explain how a packet gets from the Sandbox to the internet:
      addresses, routes, the gateway and TTL
- [ ] Explain DNS, ports and the TCP handshake, with `dig`, `ss` and
      `tcpdump` as evidence
- [ ] Write a threaded Rust server on `127.0.0.1` that survives sneaky
      input
- [ ] Explain why Caesar and keyword ciphers break, and count the
      possibilities for a passphrase
- [ ] Explain hashes, key exchange and signatures, with the toy versions
- [ ] Find and fix path traversal and SQL injection in their own code
- [ ] Set up a default-deny firewall without locking themselves out

They can also:
- [ ] Log in to the Sandbox with their own `ssh` key, and sign a file
- [ ] Run a puzzle trail they designed, played by someone else
      (Lesson 11.16)
