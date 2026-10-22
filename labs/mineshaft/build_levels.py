#!/usr/bin/env python3
"""Build the Mineshaft levels inside the container image.

Run with --print-goals (anywhere, no root needed) to print the level goals as
Markdown; that output is LEVELS.md, so the goals have one source of truth.
"""
import base64
import codecs
import grp
import gzip
import io
import os
import random
import subprocess
import sys
import tarfile

LAST = 20  # miner20 is the summit: no puzzle, just a celebration

WORDS = """apple badger bacon banjo beetle biscuit blizzard bubble cactus
carrot castle cheese chicken cloud cobble comet cookie cricket crystal
dragon dynamo eagle ember falcon fossil frog galaxy garlic gecko glitter
goblin gravel hamster hedgehog iceberg igloo jelly jungle kettle koala
lantern lava lemon llama magma marble meteor mitten muffin narwhal nugget
octopus otter panda pebble penguin pickle pirate pizza planet potato
pretzel puddle pumpkin quartz rabbit rainbow robot rocket saddle salmon
sandwich sapling slime snorkel socks sprout squid sticker taco thunder
tiger toast tomato tornado trumpet turnip turtle unicorn velcro volcano
waffle walrus wizard wombat yeti zebra zipper""".split()

GOALS = {
    0: """Welcome to the Mineshaft! You are logged in as miner0.
The password for the next level (miner1) is in a file called `readme`
right here in your home folder. Read it with `cat`.
Then type `exit` and log in again as miner1:
    ssh miner1@localhost -p 2220""",
    1: """The password is in a file called `gem.txt` inside the folder `tunnel`.
Commands that help: ls, cd, cat""",
    2: """The password is in a file whose name has a SPACE in it.
The terminal thinks a space means "next thing". How do you tell it the
space is part of the name? (Try quotes, or try pressing Tab.)""",
    3: """The password is in a chest... but the chest is hidden.
Files whose names start with a dot (.) are hidden. Which `ls` option
shows hidden files? (Hint: `ls --help` or ask your guide about `-a`.)""",
    4: """There are ten chests in the `chests` folder. Nine are full of
garbled junk. Only one holds words a human can read.
The `file` command tells you what kind of thing a file is:
    file chests/*""",
    5: """Somewhere deep inside the `cave` folder is a file named exactly
`diamond`. There are a LOT of folders. Don't search by hand.
Command that helps: find   (try: find cave -name diamond)""",
    6: """The password is in `mining-log.txt`, on the only line that contains
the word PASSWORD. The file is 2000 lines long.
Command that helps: grep""",
    7: """`ores.txt` is full of passwords. Every one of them appears two or
more times, except the real one, which appears exactly once.
Commands that help: sort, uniq, and the pipe |
(Read about the -u option in `uniq --help`.)""",
    8: """`long-tunnel.txt` has 10000 lines. The password is on line 7777.
Commands that help: head, tail, and the pipe |
(How could you get the first 7777 lines, and then just the last one?)""",
    9: """A creeper has scrambled the password in `creeper-code.txt` using a
code called base64. Base64 is not a secret code: anyone can undo it.
Command that helps: base64   (read `base64 --help` and look for "decode")""",
    10: """The password in `scrambled.txt` has had every letter turned 13
places along the alphabet (A becomes N, B becomes O...). This is called
ROT13. Doing it twice gets you back where you started!
Command that helps: tr   (try: tr 'A-Za-z' 'N-ZA-Mn-za-m' < scrambled.txt)""",
    11: """The password is buried in `buried.tar.gz`, a squashed bundle of
files. Your home folder is read-only, so make a scratch folder first:
    cd "$(mktemp -d)"
Then unpack it with tar, look around, and use zcat on anything ending
in .gz.   Commands that help: mktemp, tar, ls, zcat""",
    12: """The `storage` folder has hundreds of files. The password is in the
only file that is exactly 1234 bytes big AND is not executable.
Command that helps: find   (read `find --help` about -size and -executable;
a size in bytes is written like 1234c)""",
    13: """There is a door here: `./door`. It is a program. Programs usually
tell you how to use them if you ask for help. Open the door.""",
    14: """Every program carries a little bag of notes called ENVIRONMENT
VARIABLES. One of yours is holding the password.
Commands that help: env, echo $NAME, grep""",
    15: """`old-map.txt` and `new-map.txt` are almost the same. The password
is the line in new-map.txt that changed.
Command that helps: diff""",
    16: """A gatekeeper program is listening on port 30016 of this computer.
Connect to it, then type in the password for THIS level (miner16)
and press Enter. It will give you the next one.
When you have it, press Ctrl+C to hang up.
Command that helps: nc   (try: nc localhost 30016)""",
    17: """Someone left a program running, and they typed the password right
into its command line where everyone can see it. Find the running
programs and look for something about gems.
Commands that help: ps aux, grep""",
    18: """`journal` is a git repository: a folder that remembers every change
ever made. Someone wrote the password in it, then deleted it. But git
remembers! Go into `journal` and look at its history.
Commands that help: git log, git log -p, git show""",
    19: """THE FINAL VAULT. A guard on port 30019 asks 20 addition problems.
You only get 1 second for each one, so you can't type fast enough.
You need to write a PROGRAM that talks to the guard for you.
Read `vault-notes.txt` for how the guard talks. Then write a script
(Python works great) in a scratch folder made with mktemp -d.""",
    20: """You reached the bottom of the Mineshaft. Read `trophy.txt`.""",
}


