# Lesson 11.4: Ports, Handshakes and Spying on Yourself

**Time:** 2–3 sessions of 45 min · **You need:** a terminal with three
tabs; the Sandbox; a toy telephone (or two cups) for the act-out ·
**New words:** port, TCP, connection, handshake, SYN, ACK, listen,
`nc`, `ss`, `tcpdump`, encryption

## Goal *(read this to the learner)*

> An address gets a packet to the right computer. But which program on
> that computer should get it? That's what **ports** are for: numbered
> doors. Today you'll open a door on the Sandbox, chat through it from
> the family computer, and then watch your own packets fly past with a
> packet-sniffing tool. You'll see your chat in plain words, and find
> out why `ssh` doesn't let anyone do that.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] The Sandbox switched on. The learner needs its address (the
      sticky note from Lesson 11.1).
- [ ] `tcpdump` is the most powerful tool in the stage: it shows every
      packet. The learner uses it **only inside the Sandbox**, where
      they're the admin and the only traffic is their own. Read the
      Hacker's Pledge together before step 6.

## Warm-up (5 min)

"What's the Sandbox's IP address?" *(From the sticky note.)* "In Stage
5, you served a web page and talked to it with `nc`. What number came
after the colon in `127.0.0.1:8000`?" *(8000: a port.)*

## Activity

### Session 1: doors and conversations

1. **Doors.** **Say:** "An IP address is like a block of flats. A **port**
   is the flat number: one of 65,536 doors, numbered 0 to 65535. Each
   program that wants visitors **listens** at a door." Some famous ones:

   | Port | Who listens there |
   |---|---|
   | 22 | `ssh` |
   | 53 | DNS |
   | 80 | web pages (HTTP) |
   | 443 | secure web pages (HTTPS) |

   **Ask:** "Why 65,536?" *(A port number is 2 bytes: 2¹⁶ = 65,536.)*

2. **Which doors are open?** In the Sandbox (`ssh LEARNER@localhost -p
   2222`):
   ```
   ss -tln
   ```
   **They should see:**
   ```
   State  Recv-Q Send-Q Local Address:Port Peer Address:PortProcess
   LISTEN 0      128          0.0.0.0:22        0.0.0.0:*
   LISTEN 0      128             [::]:22           [::]:*
   ```
   **Say:** "`ss` shows sockets: the kernel's ends of network
   conversations. `-t` means TCP, `-l` means listening, `-n` means show
   numbers, not names. Only one door is open: 22, where `ssh` is
   listening. That's how you got in! `0.0.0.0` means 'on every
   address'."

3. **The handshake.** Act it out with the toy phone. **Say:** "Before
   sending anything, the two computers check they can hear each other.
   It takes three messages:"
   - Learner: "Hello, can you hear me?" (**SYN**: synchronize)
   - Guide: "Yes, I hear you! Can you hear me?" (**SYN-ACK**:
     acknowledge, and synchronize back)
   - Learner: "Yes!" (**ACK**)

   **Say:** "That's the **TCP handshake**. TCP is the numbered-cards
   layer from Lesson 11.1. After the handshake, the two have a
   **connection**, and every packet gets an ACK back, so nothing lost
   goes unnoticed."

4. **A chat.** Two tabs. In the **Sandbox** tab, open door 7000:
   ```
   nc -l 7000
   ```
   It waits. In a **family computer** tab, knock on it, with the
   Sandbox's address:
   ```
   nc 172.17.0.4 7000
   ```
   Now type `hello sandbox` and Enter in the family computer's tab. **They
   should see** it appear in the Sandbox's tab. Type back from the
   Sandbox. **Say:** "Two programs on two computers, talking through
   door 7000. `nc` (netcat) just sends whatever you type." Open a third
   tab, log in to the Sandbox again, and look while the chat is going:
   ```
   ss -tn
   ```
   **They should see:**
   ```
   State Recv-Q Send-Q Local Address:Port Peer Address:Port Process
   ESTAB 0      0         172.17.0.4:7000   172.17.0.1:49042
   ```
   **Say:** "`ESTAB` is established: a connection. Its two ends are
   `172.17.0.4:7000` and `172.17.0.1:49042`. The family computer's end
   got a random door number of its own, so the answers know where to
   go." Press Ctrl+C in either chat tab to hang up.

