# Lesson 11.15: Walls and Doors: Firewalls and Updates

**Time:** 2 sessions of 45 min · **You need:** a terminal with two tabs;
the Sandbox (rebuilt for Stage 11, see the [stage README](README.md));
the internet for step 8 (optional) · **New words:** open port, attack
surface, firewall, rule, default deny, update, patch, CVE, least
privilege

## Goal *(read this to the learner)*

> Every program that listens on a port is a door into the computer.
> Today you'll find all the Sandbox's doors, open a new one, and then
> build a wall around the Sandbox, a firewall, that only lets in what
> you choose. You'll also lock yourself out (on purpose!), get back in,
> and find out why updates matter so much.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] The Sandbox was rebuilt for Stage 11 (`./sandbox.sh build LEARNER`,
      then `./sandbox.sh reset`). Check: in the Sandbox, `which ufw`
      prints `/usr/sbin/ufw`. If not, it's the old Sandbox.
- [ ] The learner's sticky note with the Sandbox's address (Lesson
      11.1). Below, it's `172.17.0.4`.
- [ ] Everything here happens inside the Sandbox's own firewall. If it
      gets in a muddle, `./sandbox.sh reset` puts it back (which also
      forgets the passphrase and key from Lessons 11.11 and 11.13).

## Warm-up (5 min)

"In Lesson 11.5, why did the Shouty server listen on `127.0.0.1`?" *(So
only programs on the same computer could visit.)* "In Lesson 11.14, how
did we decide what to let through?" *(Refuse anything sneaky. When in
doubt, refuse.)*

## Activity

### Session 1: doors

1. **Find the doors.** Log in to the Sandbox (`ssh LEARNER@localhost -p
   2222`), and:
   ```
   sudo ss -tlnp
   ```
   **They should see:**
   ```
   State  Recv-Q Send-Q Local Address:Port Peer Address:PortProcess
   LISTEN 0      128          0.0.0.0:22        0.0.0.0:*    users:(("sshd",pid=1,fd=3))
   LISTEN 0      128             [::]:22           [::]:*    users:(("sshd",pid=1,fd=4))
   ```
   **Say:** "`-l` means listening, and `-p` shows which program. Only
   one: `sshd`, on port 22, the door you came in by. `0.0.0.0` means
   'every address', so anyone who can reach the Sandbox can knock.
   (`[::]` is the same, for IPv6.)" **Say:** "Every **open port** is a
   way in. All of them together are called the **attack surface**: the
   fewer, the better."

2. **Open a new door.** In the Sandbox, make a little web page and serve
   it, the Stage 5 way:
   ```
   mkdir ~/site
   cd ~/site
   echo "<h1>The Sandbox welcomes you</h1>" > index.html
   python3 -m http.server 8000
   ```
   Leave it running. In a second tab, on the **family computer**:
   ```
   curl http://172.17.0.4:8000/
   ```
   **They should see:** `<h1>The Sandbox welcomes you</h1>`. **Ask:** "Who
   else could visit it?" *(Anything that can reach `172.17.0.4`: here,
   only this computer. On a real network, everyone on it.)* In a third
   tab in the Sandbox, `ss -tln` again: **they should see** a new line,
   `0.0.0.0:8000`.

3. **Doors that only open inside.** Stop the server (Ctrl+C), and start
   it again with `--bind 127.0.0.1` (like Lesson 11.7):
   ```
   python3 -m http.server --bind 127.0.0.1 8000
   ```
   From the family computer, `curl http://172.17.0.4:8000/` again. **They
   should see:**
   ```
   curl: (7) Failed to connect to 172.17.0.4 port 8000 after 0 ms: Couldn't connect to server
   ```
   **Say:** "Nobody's listening on the Sandbox's outside address, so the
   Sandbox says 'no' straight away. Listening only on `127.0.0.1` is the
   first defence: a door that isn't there can't be opened." Stop it,
   and start it the first way again (no `--bind`), ready for the wall.

### Session 2: the wall

