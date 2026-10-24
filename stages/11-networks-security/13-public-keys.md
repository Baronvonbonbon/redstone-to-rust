# Lesson 11.13: Padlocks and Signatures

**Time:** 2–3 sessions of 45 min · **You need:** a terminal; the Sandbox;
`~/lab/net/python`; a small padlock (or a picture of one); paper; the
internet for step 8 (optional) · **New words:** public key, private key,
signature, verify, RSA, certificate, authenticity

## Goal *(read this to the learner)*

> Last lesson ended with a sneaky spy in the middle. To beat them, you
> need something only you can make, that anyone can check: a
> signature. Today you'll build a tiny public-key lock out of two
> primes, make your own real key, log in to the Sandbox with it instead
> of a password, and sign the Creeper Club's rules so nobody can change
> them without being caught.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] The Sandbox switched on, and the learner's Sandbox passphrase
      (Lesson 11.11) to hand.
- [ ] Check whether the learner already has a key: `ls ~/.ssh` in their
      account. If `id_ed25519` is there, skip the `ssh-keygen` part of
      step 4.

## Warm-up (5 min)

"What could the spy in the middle do?" *(Swap the paint cups, so Alex
and Steve each shared a secret with the spy, not each other.)* "In
Lesson 11.10, what was the problem with `fingerprints.txt`?" *(A sneaky
person could change it too.)* **Say:** "Same problem: how do you know
who something really came from?"

## Activity

### Session 1: a lock from two primes

1. **Open padlocks.** Hold up the padlock, open. **Say:** "Imagine I
   gave out hundreds of these padlocks, all open, but kept the only key.
   Anyone could put a note in a box and click my padlock shut. Who
   could open it?" *(Only me.)* **Say:** "The open padlock is my
   **public key**: I give it to everyone. The key that opens it is my
   **private key**: I never give it to anyone." **Ask:** "Did we have to
   meet, or swap secrets first?" *(No! That's the magic.)*

2. **Signatures are the other way round.** **Say:** "Now imagine
   something only *my* key can do, that anyone with my padlock can
   check. Like a wax seal: only I have the stamp, but everyone knows what
   my seal looks like. That's a **signature**." Write both on paper:
   - Lock with the **public** key → only the private key opens it.
   - Sign with the **private** key → anyone can **verify** it with the
     public key.

3. **A tiny lock in Python.** In `~/lab/net/python`, make `rsa.py`:
   ```python
   # A tiny public-key lock, made from two primes.
   p = 5
   q = 11
   n = p * q                  # 55: everyone may know this
   turns = (p - 1) * (q - 1)  # 40: secret, because only we know p and q
   e = 3                      # everyone may know this too
   d = pow(e, -1, turns)      # 27: the private key, from Lesson 11.8's trick

   print(f"Public key: n={n}, e={e}.  Private key: d={d}")

   message = 9
   locked = pow(message, e, n)
   print(f"{message} locked with the public key is {locked}")
   print(f"{locked} unlocked with the private key is {pow(locked, d, n)}")

   signature = pow(message, d, n)
   print(f"The signature for {message} is {signature}")
   print(f"Anyone can check it with the public key: {pow(signature, e, n)}")
   ```
   `python3 rsa.py`. **They should see:**
   ```
   Public key: n=55, e=3.  Private key: d=27
   9 locked with the public key is 14
   14 unlocked with the private key is 9
   The signature for 9 is 4
   Anyone can check it with the public key: 9
   ```
   **Say:** "Locking is 'to the power of 3, on a 55 clock'. Unlocking is
   'to the power of 27'. Somehow, the 27 undoes the 3! It works because
   of how `turns` was made from the primes." Check one by hand, with a
   calculator: 9 × 9 × 9 = 729, and 729 − 13 × 55 = 729 − 715 = 14. Then:
   4 × 4 × 4 = 64, and 64 − 55 = 9: the signature checks out.

