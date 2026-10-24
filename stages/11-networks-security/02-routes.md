# Lesson 11.2: Hop by Hop: Routers and Routes

**Time:** 2 sessions of 45 min · **You need:** a terminal; the Sandbox;
paper and coloured pens; 4 or 5 helpers or soft toys (to be routers);
the internet for step 6 (optional) · **New words:** router, route,
routing table, default route, gateway, hop, TTL, `tracepath`

## Goal *(read this to the learner)*

> A packet to the other side of the world doesn't know the way. Nobody
> does! Each router only knows which way to pass it next, like a chain
> of people passing a bucket. Today you'll be a router, watch real
> packets hop across the internet, and write a little internet in
> Python, then break it to see why every packet carries a countdown.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] The Sandbox switched on; the learner's sticky note with its
      address (Lesson 11.1).
- [ ] Write five place names on cards, one each: **home**, **village**,
      **portal**, **stronghold**, **end**. Put them around the room in a
      line, in that order, with a helper or a toy at each one.

## Warm-up (5 min)

"What's the Sandbox's address? The family computer's, on the same
street?" *(From the sticky note: `172.17.0.4` and `172.17.0.1`.)* "Which
ping took longest last time, and why?" *(The far one, `1.1.1.1`: more
distance and more routers.)*

## Activity

### Session 1: passing it on

1. **Be the routers.** Each place card gets a small **routing table**,
   written on its back:
   ```
   home:        anywhere else -> village
   village:     home -> home;  anywhere else -> portal
   portal:      home or village -> village;  anywhere else -> stronghold
   stronghold:  end -> end;  anywhere else -> portal
   end:         anywhere else -> stronghold
   ```
   Write an envelope **To: end, From: home**. The learner stands at
   **home**, reads the table, and walks the envelope to wherever it
   says; then reads the next table, and so on. **Ask:** "Did anyone know
   the whole way?" *(No: each one only knew the next step.)* **Say:**
   "That's a **router**: a computer that passes packets on. Its list is
   a **routing table**. Each step is a **hop**." Send a reply back, from
   end to home.

2. **The family computer's table.** In a terminal:
   ```
   ip route
   ```
   **They should see** something like:
   ```
   default via 192.168.50.1 dev wlp3s0 proto dhcp src 192.168.50.23 metric 600
   172.17.0.0/16 dev docker0 proto kernel scope link src 172.17.0.1
   192.168.50.0/24 dev wlp3s0 proto kernel scope link src 192.168.50.23 metric 600
   ```
   **Say:** "Read it like the cards. Anything on the `172.17` street goes
   straight out of the `docker0` door. Anything on the `192.168.50`
   street goes out of the Wi-Fi. And `default` means 'anywhere else':
   give it to `192.168.50.1`, the house's router. That's the
   **gateway**: the way out to the world." Ask the kernel which way it
   would send things:
   ```
   ip route get 172.17.0.4
   ip route get 1.1.1.1
   ```
   **They should see:**
   ```
   172.17.0.4 dev docker0 src 172.17.0.1 uid 1000
       cache
   1.1.1.1 via 192.168.50.1 dev wlp3s0 src 192.168.50.23 uid 1000
       cache
   ```
   **Ask:** "Which one goes through the router?" *(`1.1.1.1`: `via`
   means 'hand it to'.)*

