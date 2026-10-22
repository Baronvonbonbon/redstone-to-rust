#!/usr/bin/env python3
"""The Great Underpants Heist: a command-line mystery for Stage 1.

Makes a folder of evidence. The learner solves it with cat, less, grep,
head, tail, wc and pipes, then checks their answer with ./accuse.

    python3 make_heist.py ~/heist          # new random mystery
    python3 make_heist.py ~/heist --seed 7 # the same mystery every time

The culprit is printed for the guide. It is not written anywhere the
learner can read it (./accuse only stores a hash).
"""
import argparse
import hashlib
import os
import random
import stat
import textwrap

FIRST = """Ada Barnaby Bea Cosmo Dot Eggbert Fern Gus Hattie Iggy Juno Kip Lulu
Milo Nell Ozzie Pip Quincy Rosie Sid Tilly Ubie Vera Wally Xena Yuri Zelda
Arlo Binx Clem Dex Effie Fitz Gertie Hank Ivy Jasper Kit Lars Mabel""".split()
LAST = """Wigglebottom Fluffernutter Snorkelton McNoodle Bumblesnoot Puddingpants
Ticklebum Sniffleton Wafflebottom Picklesworth Burpington Gigglesnort Noodleman
Crumplehorn Sockbottom Stinkwhistle Bogglesby Fizzwinkle Gumbleton Tootlebee""".split()
COLORS = "purple green orange silver gold pink blue rainbow".split()
PETS = "hamster goldfish lizard dog cat parrot snail tarantula rabbit none".split()
PLACES = "the library|the gym|the cafeteria|the art room|the nurse's office|the music room|the playground door|the bathrooms".split("|")
FLUFF = [
    "The floor is very shiny. Too shiny. Somebody mopped it with pudding.",
    "A poster on the wall says READING IS FUNDAMENTAL in big letters.",
    "There is a lost mitten under the radiator.",
    "The trophy case has a trophy for the 1987 spelling bee.",
    "Somebody has drawn a mustache on the picture of the old principal.",
    "A gum wrapper. Spearmint. Not a clue, just gross.",
    "The fish tank bubbles. The fish looks guilty but fish always look guilty.",
    "A crumpled lunch menu says Tuesday is Mystery Meat Day.",
    "There is a pencil sharpener full of crayon shavings.",
    "The clock on the wall is three minutes fast.",
    "A banner reads: GO FIGHTING TURNIPS!",
    "Someone left a half-eaten cheese sandwich on the bench.",
    "The window is open a crack. A pigeon is staring at you.",
    "A sign says NO RUNNING IN THE HALLS. Somebody added 'or skipping'.",
]

STORY = """\
THE GREAT UNDERPANTS HEIST
==========================

Something TERRIBLE has happened at Fuzzlewood Elementary.

Principal Pickles' prize-winning underpants (they won "Most Majestic
Underpants" at the county fair three years in a row) have been STOLEN
from the trophy case in the front hall!

The principal is too embarrassed to call the police. So it is up to
you, Detective, to find the thief using nothing but the terminal.

YOUR EVIDENCE (all in this folder):
  crime-scene.txt   notes about the trophy case. VERY long. Most of it
                    is useless. The important lines start with CLUE
  students.txt      every student, their room, their favorite glitter
                    color, and their pet
  hall-log.txt      the hall monitor's log of who walked where, and when

TOOLS THAT WILL HELP:
  cat FILE           show a whole file
  less FILE          scroll through a file (press q to quit)
  grep WORD FILE     show only the lines that contain WORD
  head / tail FILE   show the first / last lines of a file
  wc -l FILE         count the lines in a file
  A | B              send what A prints into B (a "pipe")

WHEN YOU KNOW WHO DID IT:
  ./accuse "Firstname Lastname"

STUCK? Look in the hints folder: cat hints/hint-1.txt
(Only open the next hint if you are still stuck after trying.)
"""

HINTS = [
    "Start with the crime scene. You don't need to read all of it.\n"
    "grep can find just the lines that start with CLUE:\n\n    grep CLUE crime-scene.txt\n",
    "One clue tells you a room number. Find everyone in that room:\n\n"
    "    grep \"Room 7 \" students.txt\n\n(Use YOUR room number, not 7! The space after the number stops\n"
    "Room 7 from also matching Room 17.)\n",
    "Another clue tells you a glitter color. You can grep the output of\n"
    "another grep using a pipe | like this:\n\n"
    "    grep \"Room 7 \" students.txt | grep purple\n\nNow you have your suspects!\n",
    "The last clue says to check who walked past the trophy case after\n"
    "12:30. Try:\n\n    grep \"trophy case\" hall-log.txt\n\n"
    "Or grep for each suspect's name in hall-log.txt and look at the times.\n",
    "Only one suspect walked past the trophy case AFTER 12:30.\n"
    "Accuse them with:  ./accuse \"Firstname Lastname\"\n",
]

