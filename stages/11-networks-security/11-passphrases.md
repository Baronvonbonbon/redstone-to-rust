# Lesson 11.11: Dice Passphrases

**Time:** 1–2 sessions of 45 min · **You need:** a terminal; the Sandbox;
three dice (or one, rolled three times); paper; `~/lab/net/words.txt`
(from `give-lab net`) · **New words:** passphrase, possibilities,
random, password manager, phishing, two-factor

## Goal *(read this to the learner)*

> What makes a password strong? Not funny symbols, it turns out, but
> how many possibilities there are, and whether it was chosen by
> chance. Today you'll count possibilities, roll dice to make a
> passphrase that's both strong and easy to remember, and give the
> Sandbox a new one.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] `~/lab/net/words.txt` is there (`./scripts/give-lab.sh LEARNER
      net`, see [the net lab](../../labs/net/README.md)). It's 216 words,
      one for every roll of three dice.
- [ ] Decide what the family rule is for writing passwords down. A good
      one: the learner tells the guide new passwords, and the guide
      keeps them somewhere safe (a notebook in a drawer, or a password
      manager, see Guide's background).
- [ ] The Sandbox switched on.

## Warm-up (5 min)

"In Lesson 11.9, why was a Caesar cipher easy to crack, and the keyword
cipher harder?" *(26 keys can all be tried; a long keyword has far more
possibilities. But a keyword from a list of Minecraft words was found
fast, because people choose guessable words.)* "So what makes a
password good?" Write the learner's ideas down.

## Activity

1. **Counting possibilities.** On paper. **Ask:** "How many 1-digit
   codes are there?" *(10: 0 to 9.)* "2 digits?" *(100: 00 to 99.)*
   "4 digits, like a bike lock?" *(10,000.)* **Say:** "Each extra digit
   multiplies by 10. That's a **power** (Stage 4): 10 × 10 × 10 × 10 =
   10⁴." Now: "How many 3-letter words, if any letters are allowed?"
   *(26 × 26 × 26 = 17,576.)*

2. **Why chance matters.** **Ask:** "If I let you choose any password,
   what would you choose?" Don't write a real one down! **Say:** "People
   choose their pet's name, their favourite mob, `password`, `123456`.
   A list of the most popular passwords would find a lot of them,
   because people's choices are easy to guess. The trick is to let
   something that can't be guessed do the choosing: dice." *(This is
   what went wrong with `OCELOT` in Lesson 11.9.)*

3. **Roll a passphrase.** Look at `~/lab/net/words.txt` together
   (`less ~/lab/net/words.txt`): **they should see** lines like
   ```
   111 acorn
   112 anvil
   113 apple
   ```
   down to `666 wizard`. **Say:** "Three dice give a number like 352.
   Find it, and that's your word." Roll three dice six times, and write
   each word down. **Ask:** "How many possible words for one roll?"
   *(6 × 6 × 6 = 216.)* "For six words?" Work it out together in
   Python:
   ```
   python3 -c 'print(f"{216 ** 6:,}")'
   ```
   **They should see:** `101,559,956,668,416`. **Say:** "A **passphrase**
   is a password made of words. Six random words: over a hundred
   million million possibilities, and easy to remember, because you can
   make a picture of it." Make up a silly picture or story for the six
   words. *(For example: an ocean of pizza, covered in moss, in the
   middle of a desert, with a ghost fish.)*

4. **How big is that?** **Ask:** "If a computer could count a billion
   numbers every second, how long to count to that?"
   ```
   python3 -c 'print(216 ** 6 / 1_000_000_000 / 60 / 60, "hours")'
   ```
   **They should see** about `28.2 hours`. **Say:** "That's for six
   words. Every extra word multiplies by 216." Try 7 *(about 254 days)*
   and 8 *(about 150 years)*. **Ask:** "Which helps more: adding one
   symbol like `!`, or adding one word?" *(A word: a symbol at the end is
   one of about 30 choices, a word is one of 216, and people usually put
   the `!` in the same place, so it hardly helps.)*

5. **A passphrase machine.** In `~/lab/net/python`, copy the word list
   in (`cp ~/lab/net/words.txt .`) and make `passphrase.py`:
   ```python
   import secrets

   # words.txt has lines like "111 acorn": three dice, then a word.
   words = []
   for line in open("words.txt"):
       dice, word = line.split()
       words.append(word)

   how_many = 6
   chosen = []
   for n in range(how_many):
       chosen.append(secrets.choice(words))
   print(" ".join(chosen))
   print(f"One of {len(words) ** how_many:,} possible passphrases")
   ```
   `python3 passphrase.py`, a few times. **They should see** something
   like:
   ```
   crystal wind crystal kayak rocket seed
   One of 101,559,956,668,416 possible passphrases
   ```
   **Ask:** "Why `secrets.choice`, not `random.choice`?" *(Lesson 11.8:
   `random` can be predicted; `secrets` uses the computer's real
   randomness.)* "`crystal` came up twice. Is that bad?" *(No: the dice
   can roll the same number twice too. Every word is still a fresh,
   fair choice.)* Commit `passphrase.py`. Never commit a passphrase
   you're actually using!