4. **Be the spy.** **Ask:** "The spy knows `n = 55` and `e = 3`. What
   do they need to work out `d`?" *(`turns`, which needs `p` and `q`.)*
   "Can they find two primes that multiply to 55?" *(5 × 11! Easy.)* Make
   `factor.py`:
   ```python
   # The spy knows n. Can they find p and q?
   n = 55
   for p in range(2, n):
       if n % p == 0:
           print(f"{n} = {p} x {n // p}")
           break
   ```
   **They should see:** `55 = 5 x 11`. **Say:** "Remember the Prime
   Hunters in Lesson 3.6? Multiplying two primes is easy. Finding them
   again, from the answer, is very hard when they're huge. Real keys use
   primes with over 300 digits each. This lock is called **RSA**, after
   the three people who published it: Rivest, Shamir and Adleman."
   Commit.

### Session 2: your own real key

5. **Make a key.** On the family computer:
   ```
   ssh-keygen -t ed25519
   ```
   Press Enter to accept the place to save it. For the passphrase, roll
   a new dice passphrase (Lesson 11.11) and type it twice; tell the
   guide. **They should see** something like:
   ```
   Generating public/private ed25519 key pair.
   Enter file in which to save the key (/home/sam/.ssh/id_ed25519):
   Created directory '/home/sam/.ssh'.
   Enter passphrase (empty for no passphrase):
   Enter same passphrase again:
   Your identification has been saved in /home/sam/.ssh/id_ed25519
   Your public key has been saved in /home/sam/.ssh/id_ed25519.pub
   The key fingerprint is:
   SHA256:bQ7BTgqW/yOOIrCwDJVEt+fnvl/Ozayp9aFMjI04xA8 sam@pop-os
   The key's randomart image is:
   +--[ED25519 256]--+
   | .. .            |
   ...
   ```
   Then:
   ```
   ls -l ~/.ssh
   cat ~/.ssh/id_ed25519.pub
   ```
   **They should see:**
   ```
   -rw------- 1 sam sam 464 Oct 24 16:02 id_ed25519
   -rw-r--r-- 1 sam sam  98 Oct 24 16:02 id_ed25519.pub
   ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEqL/9qFADOhMhzzSBRK6hU53JFYsgqqq0Zc2kSFg3sV sam@pop-os
   ```
   **Ask:** "Which file is the open padlock, and which is the key?"
   *(`.pub` is public: everyone may read it, `-rw-r--r--`. The other is
   private: only you, `-rw-------`, and it's locked with your
   passphrase too.)* **Say:** "The private file must never leave this
   computer. Never send it, never commit it." *(The key is an
   **Ed25519** key: a modern cousin of RSA, made with curves instead of
   primes, and much shorter.)*

6. **Log in with the key.** Give the Sandbox your open padlock:
   ```
   ssh-copy-id -p 2222 LEARNER@localhost
   ```
   It asks for the Sandbox password one last time. **They should see**,
   at the end:
   ```
   Number of key(s) added: 1

   Now try logging into the machine, with:   "ssh -p 2222 'sam@localhost'"
   and check to make sure that only the key(s) you wanted were added.
   ```
   Now `ssh LEARNER@localhost -p 2222`. **They should see:**
   `Enter passphrase for key '/home/sam/.ssh/id_ed25519':` instead of the
   Sandbox's password. Inside, `cat ~/.ssh/authorized_keys`: **they
   should see** the same `ssh-ed25519 AAAA...` line. **Say:** "The
   Sandbox keeps a list of padlocks it trusts. When you log in, it sends
   a random challenge, and your computer signs it with your private key.
   The Sandbox checks the signature with the padlock. Your private key
   never travels at all."