ACCUSE = '''#!/usr/bin/env python3
import hashlib, sys
ANSWER = "{digest}"
SALT = "{salt}"
if len(sys.argv) != 2:
    print('Usage: ./accuse "Firstname Lastname"')
    sys.exit(1)
name = " ".join(sys.argv[1].split()).title()
if hashlib.sha256((SALT + name).encode()).hexdigest() == ANSWER:
    print(r"""
   _____________________
  |  CASE CLOSED!       |
  |   _______________   |
  |  |               |  |
  |  |  \\\\_______/  |  |
  |  |   |       |   |  |
  |  |   |_______|   |  |
  |  |_______________|  |
  |_____________________|
""")
    print(f"{{name}} did it! Principal Pickles' underpants are SAVED.")
    print("You are an official Terminal Detective. Tell your guide!")
else:
    print(f"{{name}} gasps: 'It wasn't me!' ...and they have a good alibi.")
    print("Check your clues again. (Spelling counts!)")
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("--seed", type=int)
    args = ap.parse_args()
    rng = random.Random(args.seed)

    names = rng.sample([f"{f} {l}" for f in FIRST for l in LAST], 150)
    room, color = rng.randint(1, 20), rng.choice(COLORS)
    suspects, others = names[:3], names[3:]
    culprit = suspects[0]

    students = []
    for n in suspects:
        students.append((n, room, color))
    for i, n in enumerate(others):
        r = room if i < 12 else rng.randint(1, 20)  # plenty of room-mates with other colors
        c = rng.choice([x for x in COLORS if x != color]) if r == room else rng.choice(COLORS)
        students.append((n, r, c))
    rng.shuffle(students)

    # Hall log: everybody wanders around; suspects pass the trophy case, but only
    # the culprit does it after lunch.
    events = []
    minute = lambda h0, h1: rng.randint(h0 * 60, h1 * 60 - 1)
    for n, _, _ in students:
        for _ in range(rng.randint(1, 4)):
            events.append((minute(8, 15), n, rng.choice(PLACES)))
    for n in rng.sample(others, 15):  # innocent trophy-case visitors, any time
        events.append((rng.choice([minute(8, 12), rng.randint(12 * 60 + 31, 15 * 60 - 1)]), n, "the trophy case"))
    for n in suspects[1:]:
        events.append((rng.randint(8 * 60, 12 * 60 + 29), n, "the trophy case"))
        events.append((rng.randint(12 * 60 + 31, 15 * 60 - 1), n, rng.choice(PLACES)))
    events.append((rng.randint(12 * 60 + 31, 15 * 60 - 1), culprit, "the trophy case"))
    events.sort()

    os.makedirs(os.path.join(args.dir, "hints"), exist_ok=True)
    w = lambda name, text: open(os.path.join(args.dir, name), "w").write(text)
    w("START-HERE.txt", STORY)
    for i, h in enumerate(HINTS, 1):
        w(f"hints/hint-{i}.txt", h)
    w("students.txt", "".join(f"{n:<26} | Room {r:<2} | glitter: {c:<7} | pet: {rng.choice(PETS)}\n"
                              for n, r, c in students))
    w("hall-log.txt", "HALL MONITOR LOG (12:30 is the end of lunch)\n" +
      "".join(f"{t // 60:02}:{t % 60:02}  {n} walked past {p}\n" for t, n, p in events))

    clues = [
        f"CLUE: There is sparkly {color} glitter all over the trophy case. The thief had {color} glitter on their shoes.",
        f"CLUE: A note on the floor says 'ROOM {room} RULEZ'. The thief must be in Room {room}.",
        "CLUE: The underpants were still there at the end of lunch (12:30). Check hall-log.txt to see "
        "who walked past the trophy case AFTER 12:30.",
    ]
    scene = [rng.choice(FLUFF) for _ in range(600)]
    for c, pos in zip(clues, sorted(rng.sample(range(50, 590), 3))):
        scene.insert(pos, c)
    w("crime-scene.txt", "CRIME SCENE NOTES: THE TROPHY CASE\n\n" + "\n".join(scene) + "\n")

    salt = "%016x" % rng.getrandbits(64)
    digest = hashlib.sha256((salt + culprit).encode()).hexdigest()
    path = os.path.join(args.dir, "accuse")
    w("accuse", ACCUSE.format(digest=digest, salt=salt))
    os.chmod(path, os.stat(path).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    print(textwrap.dedent(f"""\
        Mystery created in {args.dir}
        FOR THE GUIDE ONLY (don't show the learner!):
          culprit: {culprit}   room: {room}   glitter: {color}
          other suspects: {', '.join(suspects[1:])}"""))


if __name__ == "__main__":
    main()