6. **Give the Sandbox a passphrase.** In the Sandbox
   (`ssh LEARNER@localhost -p 2222`):
   ```
   passwd
   ```
   Type the current password, then the dice passphrase from step 3,
   twice, spaces and all. Nothing appears while typing: that's on
   purpose (Stage 5). **They should see:**
   ```
   Changing password for LEARNER.
   Current password:
   New password:
   Retype new password:
   passwd: password updated successfully
   ```
   Type `exit`, and log in again with the passphrase. Tell the guide the
   new passphrase, so it can be kept safe. (If it's forgotten,
   `./sandbox.sh reset` puts the first one back.)

7. **How computers keep passwords.** **Ask:** "When you log in, the
   computer has to check your passphrase. Does it keep a copy?"
   **Say:** "It keeps a fingerprint (Lesson 11.10), made with a
   fingerprint machine that's slow on purpose. When you log in, it
   fingerprints what you typed and compares. So even someone who stole
   the list of fingerprints from a website wouldn't have anyone's
   password, only a list of one-way fingerprints. A random passphrase
   makes sure it stays that way." That's the `/etc/shadow` story from
   Lesson 5.1.

8. **The rules.** Talk through these, and write them in the lab
   notebook:
   - **One passphrase per place.** If one website loses its list, the
     others are still safe.
   - **Only tell the guide.** Not friends, not a game, not anyone who
     messages you, even if they say they're from the game's company. A
     message or page that pretends to be someone trustworthy, to get
     your password, is called **phishing** (like fishing, with bait).
     Remember the fake Wikipedia from Lesson 11.3: a page can look
     exactly right and still be fake.
   - **Someone else's password is theirs.** The Hacker's Pledge, rule
     4: even if you find it, see it or guess it, don't use it. Tell
     them, so they can change it.
   - **Two-factor.** Many accounts can also ask for a second thing (a
     code from a phone, or a little USB key) as well as the password.
     Then a stolen password alone isn't enough.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `FileNotFoundError: ... 'words.txt'` | `words.txt` isn't in the folder `passphrase.py` runs in | `cp ~/lab/net/words.txt ~/lab/net/python/` |
| `ValueError: not enough values to unpack` | A blank or one-word line in `words.txt` | Use the original from `~/lab/net/words.txt`. |
| `passwd: Authentication token manipulation error` | The current password was wrong | Try again. If it's forgotten, the guide runs `./sandbox.sh reset`. |
| `Sorry, passwords do not match.` | The two new ones were typed differently | Run `passwd` again, slowly. |
| `Permission denied, please try again.` when logging in again | A typing slip in the passphrase | Try again; check spaces. If it's forgotten, `./sandbox.sh reset`. |

## Talk about it

- What makes a password strong? Was your warm-up list right?
- Why do dice make a better password than choosing one yourself?
- Why does adding a word help more than adding a `!`?
- Why do websites keep fingerprints of passwords, and not the passwords?
- What's phishing? What would you do if a message asked for your
  password?

## Challenge *(if there's time, or for next time)*

- Change `passphrase.py` to ask how many words to use, with `input()`.
- Make a 4-digit PIN with `secrets.randbelow(10000)`. Why does it need
  `:04` in an f-string (`f"{pin:04}"`)? *(Without it, 42 prints as `42`,
  not `0042`.)*
- How many words would you need from a list of 7776 (five dice) to beat
  eight words from this list? *(Five: 7776⁵ is bigger than 216⁸, but
  7776⁴ isn't.)*

## Checkpoint

The learner can, without help:
- [ ] Count the possibilities for a PIN and for a dice passphrase
- [ ] Explain why chance beats choosing
- [ ] Make a passphrase with dice or `passphrase.py`, and change a
      password with `passwd`
- [ ] Say the rules: one per place, only tell the guide, never use
      someone else's, and what phishing is

## Lab notebook

Write the rules from step 8. Draw a picture of a made-up passphrase
(not a real one). Write how many possibilities six and eight words
have. Commit. Add *passphrase*, *possibilities*, *phishing*, *password
manager* and *two-factor* to `dictionary.md`.

## Guide's background *(optional reading)*

This is the **Diceware** method, invented by Arnold Reinhold in 1995;
the Electronic Frontier Foundation's word lists (7776 words for five
dice, or 1296 for four) are the usual choice for real passphrases.
`words.txt` is a short, child-friendly list written for this course,
so its six-word passphrases are fine for the Sandbox and a family
computer, but for anything important use eight words from it, or six
from a full Diceware list. The strength comes entirely from the dice:
a passphrase *chosen* by a person is much weaker than the same number of
words picked at random.

Linux keeps password fingerprints in `/etc/shadow`, readable only by
root, made with a deliberately slow algorithm (on Ubuntu, **yescrypt**)
and a random **salt** mixed in, so that two people with the same
password have different fingerprints and each check takes real
computer time. Well-run websites do the same. That's why one strong,
unique passphrase per site matters: when a website's database leaks,
it's the reused and guessable passwords that get found.

A **password manager** keeps every password in one encrypted file
behind one strong passphrase. **KeePassXC** (`sudo apt install
keepassxc`) is open source, works entirely offline and needs no
account; it can also generate Diceware passphrases. For a family, a
reasonable approach is for the guide to keep the learner's passwords in
the guide's manager until the learner is older.
