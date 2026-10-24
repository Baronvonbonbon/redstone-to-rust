# Lesson 11.3: The Internet's Phone Book: DNS

**Time:** 2 sessions of 45 min · **You need:** a terminal; the Sandbox;
`~/lab/net/python`; the internet for steps 5 to 7 (optional) · **New words:**
domain name, DNS, name server, resolve, cache, `/etc/hosts`, `dig`

## Goal *(read this to the learner)*

> Computers find each other by numbers, but people remember names. Who
> turns `wikipedia.org` into `208.80.154.224`? A huge phone book,
> spread over thousands of computers, called **DNS**. Today you'll add
> names to the Sandbox's own little phone book, follow a real lookup
> from the top of the internet down, and build a pretend DNS in Python.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] The Sandbox switched on.
- [ ] Step 3 uses the learner's `sudo` in the Sandbox (they're its admin,
      from Stage 5). If they've forgotten the Sandbox password,
      `./sandbox.sh reset` sets it back to their name.

## Warm-up (5 min)

"How did a packet from the Sandbox find its way to `1.1.1.1`?" *(Hop by
hop: each router's table said where to pass it next.)* "Can you
remember the address of the house's router?" *(Probably not! That's
the problem with numbers.)*

## Activity

### Session 1: little phone books

1. **The phone book game.** **Say:** "You want to phone Steve, but you
   don't know his number. Who could you ask?" *(Someone who knows
   him.)* Act it out: you're the **name server**. The learner asks, "What's
   Steve's number?", and you answer with a made-up number. **Say:**
   "Turning a name into a number is called **resolving** it. The
   internet's phone book is **DNS**: the Domain Name System."

2. **The computer's own little book.** On the family computer:
   ```
   cat /etc/hosts
   getent hosts localhost
   ```
   **They should see** a short file, starting something like:
   ```
   127.0.0.1	localhost
   127.0.1.1	pop-os
   ```
   and then `::1   localhost` from `getent` (or `127.0.0.1 localhost`).
   **Say:** "`/etc/hosts` is the oldest phone book of all: a file of
   names and numbers, checked before anything else. `getent hosts` asks
   the computer, 'What number do *you* think this name has?'"

3. **Add a name.** In the Sandbox (`ssh LEARNER@localhost -p 2222`),
   where they're the admin:
   ```
   ping -c 1 diamond-mine
   ```
   **They should see:** `ping: diamond-mine: Name or service not known`.
   Now add it:
   ```
   sudo nano /etc/hosts
   ```
   Add a line at the end, with a Tab (or spaces) in the middle:
   ```
   127.0.0.1	diamond-mine
   ```
   Save, then:
   ```
   getent hosts diamond-mine
   ping -c 1 diamond-mine
   ```
   **They should see:**
   ```
   127.0.0.1       diamond-mine
   PING diamond-mine (127.0.0.1) 56(84) bytes of data.
   64 bytes from localhost (127.0.0.1): icmp_seq=1 ttl=64 time=0.053 ms
   ```
   **Say:** "A brand-new name, and it works. (The reply says `localhost`,
   because that's the first name in the book for `127.0.0.1`.)"

4. **Why only the admin can change it.** **Ask:** "What would happen if
   someone added the line `127.0.0.1 wikipedia.org`?" Try it, in the
   Sandbox only: add that line to `/etc/hosts`, then:
   ```
   ping -c 1 wikipedia.org
   ```
   **They should see:** `PING wikipedia.org (127.0.0.1)`. **Say:** "Every
   program on this computer now goes to the wrong place for Wikipedia.
   If a bad person could do that, they could send you to a fake
   Wikipedia that looked just like the real one. That's why it's
   `root`'s file." Now **delete that line** (and keep `diamond-mine`).
   Run `ls -l /etc/hosts` and look at the permissions (Stage 5):
   *(`-rw-r--r-- root root`: everyone can read it; only root can write.)*

### Session 2: the big phone book