3. **The Sandbox's table.** Log in to the Sandbox (`ssh LEARNER@localhost
   -p 2222`) and run `ip route` there. **They should see:**
   ```
   default via 172.17.0.1 dev eth0
   172.17.0.0/16 dev eth0 proto kernel scope link src 172.17.0.4
   ```
   **Ask:** "Who is the Sandbox's gateway?" *(`172.17.0.1`: the family
   computer! It's a router for the Sandbox.)* Add the router arrows to
   the drawing from Lesson 11.1: Sandbox → family computer → house
   router → internet.

### Session 2: the countdown

4. **A little internet in Python.** On the family computer:
   ```
   mkdir -p ~/lab/net/python
   cd ~/lab/net/python
   git init
   ```
   **Say:** "`~/lab/net` is this stage's folder. The Python programs live
   in `python`, which is a git repository; each Rust project will be its
   own, like Stage 10's." Make `routes.py`:
   ```python
   # Each router's table says where to pass a packet next.
   # "default" means "anywhere else".
   tables = {
       "home":       {"default": "village"},
       "village":    {"home": "home", "default": "portal"},
       "portal":     {"home": "village", "village": "village", "default": "stronghold"},
       "stronghold": {"end": "end", "default": "portal"},
       "end":        {"default": "stronghold"},
   }


   def send(start, to, ttl=8):
       print(f"A packet from {start} to {to}:")
       here = start
       while here != to:
           if ttl == 0:
               print(f"  {here}: the TTL ran out! The packet is thrown away.")
               return
           table = tables[here]
           hop = table.get(to, table["default"])
           print(f"  {here} -> {hop}   (ttl {ttl})")
           here = hop
           ttl = ttl - 1
       print(f"  Arrived at {to}.")


   send("home", "end")
   send("end", "home")
   ```
   ```
   python3 routes.py
   ```
   **They should see:**
   ```
   A packet from home to end:
     home -> village   (ttl 8)
     village -> portal   (ttl 7)
     portal -> stronghold   (ttl 6)
     stronghold -> end   (ttl 5)
     Arrived at end.
   A packet from end to home:
     end -> stronghold   (ttl 8)
     stronghold -> portal   (ttl 7)
     portal -> village   (ttl 6)
     village -> home   (ttl 5)
     Arrived at home.
   ```
   **Say:** "`table.get(to, table["default"])` means: look up where it's
   going, and if it's not in the table, use `default`. Just like the
   cards."

5. **Break it.** **Say:** "A router's owner makes a typing mistake."
   Change the village's `"default": "portal"` to `"default": "home"`,
   and run it again. **They should see:**
   ```
   A packet from home to end:
     home -> village   (ttl 8)
     village -> home   (ttl 7)
     home -> village   (ttl 6)
     village -> home   (ttl 5)
     home -> village   (ttl 4)
     village -> home   (ttl 3)
     home -> village   (ttl 2)
     village -> home   (ttl 1)
     home: the TTL ran out! The packet is thrown away.
   ```
   **Ask:** "What would happen without the TTL?" *(The packet would go
   round and round for ever, and more and more lost packets would fill
   up the network.)* **Say:** "**TTL** means 'time to live'. Every real
   packet carries one, and every router takes one off. At zero, the
   router throws the packet away, and sends a little 'time exceeded'
   note back to whoever sent it." Mend the mistake. Commit.

6. **Real hops** *(needs the internet)*. On the family computer:
   ```
   ping -c 1 -t 1 1.1.1.1
   ```
   **They should see:**
   ```
   PING 1.1.1.1 (1.1.1.1) 56(84) bytes of data.
   From 192.168.50.1 icmp_seq=1 Time to live exceeded
   ```
   **Say:** "`-t 1` sent it with a TTL of just 1. The first router, the
   house's, took it to 0, threw it away, and told us. Now we know who
   the first hop is!" Try `-t 2`: **they should see** a different
   address, the next router along. **Say:** "Do that with 1, 2, 3, and so
   on, and you can map the whole path. A tool does exactly that:"
   ```
   tracepath -n 1.1.1.1
   ```
   **They should see** something like (it takes a while; Ctrl+C to stop
   early):
   ```
    1?: [LOCALHOST]                      pmtu 1500
    1:  192.168.50.1                                          1.401ms
    1:  192.168.50.1                                          2.253ms
    2:  142.254.149.93                                       12.121ms
    3:  no reply
    4:  65.29.38.78                                          12.690ms
    5:  65.29.33.206                                         15.340ms asymm  6
    6:  24.33.105.240                                        20.621ms asymm  7
    7:  65.25.137.132                                        23.132ms asymm  6
    8:  65.29.33.229                                         23.784ms
    9:  172.68.168.2                                         21.727ms
   10:  172.68.168.17                                        24.732ms
   11:  no reply
   ```
   **Say:** "Each line is a router on the way, with how long it took to
   answer. `no reply` is a router that's been told not to send the
   'time exceeded' notes. That's allowed: it still passes packets on."
   Now run it from the **Sandbox**:
   ```
   tracepath -n -m 4 1.1.1.1
   ```
   **They should see:**
   ```
    1?: [LOCALHOST]                      pmtu 1500
    1:  172.17.0.1                                            0.128ms
    1:  172.17.0.1                                            0.037ms
    2:  192.168.50.1                                          1.320ms
    3:  142.254.149.93                                       11.786ms
    4:  no reply
   ```
   **Ask:** "What's the Sandbox's first hop?" *(The family computer.)*
   "Its second?" *(The house router.)* That's the drawing, proved.

7. **How do routers learn their tables?** **Say:** "Small networks, like
   ours, are typed in or set up automatically. On the internet, routers
   talk to their neighbours all the time, sharing which places they can
   reach and how far away they are, and each one works out the cheapest
   path. Remember Dijkstra's algorithm, from Lesson 7.15? Many routers
   run it, every time the map changes." *(If a cable breaks, the
   routers find a way around it, by themselves, in seconds.)*

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `KeyError: 'default'` | A table is missing its `default` line | Check each table in `routes.py`. |
| `tracepath: command not found` | It's not installed | Ask the guide: `sudo apt install iputils-tracepath`. In the Sandbox, the guide rebuilds it. |
| Every line after the first says `no reply` | Offline, or the house router blocks it | Check `ping -c 1 1.1.1.1`. If that works, it's the router; that's fine. |
| `tracepath` never reaches `1.1.1.1` | Its last routers don't answer `tracepath`'s kind of packet | Normal. Ctrl+C. |
| `From 192.168.50.1 ... Destination Host Unreachable` | The router can't find that address | Check the number. |

## Talk about it

- Does any router know the whole way? How does the packet get there,
  then?
- What does `default` mean in a routing table? What's a gateway?
- What does TTL stand for, and what would happen without it?
- How did `-t 1` find the first router?

## Challenge *(if there's time, or for next time)*

- In `routes.py`, send a packet from home to `"school"`, a place that
  isn't on the map. What happens, and why? *(It bounces between portal
  and stronghold until the TTL runs out.)*
- Add a shortcut: a new router `"nether"` between village and
  stronghold. Change the tables so packets from home take it. Is it
  fewer hops?
- Replies from `1.1.1.1` came back with `ttl=56` in Lesson 11.1. They
  start at 64. How many routers did the reply pass through?
  *(64 − 56 = 8.)*

## Checkpoint

The learner can, without help:
- [ ] Explain routing as passing a packet on, one hop at a time
- [ ] Read `ip route`, and find the gateway
- [ ] Explain the TTL, with `routes.py`'s loop
- [ ] Run `tracepath`, and explain its lines

## Lab notebook

Copy the five routing table cards. Draw the path from the Sandbox to
`1.1.1.1`, one box per hop, with the times. Commit. Add *router*,
*routing table*, *default route*, *gateway*, *hop* and *TTL* to
`dictionary.md`.

## Guide's background *(optional reading)*

This is *Computer Networks: A Systems Approach*, Chapter 3
("Internetworking"), in the offline library. Routers decide where each
packet goes using only the destination address and their own table;
the most specific matching line wins (`192.168.50.0/24` beats
`default`), which is called **longest-prefix match**.

Inside one organisation, routers share their maps with protocols like
**OSPF** (which runs Dijkstra's shortest-path algorithm from Lesson
7.15). Between the internet's big networks, **BGP** shares which
networks each can reach; mistakes in BGP have taken large parts of the
internet offline for hours, which is the real version of step 5.

`tracepath` (and its cousin `traceroute`, in the `traceroute` package)
works exactly as step 6 says: it sends packets with TTL 1, 2, 3 and so
on, and listens for the "time exceeded" messages (ICMP) that each
router sends back. Lines with `asymm` mean the reply came back a
different way from the one the packet went: paths across the internet
aren't always the same in both directions.