5. **A door nobody's at.** From the family computer:
   ```
   nc 172.17.0.4 7001
   ```
   **They should see:**
   ```
   nc: connect to 172.17.0.4 port 7001 (tcp) failed: Connection refused
   ```
   **Say:** "The Sandbox's kernel answered straight away: 'nobody lives
   there'."

### Session 2: watching the packets

6. **The Pledge.** **Say:** "Next is a tool that shows every packet going
   in and out of a computer. On a shared network, it could show other
   people's. So we only use it on the Sandbox, which is ours, where the
   only packets are our own." Re-read the Pledge's first rule.

7. **Watch a chat.** Three tabs: two logged in to the Sandbox, one on the
   family computer. In Sandbox tab 1:
   ```
   sudo tcpdump -i eth0 -n port 7000
   ```
   It says `listening on eth0` and waits. In Sandbox tab 2: `nc -l
   7000`. On the family computer: `nc -N 172.17.0.4 7000`, then type
   `hello sandbox`, Enter, `creepers are green`, Enter, and Ctrl+D. (`-N`
   tells `nc` to hang up politely when you press Ctrl+D.) Ctrl+C in tab 1 to stop `tcpdump`. **They should
   see** something like (trimmed, without the `options [...]` parts):
   ```
   13:32:50.285079 IP 172.17.0.1.54110 > 172.17.0.4.7000: Flags [S], seq 3552230094, win 64240, length 0
   13:32:50.285107 IP 172.17.0.4.7000 > 172.17.0.1.54110: Flags [S.], seq 3361746086, ack 3552230095, win 65160, length 0
   13:32:50.285146 IP 172.17.0.1.54110 > 172.17.0.4.7000: Flags [.], ack 1, win 502, length 0
   13:32:50.285239 IP 172.17.0.1.54110 > 172.17.0.4.7000: Flags [P.], seq 1:15, ack 1, win 502, length 14
   13:32:50.285250 IP 172.17.0.4.7000 > 172.17.0.1.54110: Flags [.], ack 15, win 509, length 0
   13:32:51.284232 IP 172.17.0.1.54110 > 172.17.0.4.7000: Flags [P.], seq 15:34, ack 1, win 502, length 19
   13:32:51.284256 IP 172.17.0.4.7000 > 172.17.0.1.54110: Flags [.], ack 34, win 509, length 0
   13:32:51.284424 IP 172.17.0.1.54110 > 172.17.0.4.7000: Flags [F.], seq 34, ack 1, win 502, length 0
   13:32:51.284494 IP 172.17.0.4.7000 > 172.17.0.1.54110: Flags [F.], seq 1, ack 35, win 509, length 0
   13:32:51.284539 IP 172.17.0.1.54110 > 172.17.0.4.7000: Flags [.], ack 2, win 502, length 0
   ```
   Read it together, line by line:
   - "The first three are the handshake: `[S]` is SYN, `[S.]` is
     SYN-ACK (the dot means ACK), and `[.]` is the last ACK. Just like
     the phone!"
   - "`[P.]` with `length 14` is our first message. **Ask:** How many
     letters is `hello sandbox`?" *(13, plus the Enter: 14.)* "Then the
     Sandbox ACKs it: `ack 15` means 'I've got everything up to 15'."
   - "`length 19` is `creepers are green` and its Enter."
   - "`[F.]` is FIN: 'I've finished.' Both sides say it, and that's the
     goodbye."

8. **Read the words.** Do it again, with `-A` (show the packets' insides
   as letters):
   ```
   sudo tcpdump -i eth0 -n -A port 7000
   ```
   **They should see**, under the two `[P.]` lines, among some
   gibberish:
   ```
   .D:b~p..hello sandbox
   ```
   and `creepers are green`. **Ask:** "Who else could read that?"
   *(Every computer and router the packets pass through.)* "What if you
   had typed a password?" *(They could read that too!)*

