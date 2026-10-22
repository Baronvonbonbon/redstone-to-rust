# Lesson 5.12: Processes and Ports

**Time:** 2 sessions of 45 min · **You need:** two terminal windows on
the family computer; a web browser · **New words:** process, PID,
background, `kill`, port, server, client

## Goal *(read this to the learner)*

> A computer runs lots of programs at the same time: right now there are
> probably hundreds. Each running program is called a **process**. Today
> you'll spy on them, pause them, stop them, and then learn how programs
> talk to each other through numbered doors called **ports**. You'll build
> a chat line between two terminals, and run your own tiny website.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Open two terminal windows side by side for the learner (left and
      right), as in the Mineshaft lessons.

## Warm-up (5 min)

"When you log in to the Mineshaft, which number do you type after `-p`?"
*(2220.)* "And the Sandbox?" *(2222.)* "What do you think that number
is?" *(It's a port: today's topic!)*

## Activity

### Session 1: processes

1. **What's running?**
   ```
   ps
   ps aux | wc -l
   ```
   **They should see:** a tiny list (`bash` and `ps` itself), then a
   number in the hundreds. **Say:** "`ps` alone shows only the processes in
   this terminal. `ps aux` shows *every* process on the computer, from
   every user. `wc -l` counts them."

2. **Read the list.** `ps aux | head`. Point out the columns: `USER` (who
   it belongs to), `PID` (the **process ID**, its unique number), `%CPU`
   and `%MEM` (how much of the processor and memory it uses), and
   `COMMAND` (what's running). Find some: `ps aux | grep bash`,
   `ps aux | grep firefox` (if the browser is open).

3. **The live view.** `top`. **They should see:** a list that updates
   every few seconds, with the busiest processes at the top. Press `q` to
   quit. **Say:** "When the computer is slow, `top` shows who's hogging
   it."

4. **Background and foreground.** A program that waits a long time:
   ```
   sleep 300
   ```
   The terminal is stuck. Press **Ctrl+C**: it stops. **Say:** "Ctrl+C
   stops the program in front, the **foreground**." Now:
   ```
   sleep 300 &
   jobs
   ```
   **They should see:** something like `[1] 12345` (the job number and
   the PID), then `[1]+  Running   sleep 300 &`. **Say:** "The `&` runs it
   in the **background**. You can keep typing while it runs. You did this
   with `digital &` in Stage 4!"

   ```
   fg
   ```
   brings it to the front (stuck again). Press **Ctrl+Z**: **They should
   see:** `Stopped`. That's paused, not ended. `bg` sets it running in the
   background again. `jobs` shows it.

5. **Stopping processes.**
   ```
   kill %1
   jobs
   ```
   (`%1` is job number 1.) **They should see:** `Terminated`. Another way,
   with the PID:
   ```
   sleep 500 &
   ps
   kill 12345
   ```
   (With the PID that `ps` shows for `sleep`.) **Say:** "`kill` sends a
   process a message asking it to stop. You can only kill your *own*
   processes, unless you're root. Try `pkill sleep` to stop every `sleep`
   you own, by name."

### Session 2: ports

6. **Ports are doors.** **Say:** "A computer has 65,536 numbered doors,
   called **ports**. (That number should look familiar: 2 to the power of
   16!) A program that waits behind a port for visitors is a **server**.
   A program that knocks on the door is a **client**. SSH servers usually
   wait at port 22. Our Mineshaft waits at 2220."

   See which doors have servers waiting:
   ```
   ss -ltn
   ```
   **They should see:** a list with `LISTEN` lines and addresses like
   `127.0.0.1:2220` (the Mineshaft) and `127.0.0.1:2222` (the Sandbox).
   **Say:** "`127.0.0.1` means 'this computer only', the same as
   `localhost`. Nobody else on the network can reach those doors."

7. **A chat line.** Two terminals.
   - **Right terminal (the server):** `nc -l 4444`
   - **Left terminal (the client):** `nc localhost 4444`

   Type a message in the left one and press Enter. **They should see:** it
   appear in the right one! Type in the right one too: it works both
   ways. **Say:** "`nc` (netcat) is the simplest network program there is:
   it just sends whatever you type through a port. You're doing what every
   chat app does, with no app." Press **Ctrl+C** in one window to hang up;
   the other one ends too.

   While the server is waiting, run `ss -ltn` in a third terminal, and
   find port 4444 in the list.

8. **Your own web server.** In the right terminal:
   ```
   cd ~/lab
   python3 -m http.server 8000 --bind 127.0.0.1
   ```
   **They should see:** `Serving HTTP on 127.0.0.1 port 8000`. (The
   `--bind 127.0.0.1` keeps it to this computer only.) In the web
   browser, go to `http://localhost:8000`. **They should see:** a list of
   the files in `~/lab`, as a web page! Click into `notebook` and open
   `stage5.md`. The terminal shows a line for every page the browser asks
   for. **Say:** "That's a real web server. Every website in the world is a
   program like this, waiting behind port 80 or 443 on some computer."
   Press **Ctrl+C** to stop it.

9. **Talk to the web server by hand.** Start it again, and in the left
   terminal:
   ```
   printf 'GET / HTTP/1.0\r\n\r\n' | nc localhost 8000 | head -5
   ```
   **They should see:** `HTTP/1.0 200 OK` and some lines of information.
   **Say:** "That's exactly what the browser sends: a short polite message
   saying 'GET me the page at /'. Web browsers and servers are just
   programs talking through a port, using an agreed language called
   **HTTP**." Stop the server with Ctrl+C.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `nc localhost 4444` ends straight away, with nothing | Nothing is listening on that port | Start the server side (`nc -l 4444`) first. `nc -v` explains: `Connection refused`. |
| `kill: (12345) - No such process` | Wrong PID, or it already ended | Check with `ps`. |
| `kill: (1234) - Operation not permitted` | That process belongs to someone else | You can only stop your own processes. |
| `OSError: [Errno 98] Address already in use` from Python | The web server is still running in another terminal | Stop the old one with Ctrl+C, or use port 8001. |
| The browser says it can't connect | The web server isn't running, or the port number is different | Check the terminal says `Serving HTTP on 127.0.0.1 port 8000`. |
| A program won't stop with Ctrl+C | It's in the background | `fg` first, or `kill` its PID. |

## Talk about it

- What's the difference between a program and a process?
- What do Ctrl+C, Ctrl+Z, `&`, `fg` and `kill` each do?
- What's a port? What's the difference between a server and a client?
- Why does `127.0.0.1` keep the Mineshaft safe from other computers?

## Challenge *(if there's time, or for next time)*

- `ps aux --sort=-%mem | head -5`: which programs use the most memory?
- Put an `index.html` file in a folder (a heading and a sentence, in
  HTML: `<h1>My Base</h1><p>Welcome!</p>`), and serve that folder. What
  does the browser show now?
- `pstree` draws the processes as a family tree: every process has a
  parent. Find your terminal and its `bash`.

## Checkpoint

The learner can, without help:
- [ ] List processes with `ps` and `ps aux`, and find one with `grep`
- [ ] Run something in the background, bring it back, and stop it
- [ ] Explain what a port is, and see listening ports with `ss -ltn`
- [ ] Set up an `nc` chat between two terminals

## Lab notebook

Write a notebook entry about processes and ports, and commit it. Add
*process*, *PID*, *background*, *kill*, *port*, *server* and *client* to
`dictionary.md`.

## Guide's background *(optional reading)*

A **process** is a running instance of a program, with its own memory
and a unique **PID**. `kill` sends a *signal*; the default one (TERM)
politely asks the process to end, Ctrl+C sends another (INT), and Ctrl+Z
pauses (STOP). Stage 10 builds on this when the learner studies how an
operating system schedules processes.

A **port** number lets one computer run many network servers at once;
an address plus a port identifies one door on one machine. Listening
only on `127.0.0.1` (localhost) means only programs on the same computer
can connect, which is why the Mineshaft and the Sandbox are safe on a
home network. Python's `http.server` listens on *all* addresses unless
told otherwise, so the lesson adds `--bind 127.0.0.1`; without it, other
devices on your home network could see the folder while it runs.

Speaking HTTP by hand with `nc` is the first look at network
**protocols**: agreed languages for programs. Stage 11 goes much deeper,
and Mineshaft level 19 (Lesson 5.15) asks the learner to write a client
for a made-up protocol.