def say(text):
    return f"The password for the next level is: {text}\n"


def write(path, data, mode=0o640):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb" if isinstance(data, bytes) else "w") as f:
        f.write(data)
    os.chmod(path, mode)


def build():
    rng = random.Random()
    word = lambda: f"{rng.choice(WORDS)}-{rng.choice(WORDS)}-{rng.randint(10, 99)}"
    pw = {0: "miner0"}
    for n in range(1, LAST + 1):
        while (p := word()) in pw.values():
            pass
        pw[n] = p

    os.makedirs("/etc/mineshaft/pass", exist_ok=True)
    for n in range(LAST + 1):
        u = f"miner{n}"
        subprocess.run(["useradd", "-m", "-s", "/bin/bash", u], check=True)
        subprocess.run(["chpasswd"], input=f"{u}:{pw[n]}\n", text=True, check=True)
        p = f"/etc/mineshaft/pass/{u}"
        write(p, pw[n] + "\n", 0o400)
        subprocess.run(["chown", f"{u}:{u}", p], check=True)

    with open("/root/answers.txt", "w") as f:
        for n in range(LAST + 1):
            f.write(f"miner{n:<3} {pw[n]}\n")
    os.chmod("/root/answers.txt", 0o600)

    def home(n):
        return f"/home/miner{n}"

    for n in range(LAST + 1):
        h = home(n)
        for name in os.listdir(h):  # drop skeleton dotfiles except .bashrc/.profile
            if name not in (".bashrc", ".profile"):
                os.remove(os.path.join(h, name))
        write(f"{h}/GOAL.txt", f"LEVEL {n}\n\n{GOALS[n]}\n")

    nxt = lambda n: pw[n + 1]

    # 0: cat a file
    write(f"{home(0)}/readme", "Nice digging! " + say(nxt(0)))
    # 1: cd into a folder
    write(f"{home(1)}/tunnel/gem.txt", say(nxt(1)))
    for d in ("rock.txt", "dirt.txt"):
        write(f"{home(1)}/tunnel/{d}", "Just a boring old block. Keep looking!\n")
    # 2: space in a filename
    write(f"{home(2)}/diamond ore.txt", say(nxt(2)))
    # 3: hidden file
    write(f"{home(3)}/chest", "Nope! This chest is empty. Is there another chest you can't see?\n")
    write(f"{home(3)}/.secret-chest", say(nxt(3)))
    # 4: file type
    good = rng.randrange(10)
    for i in range(10):
        data = say(nxt(4)).encode() if i == good else bytes(rng.randrange(256) for _ in range(300))
        write(f"{home(4)}/chests/chest-{i:02}", data)
    # 5: find by name
    names = ["stone", "dirt", "gravel", "coal", "iron", "granite"]
    dirs = [f"{home(5)}/cave"]
    for depth in range(4):
        new = []
        for d in dirs:
            for k in range(3):
                nd = f"{d}/{rng.choice(['passage', 'tunnel', 'shaft', 'cavern'])}-{depth}{k}"
                new.append(nd)
                for nm in rng.sample(names, 3):
                    write(f"{nd}/{nm}", f"It's {nm}. Not a diamond.\n")
        dirs = new
    write(f"{rng.choice(dirs)}/diamond", say(nxt(5)))
    # 6: grep
    lines = [f"Mined {rng.randint(1, 64)} {rng.choice(names)} at depth {rng.randint(1, 60)}." for _ in range(2000)]
    lines[rng.randrange(2000)] = f"The PASSWORD is {nxt(6)}"
    write(f"{home(6)}/mining-log.txt", "\n".join(lines) + "\n")
    # 7: sort | uniq -u
    decoys = set()
    while len(decoys) < 60:
        if (w := word()) not in pw.values():
            decoys.add(w)
    lines = [d for d in decoys for _ in range(rng.randint(2, 5))] + [nxt(7)]
    rng.shuffle(lines)
    write(f"{home(7)}/ores.txt", "\n".join(lines) + "\n")
    # 8: head | tail
    lines = [word() for _ in range(10000)]
    lines[7776] = nxt(8)
    write(f"{home(8)}/long-tunnel.txt", "\n".join(lines) + "\n")
    # 9: base64
    write(f"{home(9)}/creeper-code.txt", base64.encodebytes(say(nxt(9)).encode()).decode())
    # 10: rot13
    write(f"{home(10)}/scrambled.txt", codecs.encode(say(nxt(10)), "rot13"))
    # 11: tar + gzip
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tf:
        def add(name, data):
            ti = tarfile.TarInfo(name)
            ti.size = len(data)
            ti.mode = 0o644
            tf.addfile(ti, io.BytesIO(data))
        add("treasure/note.txt", b"Almost there! Squashed files end in .gz. Try zcat.\n")
        add("treasure/map.txt.gz", gzip.compress(say(nxt(11)).encode()))
        add("treasure/rock.txt", b"Just a rock.\n")
    write(f"{home(11)}/buried.tar.gz", buf.getvalue())
    # 12: find -size -executable
    target = rng.randrange(300)
    for i in range(300):
        path = f"{home(12)}/storage/box-{i // 30:02}/item-{i:03}"
        if i == target:
            body = say(nxt(12))
            write(path, body + " " * (1233 - len(body)) + "\n")
        elif i % 7 == 0:  # same size but executable: a trap for size-only searches
            trap = "#!/bin/sh\necho Not this one.\n"
            write(path, trap + "#" * (1233 - len(trap)) + "\n", 0o750)
        else:
            write(path, "junk " * rng.randint(10, 400))
    # 13: setuid door
    subprocess.run(["install", "-o", "miner14", "-g", "miner13", "-m", "4750",
                    "/opt/mineshaft/door", f"{home(13)}/door"], check=True)
    # 14: environment variable
    with open(f"{home(14)}/.bashrc", "a") as f:
        f.write(f'\nexport MINESHAFT_SECRET="{nxt(14)}"\n')
    # 15: diff
    old = [word() for _ in range(500)]
    new = list(old)
    new[rng.randrange(500)] = nxt(15)
    write(f"{home(15)}/old-map.txt", "\n".join(old) + "\n")
    write(f"{home(15)}/new-map.txt", "\n".join(new) + "\n")
    # 16 and 19 are network services (services.py); 17 is a process (entrypoint.sh)
    write(f"{home(19)}/vault-notes.txt", VAULT_NOTES)
    write("/etc/mineshaft/keeper-secret", nxt(17) + "\n", 0o600)
    # 18: git history
    j = f"{home(18)}/journal"
    os.makedirs(j)
    git = lambda *a: subprocess.run(["git", "-C", j, "-c", "user.name=Old Miner",
                                     "-c", "user.email=miner@mineshaft.local", *a], check=True)
    git("init", "-q", "-b", "main")
    write(f"{j}/journal.txt", f"Day 1: Found a great tunnel.\nNote to self, the password is {nxt(18)}\n")
    git("add", ".")
    git("commit", "-q", "-m", "Start my mining journal")
    write(f"{j}/journal.txt", "Day 1: Found a great tunnel.\nDay 2: Oops. I erased the password so nobody can find it. Ha!\n")
    git("commit", "-q", "-am", "Remove the password (nobody will ever know)")
    # 20: summit
    write(f"{home(20)}/trophy.txt", TROPHY)

    for n in range(LAST + 1):
        gid = grp.getgrnam(f"miner{n}").gr_gid
        for dirpath, dirnames, filenames in os.walk(home(n)):
            for p in [dirpath] + [os.path.join(dirpath, f) for f in filenames]:
                if p == f"{home(13)}/door":
                    continue
                os.chown(p, 0, gid)
                executable = os.path.isdir(p) or os.stat(p).st_mode & 0o100
                os.chmod(p, 0o750 if executable else 0o640)

    os.chmod("/tmp", 0o1733)  # can make folders in /tmp, but can't list other people's