9. **What `ssh` looks like.** In Sandbox tab 1, save the packets to a
   file instead of the screen:
   ```
   sudo tcpdump -i eth0 -n -A port 22 > ssh.txt
   ```
   On the family computer, log in to the Sandbox again in a new tab,
   type the password, then `echo creepers are green`, then `exit`. Back
   in tab 1, Ctrl+C, then look for the words:
   ```
   grep creepers ssh.txt
   grep -a SSH-2 ssh.txt
   ```
   **They should see:** nothing at all for `creepers`, and a couple of
   lines with `SSH-2.0-OpenSSH_9.6p1 Ubuntu-3ubuntu13.20`. **Say:** "The
   only plain words are the 'hello, I speak SSH version 2' at the
   start. After that, everything, even your password, was scrambled
   with a secret key that only the two computers know. That's
   **encryption**, and it's the second half of this stage." Look at
   `less ssh.txt` for a moment to see the gibberish. Then `rm ssh.txt`.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `nc: connect to 172.17.0.4 port 7000 (tcp) failed: Connection refused` | Nobody's listening at that door yet | Start `nc -l 7000` in the Sandbox first. |
| `tcpdump: eth0: You don't have permission to perform this capture on that device` | `sudo` is missing | `sudo tcpdump ...`. |
| `tcpdump: command not found` or `sudo: tcpdump: command not found` | An old Sandbox | The guide rebuilds it (the Stage 11 README). |
| `tcpdump` shows nothing | The chat isn't using port 7000, or it's using the wrong address | Check both `nc` commands. |
| `tcpdump` scrolls for ever on port 22 | It's showing its own `ssh` output, which makes more packets, which it shows... | Ctrl+C. Step 9 saves to a file to stop that. |
| `nc` doesn't end after Ctrl+D, and there's no `[F.]` | `-N` is missing | Ctrl+C, and use `nc -N` next time. |
| Messages go to the wrong chat | An old `nc -l 7000` is still running in another tab | Ctrl+C every `nc`, and start again. |

## Talk about it

- What's a port? Why does a computer need them?
- What are the three messages of the handshake?
- What did `tcpdump -A` show, and why is that worrying?
- Why couldn't you find your words in the `ssh` packets?

## Challenge *(if there's time, or for next time)*

- `nc -u -l 7000` and `nc -u 172.17.0.4 7000` chat with **UDP** instead.
  Watch it with `tcpdump`. Is there a handshake? *(No: UDP just sends
  each packet, with no ACKs. Faster, but nothing is resent.)*
- Watch a `ping` with `sudo tcpdump -i eth0 -n icmp`.
- In the Sandbox, `sudo tcpdump -i eth0 -n port 53` while running `dig
  minecraft.net` in another Sandbox tab (needs the internet). Can you
  see the name you looked up? *(Yes: DNS isn't encrypted.)*

## Checkpoint

The learner can, without help:
- [ ] Explain ports, and find listening ones with `ss -tln`
- [ ] Act out the TCP handshake, and find it in `tcpdump`'s output
- [ ] Chat between the Sandbox and the family computer with `nc`
- [ ] Explain what `-A` showed, and why `ssh` looked different

## Lab notebook

Draw the handshake as three arrows between two computers. Copy the
ten `tcpdump` lines' flags (`[S]`, `[S.]`, ...) with what each one
means. Write the Pledge rule that goes with `tcpdump`. Add *port*,
*TCP*, *connection*, *handshake*, *SYN*, *ACK*, *listen* and
*encryption* to `dictionary.md`.

## Guide's background *(optional reading)*

This is *Computer Networks: A Systems Approach*, Section 5.2 ("Reliable
Byte Stream (TCP)"). TCP gives programs a reliable, in-order stream of
bytes on top of IP's unreliable packets: it numbers every byte (`seq`),
the other side acknowledges what it's received (`ack`), and anything not
acknowledged in time is sent again. The `win` (window) is how much the
receiver can take before the sender must wait. The `seq` numbers start
at a random value, so they look huge; `tcpdump` shows later ones
relative to the start (`1:15`).

`tcpdump` captures packets as the network card sees them, which needs
admin power (the `CAP_NET_RAW` capability). On a home Wi-Fi network,
a computer mostly sees its own traffic; but on many networks, capturing
can show other people's, which is why it's a "Sandbox only" tool here,
and why the lesson ties it to the Pledge. The graphical version,
**Wireshark**, is installed by `install-packages.sh --later` for you to
explore if you like; it asks during installation whether non-admin
users may capture: answer **No**.

Step 9 is the strongest argument for encryption a learner can see:
plain TCP is readable by anyone on the path; `ssh` (and HTTPS) agree a
secret key at the start, and everything after that, passwords
included, is encrypted. Lessons 11.12 and 11.13 explain how two
computers can agree a secret while someone listens.
