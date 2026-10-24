# Lesson 11.1: Messages in Envelopes

**Time:** 2 sessions of 45 min · **You need:** a terminal; the Sandbox,
switched on (see the Stage 11 README); 8 index cards or small pieces of
paper; 8 envelopes (or folded paper); a pen · **New words:** network,
packet, protocol, layer, IP address, interface, loopback, MAC address,
`ping`

## Goal *(read this to the learner)*

> When you watch a video, the computer at the other end doesn't send
> you the video. It sends thousands of tiny pieces, each in its own
> envelope with an address on it, and your computer puts them back
> together. Today you'll play the envelope game, find your computer's
> addresses, and send your first messages to a second computer: the
> Sandbox, from Stage 5.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] The Sandbox must be rebuilt for Stage 11 (once): see the Stage 11
      README, "Tools". Then `./sandbox.sh start`, from your account.
- [ ] Cards and envelopes for the game. Write this message on a sheet of
      paper (or make up your own, eight words long):
      **"THE PRINCIPAL'S UNDERPANTS ARE ON THE FLAGPOLE AGAIN"**.
- [ ] Find somewhere in the house to be "the far computer": another
      room, or the far end of the table.

## Warm-up (5 min)

"In Stage 10, how did a program print something?" *(It asked the kernel,
with a system call.)* "How do you think a program sends something to
another computer?" *(Same idea: it asks the kernel, and the kernel
talks to the network card.)* "What's the furthest computer you've ever
talked to?" *(Every web page is one!)*

## Activity

### Session 1: the envelope game

1. **One message, many pieces.** **Say:** "Networks don't send big
   things in one go. They cut them into small pieces called **packets**.
   You're my computer, and you want to send this message to the far
   computer." Give them the message and the cards.
   - They write **one word on each card**. **Ask:** "If the cards get
     muddled up on the way, how will the far end know the order?"
     *(Number them!)* They number the cards 1 to 8.
   - Each card goes in an envelope. On the front, they write **To:**
     "Far computer" and **From:** "My computer". **Say:** "That's the
     address. Every packet carries both, so the answer knows where to
     go back to."
   - They carry the envelopes, a few at a time, to the far computer.
     Secretly hide one in your pocket on the way (a lost packet).

2. **At the other end.** The learner goes to the far computer and opens
   the envelopes. **Ask:** "Can you read the message?" *(Not quite: one
   is missing.)* "How do you know which one?" *(A number is missing.)*
   **Say:** "So the far computer sends a little note back: 'Please send
   card 5 again.' Real computers do exactly that." Give back the lost
   envelope, after they ask for it properly.

3. **The layers.** **Say:** "Look at how many jobs we had." Write a
   stack on paper, from the top:
   ```
   the message           what you want to say          (the program)
   numbered cards        cut up, in order, resend      (TCP)
   envelopes             To and From addresses         (IP)
   carrying them         walking down the hall         (Wi-Fi or a cable)
   ```
   **Say:** "Each job is a **layer**, and each layer only cares about its
   own job. The person carrying envelopes doesn't read the cards. The
   cards don't care whether they're carried by hand or by bike. The
   rules for each layer are a **protocol**: an agreed way to talk. You
   met one in Stage 5: HTTP, the web's protocol."

### Session 2: real addresses

4. **Your computer's addresses.** Open a terminal on the family
   computer.
   ```
   ip -br addr
   ```
   **They should see** something like this (yours will have different
   names and numbers, and maybe more lines):
   ```
   lo               UNKNOWN        127.0.0.1/8 ::1/128
   enp0s25          DOWN
   wlp3s0           UP             192.168.50.23/24
   docker0          UP             172.17.0.1/16 fe80::3c35:b2ff:fe64:aea6/64
   ```
   **Say:** "Each line is an **interface**: a way in and out of the
   computer, like a door. The number after the name is this computer's
   **IP address** on that door."
   - "`lo` is the **loopback**: a pretend door that leads straight back
     into the same computer. `127.0.0.1` always means 'me'."
   - "A name starting `wl` is Wi-Fi (wireless). A name starting `en` or
     `eth` is a cable (Ethernet). `UP` means it's working; `DOWN` means
     nothing's plugged in."
   - "`docker0` is a pretend network inside this computer, which the
     Sandbox is plugged into."
   - "The long ones with colons are the new kind of address, IPv6. We'll
     use the old kind, IPv4: four numbers with dots."