5. **Ask DNS** *(needs the internet)*. On the family computer:
   ```
   dig wikipedia.org
   ```
   **They should see** a lot of lines; the important ones are:
   ```
   ;; QUESTION SECTION:
   ;wikipedia.org.			IN	A

   ;; ANSWER SECTION:
   wikipedia.org.		2	IN	A	208.80.154.224

   ;; Query time: 28 msec
   ;; SERVER: 8.8.8.8#53(8.8.8.8) (UDP)
   ```
   **Say:** "The question: what's the `A` (address) for `wikipedia.org`?
   The answer: `208.80.154.224`. `SERVER` is the name server this
   computer asked. And the small number after the name is how many
   seconds the answer may be remembered for." Run it again, and look at
   `Query time`. **Ask:** "Was it quicker the second time?" *(If it's
   now 0 or 1 msec, this computer remembered the answer: a **cache**. If
   not, the remembering is happening further along, at the server.)*
   Try `dig +short minecraft.net` for just the number.

6. **From the top.** **Say:** "Who does that server ask? Nobody knows
   every name in the world." Draw a tree on paper: a dot at the top
   (the **root**), then `org`, `net` and `com` below it, then
   `wikipedia` under `org`, then `www` under `wikipedia`. **Say:** "Names
   are read from the right. Each level only knows the level below."
   ```
   dig +trace wikipedia.org | grep -v '^;'
   ```
   **They should see** four groups of lines (a long wait is normal).
   Find these: lines for `.` with `root-servers.net` names (the 13 root
   servers, `a` to `m`); lines for `org.` with name servers that know
   about `org`; lines for `wikipedia.org.` with `ns0.wikimedia.org` and
   friends; and at the end, `wikipedia.org. ... A 208.80.154.224`.
   **Say:** "The root said 'ask the `org` servers', they said 'ask
   Wikipedia's own servers', and Wikipedia's servers knew the answer.
   Like the routers, nobody knows everything, but everyone knows who to
   ask next."

7. **`dig` doesn't read `/etc/hosts`.** In the Sandbox:
   ```
   dig +short diamond-mine
   ```
   **They should see** nothing at all. **Ask:** "But `ping` found it!
   Why?" *(`ping` asks the computer, which checks `/etc/hosts` first.
   `dig` goes straight to the DNS servers, and they've never heard of
   it.)*

8. **A pretend DNS in Python.** On the family computer, in
   `~/lab/net/python`, make `names.py`:
   ```python
   # A pretend internet's name servers. Each one only knows who to ask next,
   # except the last, which knows the address.
   servers = {
       "root": {"org": "org-server", "net": "net-server"},
       "org-server": {"wikipedia.org": "wiki-server", "gutenberg.org": "book-server"},
       "net-server": {"minecraft.net": "mojang-server"},
       "wiki-server": {"www.wikipedia.org": "208.80.154.224"},
       "book-server": {"www.gutenberg.org": "152.19.134.47"},
       "mojang-server": {"www.minecraft.net": "150.171.110.7"},
   }
   cache = {}


   def resolve(name):
       if name in cache:
           print(f"  {name} is in my cache!")
           return cache[name]
       parts = name.split(".")              # "www.wikipedia.org" -> ["www", "wikipedia", "org"]
       ask = "root"
       for n in range(len(parts) - 1, -1, -1):
           piece = ".".join(parts[n:])      # "org", then "wikipedia.org", then "www.wikipedia.org"
           answer = servers[ask].get(piece)
           if answer is None:
               print(f"  {ask} says: never heard of {piece}")
               return None
           print(f"  I ask {ask} about {piece}: it says {answer}")
           ask = answer
       cache[name] = answer
       return answer


   for name in ["www.wikipedia.org", "www.minecraft.net", "www.wikipedia.org", "www.creeper.org"]:
       print(f"Where is {name}?")
       print(f"  -> {resolve(name)}")
   ```
   `python3 names.py`. **They should see:**
   ```
   Where is www.wikipedia.org?
     I ask root about org: it says org-server
     I ask org-server about wikipedia.org: it says wiki-server
     I ask wiki-server about www.wikipedia.org: it says 208.80.154.224
     -> 208.80.154.224
   Where is www.minecraft.net?
     I ask root about net: it says net-server
     I ask net-server about minecraft.net: it says mojang-server
     I ask mojang-server about www.minecraft.net: it says 150.171.110.7
     -> 150.171.110.7
   Where is www.wikipedia.org?
     www.wikipedia.org is in my cache!
     -> 208.80.154.224
   Where is www.creeper.org?
     I ask root about org: it says org-server
     org-server says: never heard of creeper.org
     -> None
   ```
   **Ask:** "Why did the second Wikipedia need no asking?" *(The cache.)*
   "What does `range(len(parts) - 1, -1, -1)` count?" *(Backwards: 2, 1,
   0, so the pieces go from the right, like the tree.)* Commit.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `[sudo] password for ...` then `Sorry, try again.` | The wrong Sandbox password | If it's forgotten: the guide runs `./sandbox.sh reset` (it goes back to their name). |