7. **The Sandbox's own key.** **Ask:** "The first time you ever used
   `ssh` to the Sandbox, in Stage 5, it asked 'Are you sure you want to
   continue connecting?' and showed a fingerprint. What was that about?"
   **Say:** "The Sandbox has a key too. That question was: 'I've never
   seen this computer's padlock before. Is it really the Sandbox, or a
   spy in the middle?'" In the Sandbox:
   ```
   ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
   ```
   **They should see** something like:
   ```
   256 SHA256:RsR6mFhq1EWkJDEpye0QAms9ME1zBc1PPhnasHzyhg4 root@buildkitsandbox (ED25519)
   ```
   Back on the family computer, `ssh-keygen -lF '[localhost]:2222'` shows
   the fingerprint that was remembered in Stage 5, on its last line:
   ```
   # Host [localhost]:2222 found: line 1
   [localhost]:2222 ED25519 SHA256:RsR6mFhq1EWkJDEpye0QAms9ME1zBc1PPhnasHzyhg4
   ```
   **Ask:** "Do they match?" *(They should! If the Sandbox was rebuilt, it won't, and
   `ssh` gives the big `REMOTE HOST IDENTIFICATION HAS CHANGED` warning:
   that's `ssh` checking for a spy in the middle.)*

### Session 3: signing things

8. **Sign the club rules.** On the family computer:
   ```
   mkdir ~/lab/net/signed
   cd ~/lab/net/signed
   echo "No exploding indoors." > rules.txt
   ssh-keygen -Y sign -f ~/.ssh/id_ed25519 -n file rules.txt
   ```
   Type the key's passphrase. **They should see:**
   ```
   Signing file rules.txt
   Write signature to rules.txt.sig
   ```
   `cat rules.txt.sig`: a short block between `-----BEGIN SSH
   SIGNATURE-----` and `-----END SSH SIGNATURE-----`. **Say:** "That's
   made from a fingerprint of the file, signed with your private key."
   Now make a list of padlocks you trust, which is just you, for now:
   ```
   echo "LEARNER $(cat ~/.ssh/id_ed25519.pub)" > signers.txt
   ssh-keygen -Y verify -f signers.txt -I LEARNER -n file -s rules.txt.sig < rules.txt
   ```
   **They should see:**
   ```
   Good "file" signature for sam with ED25519 key SHA256:ZMCIiOkZRgdhuZw+fBHfLC63EnJLeRKXPs/qBWiZmec
   ```
   Now the guide is sneaky again: `echo "No exploding indoors. Except
   Tuesdays." > rules.txt`. The learner verifies again. **They should
   see:**
   ```
   Signature verification failed: incorrect signature
   Could not verify signature.
   ```
   **Ask:** "Could the sneaky guide make a new signature, to match?"
   *(Not without the learner's private key and its passphrase.)*
   **Say:** "That's the answer to Lesson 11.10's question. A fingerprint
   says 'this file wasn't changed'; a signature says 'and it really came
   from me'. Pop!_OS and Ubuntu sign their package lists like this, so
   `apt` knows every package really came from them." Commit, including
   `rules.txt.sig` and `signers.txt` (they're public), but never
   anything from `~/.ssh` except `.pub` files.

9. **Signed websites** *(needs the internet)*. **Say:** "When you visit
   Wikipedia, how does Firefox know it isn't a fake, like the one we made
   with `/etc/hosts`?"
   ```
   openssl s_client -connect wikipedia.org:443 -servername wikipedia.org </dev/null 2>/dev/null | openssl x509 -noout -subject -issuer -dates
   ```
   **They should see** something like:
   ```
   subject=CN = *.wikipedia.org
   issuer=C = US, O = Let's Encrypt, CN = YE2
   notBefore=Oct  4 18:34:51 2026 GMT
   notAfter=Jan  2 18:34:50 2027 GMT
   ```
   **Say:** "This is a **certificate**: Wikipedia's public key, plus a
   signature from Let's Encrypt saying, 'We checked: this padlock
   really belongs to `wikipedia.org`.' And Firefox already trusts Let's
   Encrypt's padlock, because a list of trusted padlocks came with it."
   In Firefox, on `https://www.wikipedia.org`, click the padlock, then
   **Connection secure** → **More information** → **View Certificate**:
   the same names and dates. The list of trusted padlocks on this
   computer is in `/etc/ssl/certs` (`ls /etc/ssl/certs | wc -l`).

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `ValueError: base is not invertible for the given modulus` | `e` shares a factor with `turns` | Use `e = 3` with `p = 5, q = 11`, or pick another `e` with no common factor (Lesson 11.8). |
| `/home/sam/.ssh/id_ed25519 already exists. Overwrite (y/n)?` | There's a key already | Type `n`, and use the one there. Overwriting would lock you out of anywhere it's used. |
| `ssh-copy-id: ERROR: No identities found` | No key yet | Do step 5 first. |
| Still asked for the Sandbox password after `ssh-copy-id` | The key wasn't added, or the Sandbox was reset (which forgets it) | Run `ssh-copy-id` again. |
| `Load key "/home/sam/.ssh/id_ed25519": incorrect passphrase supplied to decrypt private key` | Wrong key passphrase | Try again; if it's forgotten, make a new key (delete both files in `~/.ssh` called `id_ed25519*`, with the guide). |
| `Could not verify signature.` on the unchanged file | `signers.txt` has a different name from the one after `-I` | Use the same name in both places. |
| `openssl ... connect: Network is unreachable` | Offline | Step 9 needs the internet; it's optional. |

## Talk about it

- What's the difference between a public key and a private key? Which
  do you give away?
- Locking and signing: which key does each one use?
- Why is the tiny RSA lock easy to break, and a real one not?
- What did `ssh`'s "Are you sure?" question protect you from?
- What does a certificate prove? Who signs it?

## Challenge *(if there's time, or for next time)*

- Make a bigger lock: `p = 61`, `q = 53`, `e = 17`. What's `d`? Lock
  and unlock a letter, using `ord` and `chr` (Stage 4).
  *(`n = 3233`, `d = 2753`.)*
- Ask the guide to make a key and sign a note for you. Add the guide's
  `.pub` line to `signers.txt`, with the guide's name, and verify it.
- `ssh-keygen -lvf ~/.ssh/id_ed25519.pub` draws the randomart picture
  again. Why would a picture of a fingerprint be useful? *(People are
  better at noticing a different picture than a different string of
  letters.)*

## Checkpoint

The learner can, without help:
- [ ] Explain public and private keys with the padlock, and signing
      with the seal
- [ ] Run `rsa.py`, and explain why factoring `n` breaks it
- [ ] Make a key, and log in to the Sandbox with it
- [ ] Sign a file and verify it, and explain what a failed check means
- [ ] Explain what `ssh`'s first-connection question is checking

## Lab notebook

Draw the padlock (public) and its key (private), and which one locks,
unlocks, signs and verifies. Copy the output of `rsa.py`. Write which
files in `~/.ssh` are secret. Commit. Add *public key*, *private key*,
*signature*, *verify*, *RSA* and *certificate* to `dictionary.md`.

## Guide's background *(optional reading)*

**RSA** (1977) works because `pow(pow(m, e, n), d, n) == m` whenever
`e × d` leaves a remainder of 1 when divided by `(p − 1) × (q − 1)`
(Euler's theorem). Anyone can find `d` from `e` once they know `p` and
`q`, so the security rests on factoring `n` being infeasible; real RSA
keys have `n` of 2048 bits or more, and real RSA always adds random
padding, because the raw version in `rsa.py` leaks patterns. Signing in
practice signs a hash of the message (Lesson 11.10), not the message.

**Ed25519**, which `ssh-keygen` used here, is a signature scheme on an
elliptic curve; it's fast, has short keys, and is the default for new
`ssh` keys. During an `ssh` login with a key, the server never sees the
private key: the client signs data from that session's key exchange,
which also ties the login to that connection, so a spy in the middle
can't reuse it. `ssh-keygen -Y sign` makes the same kind of signature
for files; git can sign commits with it too (`git config gpg.format
ssh`).

**Certificates** (X.509) bind a public key to a name, signed by a
**certificate authority**. Browsers and operating systems ship a list of
trusted authorities (`/etc/ssl/certs` on Pop!_OS, from the
`ca-certificates` package). Let's Encrypt, a non-profit, issues free
certificates valid for 90 days or less, which is why the dates in step
9 are close together. A certificate proves the site's name, not that the
site is good: phishing sites (Lesson 11.11) can have padlocks too.
*Computer Networks: A Systems Approach*, Sections 8.2–8.5, covers all
of this, and the course's offline library has the OpenSSH manual pages
(`man ssh-keygen`).