5. **An address is four bytes.** Take the Wi-Fi (or cable) address, like
   `192.168.50.23`. **Ask:** "What's the biggest number one byte can
   hold?" *(255, from Stage 4.)* "So an IPv4 address is four bytes:
   how many bits?" *(32.)* Turn each number into binary on paper, as in
   Stage 4, or in Python:
   ```
   python3 -c "print(format(192, '08b'))"
   ```
   ```
   192      168      50       23
   11000000 10101000 00110010 00010111
   ```
   **Say:** "The `/24` means the first 24 bits are the **street**, the
   network everyone in this house shares, and the last 8 bits are the
   **house number** on that street." **Ask:** "How many house numbers
   can 8 bits make?" *(2⁸ = 256. Two are kept for special jobs, so 254
   devices could join this network.)* "How many addresses can 32 bits
   make, altogether?" *(2³² = 4,294,967,296: about 4 billion. Fewer
   than the people on Earth! That's why IPv6 was invented, with 128
   bits.)*

6. **Hardware names.**
   ```
   ip -br link
   ```
   **They should see** each interface again, now with a number like
   `60:67:20:2b:56:82`. **Say:** "That's the **MAC address**: the name
   burned into the network card when it was made, six bytes in hex.
   IP addresses are like postal addresses, which can change when you
   move; a MAC address is like your name. The bottom layer, carrying
   envelopes across one room, uses MAC addresses."

7. **A second computer.** Log in to the Sandbox, in a new terminal tab:
   ```
   ssh LEARNER@localhost -p 2222
   ```
   (with their own name). The prompt changes to `...@sandbox`. In the
   Sandbox:
   ```
   ip -br addr
   ```
   **They should see** something like:
   ```
   lo               UNKNOWN        127.0.0.1/8 ::1/128
   eth0@if652       UP             172.17.0.4/16
   ```
   **Say:** "The Sandbox has its own loopback, and one door, `eth0`, onto
   the `docker0` street. Its address is `172.17.0.4` (yours may end
   differently). The family computer is on the same street, at
   `172.17.0.1`." Write both addresses on a sticky note: they'll need
   them all stage. Draw the two computers, joined by a line labelled
   `docker0`.

8. **Knock, knock: `ping`.** In the **family computer's** tab, use the
   Sandbox's address:
   ```
   ping -c 3 172.17.0.4
   ```
   **They should see:**
   ```
   PING 172.17.0.4 (172.17.0.4) 56(84) bytes of data.
   64 bytes from 172.17.0.4: icmp_seq=1 ttl=64 time=0.081 ms
   64 bytes from 172.17.0.4: icmp_seq=2 ttl=64 time=0.085 ms
   64 bytes from 172.17.0.4: icmp_seq=3 ttl=64 time=0.098 ms

   --- 172.17.0.4 ping statistics ---
   3 packets transmitted, 3 received, 0% packet loss, time 2068ms
   rtt min/avg/max/mdev = 0.081/0.088/0.098/0.007 ms
   ```
   **Say:** "`ping` sends a tiny packet that says 'are you there?', and
   the other computer's kernel answers 'yes!' by itself. `time` is how
   long the round trip took, in milliseconds: thousandths of a second.
   `-c 3` means three times; without it, `ping` keeps going until
   Ctrl+C."

   Now ping the other way, from the **Sandbox's** tab:
   ```
   ping -c 3 172.17.0.1
   ```
   **They should see** the same kind of answers, from `172.17.0.1`.