| `ping: diamond-mine: Name or service not known` after adding it | A typing mistake in `/etc/hosts`, or the line didn't save | `cat /etc/hosts`: check the line is there, with the address first. |
| `-bash: /etc/hosts: Permission denied` | Writing to it without `sudo` | That's the point of step 4! Use `sudo nano`. |
| `dig: command not found` | The `dnsutils` package is missing | Ask the guide: `sudo apt install dnsutils`. |
| `;; communications error ... timed out` or `no servers could be reached` | Offline | Steps 5 to 7 need the internet; skip to step 8. |
| `status: NXDOMAIN` | DNS says that name doesn't exist | Check the spelling. |
| `KeyError: 'org-server'` (or another server) | A server is missing from `servers` | Check the spelling in both places. |

## Talk about it

- What does DNS do? Why don't we just use numbers?
- Why are names read from the right?
- Why is `/etc/hosts` only writable by root?
- What's a cache, and why does it make the internet faster?

## Challenge *(if there's time, or for next time)*

- Add `com` to `names.py`, with a pretend `creeper.com` and its own
  server. Look up `www.creeper.com`.
- `dig -x 208.80.154.224` asks the other way: what's the name for this
  number?
- `dig wikipedia.org MX` asks where Wikipedia's email goes. `AAAA` asks
  for the IPv6 address.

## Checkpoint

The learner can, without help:
- [ ] Explain what DNS is for, with the phone book
- [ ] Add a name to `/etc/hosts` in the Sandbox, and explain why only
      root can
- [ ] Use `dig`, and find the answer, the server and the time
- [ ] Explain the tree, from the root down, with `names.py`

## Lab notebook

Draw the name tree, with `wikipedia.org` and `minecraft.net` on it.
Write which name servers answered, at each level. Commit. Add *domain
name*, *DNS*, *name server*, *resolve*, *cache* and */etc/hosts* to
`dictionary.md`.

## Guide's background *(optional reading)*

This is *Computer Networks: A Systems Approach*, Section 9.3 ("Name
Service (DNS)"), in the offline library. When a program looks up a
name, the computer first checks `/etc/hosts`, then asks the name server
it was given (by the router, usually), which does the work of step 6
for it and caches the answers for as long as each one says. On Pop!_OS,
that first server is `systemd-resolved` on the computer itself
(`127.0.0.53` in `/etc/resolv.conf`), which keeps its own cache; on
other set-ups, `dig` may show the router's or an internet provider's
server.

Most DNS questions are a single small packet each way (UDP, port 53:
`dig` printed `(UDP)`), and they aren't encrypted, so anyone on the path
can see which names a computer looks up. The hosts-file trick in step 4
is the simplest version of **DNS spoofing**; the real internet's
defences include **DNSSEC** (signed answers, Lesson 11.13's idea) and
encrypted DNS. A family's router or DNS settings are also where
parental filters usually live, for the same reason: every name passes
through.

`dig` comes from the `dnsutils` package (installed by `install-packages.sh
--later`, and in the Stage 11 Sandbox). The `+trace` option makes `dig`
do the whole walk itself, starting at the root.