VAULT_NOTES = """VAULT GUARD NOTES (found taped to the wall)

The guard listens on port 30019. When you connect, it says one line:
    HELLO MINER. 20 QUESTIONS. 1 SECOND EACH.
Then, 20 times, it sends a line like:
    WHAT IS 4821 + 9932?
and waits for you to send back just the answer, like:
    14753
and a newline. If you are right it says  CORRECT  and asks the next one.
If you are wrong or too slow it says  BOOM  and hangs up.
After 20 correct answers it tells you the password.

In Python, these will help:
    import socket
    s = socket.create_connection(("localhost", 30019))
    f = s.makefile("rw")
    line = f.readline()          # read one line from the guard
    f.write("123\\n"); f.flush()   # send one line to the guard
"""

TROPHY = r"""
        ___________
       '._==_==_=_.'
       .-\:      /-.
      | (|:.     |) |
       '-|:.     |-'
         \::.    /
          '::. .'
            ) (
          _.' '._
         `"""""""`

 YOU REACHED THE BOTTOM OF THE MINESHAFT!

 You used: cat, cd, ls, quotes, hidden files, file, find, grep, sort,
 uniq, pipes, head, tail, base64, tr, tar, zcat, mktemp, --help, setuid
 programs, environment variables, diff, nc, ps, git history, and you
 wrote a program that talks over a network.

 That is a LOT of real computer skill. Go show your guide this trophy.
"""


def print_goals():
    print("# Mineshaft level goals\n")
    print("<!-- Generated by `python3 build_levels.py --print-goals`. Edit GOALS in build_levels.py, not this file. -->\n")
    print("Log in to level N with `ssh minerN@localhost -p 2220`. Each level's goal is also in `GOAL.txt` in that level's home folder.\n")
    for n, text in GOALS.items():
        print(f"## Level {n}\n\n```text\n{text}\n```\n")


if __name__ == "__main__":
    if "--print-goals" in sys.argv:
        print_goals()
    else:
        build()