9. **How far is it?** From the family computer, ping four places, and
   write the average time (the middle number of `rtt`) for each:
   ```
   ping -c 3 127.0.0.1
   ping -c 3 172.17.0.4
   ip route
   ```
   The `ip route` line starting `default via` names the **router**: the
   box that connects the house to the internet, like
   `default via 192.168.50.1`. Ping that address too. Then, if the
   computer is online, a computer far away (it belongs to a company
   that's happy to be pinged):
   ```
   ping -c 3 1.1.1.1
   ```
   **They should see** times like these:

   | Where | Average time |
   |---|---|
   | `127.0.0.1` (me) | 0.08 ms |
   | the Sandbox | 0.09 ms |
   | the router | 1.4 ms |
   | `1.1.1.1` | 20 ms |

   **Ask:** "Why is the Sandbox so close?" *(It's inside this computer.)*
   "Why is the router slower?" *(The packet really travels by radio, and
   the router's a small, slow computer.)* "Light in a glass cable goes
   about 200 km in a millisecond. In 20 ms, there and back, how far away
   could `1.1.1.1` be, at most?" *(10 ms each way × 200 km = 2,000 km.
   It's usually much nearer, because routers on the way slow it down.)*

10. **Leave the Sandbox:** `exit`.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `ssh: connect to host localhost port 2222: Connection refused` | The Sandbox is off | The guide runs `./sandbox.sh start`. |
| `ping: connect: Network is unreachable` | No network at all (or a mistyped address) | Check the address with `ip -br addr`; `127.0.0.1` and the Sandbox work with no internet. |
| `ping` prints nothing for a long time, then `100% packet loss` | Nobody answered: a wrong address, or a computer that's been told not to answer pings | Check the number. Some routers don't answer pings; that's fine. |
| `ping: 1.1.1.1: Temporary failure in name resolution`, or no answers from `1.1.1.1` | The computer is offline | Skip that row; it's fine. |
| `-bash: ip: command not found` (in the Sandbox) | An old Sandbox | The guide rebuilds it (the Stage 11 README). |
| The Sandbox's address isn't `172.17.0.4` | Docker gave it a different number | Use the one `ip -br addr` shows in the Sandbox. It can change after `./sandbox.sh reset`. |

## Talk about it

- Why cut a message into packets, instead of sending it in one go?
  *(If one gets lost, only that one is sent again; and many people's
  packets can share the same cable, taking turns.)*
- What are the four layers of the envelope game?
- What's the difference between an IP address and a MAC address?
- What does `127.0.0.1` mean, on any computer?

## Challenge *(if there's time, or for next time)*

- Work out the address `10.0.0.1` in binary. Which byte is all zeros?
- `ping -c 3 -s 1000 172.17.0.4` sends bigger packets. Are they slower?
- How many IPv6 addresses are there? *(2¹²⁸.)* Python can work it out:
  `python3 -c "print(2**128)"`. Read the number out loud, if you can.

## Checkpoint

The learner can, without help:
- [ ] Explain packets and layers with the envelope game
- [ ] Find their computer's IP addresses, and explain `/24`
- [ ] Turn an IP address into 32 bits
- [ ] Use `ping`, and say what the time means

## Lab notebook

Draw the envelope game's four layers. Draw the family computer and the
Sandbox with their addresses, joined by `docker0`, with the router and
the internet beyond. Write the four ping times. Add *network*,
*packet*, *protocol*, *layer*, *IP address*, *interface*, *loopback*,
*MAC address* and *ping* to `dictionary.md`.

## Guide's background *(optional reading)*

This stage follows the free textbook *Computer Networks: A Systems
Approach* (Peterson and Davie) for the networking half: Chapter 1 covers
packets and layers. It's in the offline library; it's written for
university students, so it's for you, or for reading together later.

The four layers of the game are the internet's real layers: the
**application** (the message), **transport** (TCP, which numbers the
pieces and resends lost ones), **network** (IP, the addresses and the
routing of each packet), and **link** (Wi-Fi or Ethernet, which carries
a packet across one hop using MAC addresses). Each layer wraps the one
above in its own envelope, with its own label on the front, called a
**header**.

IPv4 addresses are 32 bits, written as four bytes; there are only about
4 billion, so homes use **private** addresses (`192.168.x.x`, `10.x.x.x`
and `172.16–31.x.x`) that are re-used in every house, and the router
swaps them for one public address on the way out (that's **NAT**). The
Sandbox is on a private network inside the computer, made by Docker;
that's why it's safe to experiment with: nothing outside this computer
can reach it. `ping` uses **ICMP**, a small helper protocol of IP. Lesson
11.2 shows what `ttl` means.