4. **Plan the wall.** **Say:** "A **firewall** is a list of **rules**
   that decides which packets may come in. The safest plan is **default
   deny**: nothing comes in, except what's on the list." On paper, the
   learner writes the Sandbox's list. **Ask:** "What must be on it?"
   *(Port 22! Otherwise we can't log in.)*

5. **Build it.** In the Sandbox (a tab that isn't running the server):
   ```
   sudo ufw status
   sudo ufw allow 22/tcp
   sudo ufw enable
   ```
   It warns `Command may disrupt existing ssh connections. Proceed with
   operation (y|n)?`: type `y`. **They should see:**
   ```
   Status: inactive
   Rules updated
   Rules updated (v6)
   Firewall is active and enabled on system startup
   ```
   Then `sudo ufw status verbose`:
   ```
   Status: active
   Logging: on (low)
   Default: deny (incoming), allow (outgoing), deny (routed)
   New profiles: skip

   To                         Action      From
   --                         ------      ----
   22/tcp                     ALLOW IN    Anywhere
   22/tcp (v6)                ALLOW IN    Anywhere (v6)
   ```
   **Say:** "`ufw` is the 'uncomplicated firewall'. Default: deny
   incoming, allow outgoing. One door allowed: 22."

6. **Test the wall.** From the family computer:
   ```
   curl --max-time 5 http://172.17.0.4:8000/
   ```
   **They should see**, after 5 seconds:
   ```
   curl: (28) Connection timed out after 5002 milliseconds
   ```
   **Ask:** "The server is still running. Why no answer?" *(The wall
   threw the packets away.)* "Why a wait, not 'no' straight away, like
   step 3?" *(The firewall doesn't even say no. It's as if the Sandbox
   isn't there at all, which tells a stranger nothing.)* Check that `ssh`
   still works: open another tab and log in. Then let the web page
   through:
   ```
   sudo ufw allow 8000/tcp
   ```
   `curl` from the family computer works again. Then take the door away:
   `sudo ufw delete allow 8000/tcp`, and check `curl` times out. Stop the
   server.

7. **Lock yourself out.** **Say:** "Now the mistake every system admin
   makes once." Keep this tab open, and in it:
   ```
   sudo ufw delete allow 22/tcp
   ```
   In a new tab on the family computer, try to log in to the Sandbox.
   **They should see** nothing at all: no password question, just
   waiting. (After about two minutes, `ssh` gives up with
   `kex_exchange_identification: read: Connection reset by peer`. Ctrl+C
   is quicker.) **Ask:** "But the first tab still
   works. Why?" *(A firewall lets a conversation that's already going
   carry on; it only stops new ones.)* Fix it from the tab that's still
   in: `sudo ufw allow 22/tcp`, and log in from the new tab. **Say:**
   "On a real server across the world, with no tab left open, you'd be
   stuck outside your own computer. That's why you allow `ssh` *first*,
   and test from a second window before you close the first." Turn the
   wall off for now, so later lessons aren't confused: `sudo ufw
   disable`.

8. **Updates.** **Ask:** "In Lesson 11.4, `tcpdump` saw the Sandbox say
   `SSH-2.0-OpenSSH_9.6p1 Ubuntu-3ubuntu13.20`. What's the `13.20`?" In
   the Sandbox:
   ```
   zcat /usr/share/doc/openssh-server/changelog.Debian.gz | head -4
   zcat /usr/share/doc/openssh-server/changelog.Debian.gz | grep -c "SECURITY UPDATE"
   ```
   **They should see** something like this (a newer Sandbox has a
   higher number, and more fixes):
   ```
   openssh (1:9.6p1-3ubuntu13.20) noble-security; urgency=medium

     * SECURITY UPDATE: sftp directory traversal
   33
   ```
   **Say:** "Look: 'directory traversal', the same kind of bug as your
   web server's in Lesson 11.14, found in a real program and fixed. Each
   fix is called a **patch**, and each publicly known bug gets a number,
   a **CVE**. This one program's changelog lists 33 security fixes,
   almost all since this version of Ubuntu came out in 2024. An
   **update** is how the fixes reach you." *(Needs the internet:)* `sudo apt update`, then `apt list
   --upgradable`, to see which of the Sandbox's programs have fixes
   waiting. **Say:** "Most attacks use bugs that already have a fix,
   on computers that haven't installed it yet. Updating is the single
   best thing anyone can do."

9. **Least privilege.** **Ask:** "Which user did the Diamond Vault run
   as?" *(The learner's own, not root.)* "Why does that matter, if
   someone found a bug in it?" *(They'd only get the learner's powers,
   not root's.)* **Say:** "Give every program only the powers it needs:
   that's **least privilege**. It's why Linux has all those accounts in
   `/etc/passwd` for programs (Lesson 5.1), and why you use `sudo` only
   when you must."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `sudo: ufw: command not found` | It's the old Sandbox | The guide rebuilds it (Before the lesson). |
| `ERROR: problem running ufw-init`, then lines ending `Permission denied (you must be root)`, even with `sudo` | The Sandbox was started without permission to change its firewall | The guide runs `./sandbox.sh reset` (the new `sandbox.sh` adds it). |
| `OSError: [Errno 98] Address already in use` | The web server is already running in another tab | Use that one, or stop it first. |
| `ssh` to the Sandbox just waits, with no password question | The firewall is blocking port 22 | From a tab that's still logged in: `sudo ufw allow 22/tcp`. |
| Locked out, and no tab left open | Port 22 was removed with nobody still logged in | The guide runs `./sandbox.sh reset`. |
| `curl` from the family computer works even with the wall up | `8000/tcp` is still allowed | `sudo ufw status numbered`, then `sudo ufw delete NUMBER`. |
| `Temporary failure resolving` on `apt update` | Offline | Step 8's `apt` part needs the internet; the changelog part doesn't. |

## Talk about it

- What's an open port? How do you find them all?
- What's the difference between "nobody listening" and "a firewall in
  the way", from outside?
- Why must `ssh` be allowed before the firewall is switched on?
- Why do updates matter so much?
- What does least privilege mean? Where have you seen it?

## Challenge *(if there's time, or for next time)*

- `sudo ufw allow from 172.17.0.1 to any port 8000 proto tcp` lets only
  the family computer in. Test it.
- Find out which ports are open on the *family computer*, with `ss
  -tln`. For each one, can you find out which program it is? (Ask the
  guide to run `sudo ss -tlnp`.)
- In the Sandbox, `zcat /usr/share/doc/openssh-server/changelog.Debian.gz
  | grep "SECURITY UPDATE" | sort | uniq -c | sort -rn | head`: which
  kinds of bug come up most?

## Checkpoint

The learner can, without help:
- [ ] List a computer's open ports with `ss -tln`, and explain the
      attack surface
- [ ] Set up `ufw` with default deny, allowing `ssh` first
- [ ] Explain the difference between refused and timed out
- [ ] Explain why updates matter, with the changelog
- [ ] Explain least privilege with an example

## Lab notebook

Draw the Sandbox as a house: doors for each port, a wall around it,
and a gate for 22. Write the firewall rules. Write the mistake from
step 7 and how to avoid it. Commit. Add *open port*, *attack surface*,
*firewall*, *default deny*, *patch*, *CVE* and *least privilege* to
`dictionary.md`.

## Guide's background *(optional reading)*

`ufw` is a friendly front end for the Linux kernel's packet filter
(netfilter, through `iptables` or `nftables`). Inside a container, it
changes only the container's own network rules; `sandbox.sh` gives the
container the `NET_ADMIN` capability for exactly this, which doesn't
affect the family computer. The "conversation carries on" behaviour in
step 7 is **connection tracking**: `ufw`'s rules allow packets belonging
to connections that were already established.

**The family computer.** Pop!_OS doesn't turn a firewall on by
default; with no programs listening on outside addresses, there's little
for one to do, but it's a reasonable extra layer, especially on laptops
that join other networks: `sudo apt install ufw`, then `sudo ufw enable`
(desktop use doesn't need any `allow` rules). If you do, note that a
firewall on the family computer can stop the Sandbox from reaching
servers on it, which this stage doesn't need. Keep Pop!_OS updated
through the Pop!_Shop or `sudo apt update && sudo apt full-upgrade`.

**CVE** (Common Vulnerabilities and Exposures) numbers are how the
world tracks publicly known security bugs. Ubuntu's changelogs list
which CVEs each update fixes, and `/usr/share/doc/PACKAGE/` holds them
for every installed package. *Computer Networks: A Systems Approach*,
Section 8.6, covers firewalls.
