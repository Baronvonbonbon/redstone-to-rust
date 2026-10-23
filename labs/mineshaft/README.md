# Mineshaft: the Guide's Handbook

Mineshaft is an offline wargame, in the spirit of OverTheWire's Bandit.
It's a tiny Linux system in a Docker container with 21 accounts,
`miner0` to `miner20`. Each level hides the password for the next one.
It needs no internet and no accounts, and the passwords are random for
every build.

- **Learner's view:** [LEVELS.md](LEVELS.md) (every level's goal; each one is
  also in `GOAL.txt` inside the level).
- **Stage 1** uses levels 0–9, and **Stage 5** uses levels 10–19.

## Running it

Run everything from the **guide's** account (the learner's account must
not be in the `docker` group):

```bash
./mineshaft.sh build     # once, while online (about 2 minutes)
./mineshaft.sh start     # starts it; it restarts by itself after a reboot
./mineshaft.sh status
./mineshaft.sh answers   # every password, for the guide only
./mineshaft.sh reset     # new passwords (a fresh start, or for a sibling)
./mineshaft.sh stop
./test_solutions.sh      # plays every level automatically; all should say "ok"
```

The learner connects with: `ssh miner0@localhost -p 2220` (password `miner0`).

It only listens on `localhost`, so nobody else on your network can reach it.

## Levels: hints and solutions

Give hints **one at a time**, in order. Solutions are for you; only use
one with the learner as a last resort, and then have them redo the level
on their own the next day.

| Lvl | Teaches | Hint 1 | Hint 2 | Solution |
|---|---|---|---|---|
| 0 | `ssh`, `cat` | Read GOAL.txt | What command shows a file? | `cat readme` |
| 1 | `cd` | What's here? (`ls`) | You can walk into folders | `cd tunnel` then `cat gem.txt` |
| 2 | spaces in names | Why does `cat diamond ore.txt` give two errors? | Quotes, or press Tab | `cat "diamond ore.txt"` |
| 3 | hidden files | Some files are invisible to plain `ls` | `ls -a` | `cat .secret-chest` |
| 4 | `file` | Try `cat` on a few chests: what do you see? | `file chests/*` says what each one is | `file chests/*`, then `cat` the one that says "text" |
| 5 | `find -name` | Too many folders to search by hand | `find` searches everywhere | `find cave -name diamond`, then `cat` that path |
| 6 | `grep` | Too long to read | grep shows only matching lines | `grep PASSWORD mining-log.txt` |
| 7 | `sort \| uniq -u` | `uniq` only notices repeats that are next to each other | Sort first, then pipe | `sort ores.txt \| uniq -u` |
| 8 | `head \| tail` | `head -n 7777` gets the first 7777 lines | The last of those is line 7777 | `head -n 7777 long-tunnel.txt \| tail -n 1` |
| 9 | `base64 -d` | Read `base64 --help` | `-d` decodes | `base64 -d creeper-code.txt` |
| 10 | `tr` (ROT13) | Remember Caesar's wheel, key 13? | The goal has the full command | `tr 'A-Za-z' 'N-ZA-Mn-za-m' < scrambled.txt` |
| 11 | `mktemp`, `tar`, `zcat` | Your home is read-only, so unpack somewhere else | `tar -xzf` unpacks; `zcat` reads `.gz` | `cd "$(mktemp -d)"`, `tar -xzf ~/buried.tar.gz`, `zcat treasure/map.txt.gz` |
| 12 | `find -size -executable` | Read `find --help` about `-size` | Bytes are written `1234c`; `!` means "not" | `find storage -size 1234c ! -executable`, then `cat` it |
| 13 | `--help`, setuid | Run `./door` | Then `./door --help` | `./door --knock 3 --say please` |
| 14 | environment variables | `env` lists them all | Look for something called SECRET | `env \| grep SECRET` or `echo $MINESHAFT_SECRET` |
| 15 | `diff` | `diff` shows lines that differ | Lines starting with `>` are from the second file | `diff old-map.txt new-map.txt` |
| 16 | `nc`, ports | Connect with `nc localhost 30016` | Type *this* level's password (miner16's) | `nc localhost 30016`, paste miner16's password, press Enter, then Ctrl+C to hang up |
| 17 | `ps` | `ps aux` lists every running program | Pipe into `grep gem` | `ps aux \| grep gem` |
| 18 | `git log -p` | `cd journal` and `git log` | `-p` shows what each change was | `cd journal && git log -p` |
| 19 | writing a network client | Read `vault-notes.txt` | Write a loop: read a question, work out the sum, send it, read "CORRECT" | See below |
| 20 | summit | — | — | `cat trophy.txt` |

### Level 19 solution (Python)

```python
import socket

f = socket.create_connection(("localhost", 30019)).makefile("rw")
print(f.readline())                     # HELLO MINER...
for _ in range(20):
    words = f.readline().split()        # ['WHAT', 'IS', '4821', '+', '9932?']
    answer = int(words[2]) + int(words[4].rstrip("?"))
    f.write(f"{answer}\n")
    f.flush()
    print(f.readline().strip())         # CORRECT
print(f.readline())                     # the password
```

The learner writes it in a scratch folder (`cd "$(mktemp -d)"` then
`nano vault.py`, and runs it with `python3 vault.py`). Expect several
tries; reading the guard's exact words matters.

## How it works (for curious guides, and for Stage 8)

- `build_levels.py` runs once while the image builds. It makes the users,
  picks random word-based passwords, and builds each level. The level
  goals live in its `GOALS` table; `python3 build_levels.py --print-goals > LEVELS.md`
  regenerates the learner's page.
- Each home folder is owned by `root` and readable only by its miner, so
  you can't look ahead. Homes are read-only, and `/tmp` lets you make
  folders without being able to list other people's.
- Level 13's `door` is a small C program (`door.c`) with the **setuid**
  bit: it runs with miner14's powers, so it can read miner14's password,
  but it only prints it when you give it the right options.
- Levels 16 and 19 are network services in `services.py`. Level 17 is a
  process started by `entrypoint.sh` with the password in its command line.
- Passwords are stored in `/etc/mineshaft/pass/` (each readable only by
  its own miner) and in `/root/answers.txt`.
