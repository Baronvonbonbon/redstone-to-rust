# The Sandbox: the Guide's Handbook

The Sandbox is Stage 5's **breakable computer**: a small Ubuntu 24.04
Linux system in a Docker container, where the learner is the admin. They
log in over `ssh`, use `sudo`, add users, install packages, and break
things on purpose. When something is broken beyond repair, one command
from you makes a brand-new one in seconds.

It needs internet only once, to build it. It has no learner accounts or
email anywhere, and it only listens on `localhost`, so nobody else on
your network can reach it.

## Running it

Run everything from the **guide's** account (the learner's account must
not be in the `docker` group):

```bash
./sandbox.sh build LEARNER   # once, while online (about 5 minutes); use the learner's account name
./sandbox.sh start           # turns it on; it comes back by itself after a reboot
./sandbox.sh status
./sandbox.sh stop            # turns it off; everything inside it is kept
./sandbox.sh reset           # throws it away and makes a brand-new one
```

The learner logs in with `ssh LEARNER@localhost -p 2222`. The first
password is the learner's name; Lesson 5.1 has them change it.

**`reset` is the fix for everything**: a forgotten password, a broken
`sudo`, deleted system files. Everything the learner did inside the
Sandbox is gone afterwards, and the password goes back to their name.
Lesson 5.3 breaks it on purpose so the learner sees that.

## What's inside

- The learner's account, in the `sudo` group (so `sudo` works with their
  own password), and root (no direct login).
- The manual pages (`man`), `nano`, `vim`, `less`, `tree`, `file`, `htop`,
  `ps`, `ss`, `nc`, `git`, `python3` and `sqlite3`.
- Four packages **downloaded but not installed**: `cowsay`, `figlet`, `sl`
  and `toilet`. Lesson 5.3 installs and removes them with `apt`, with no
  internet. Other packages need the internet (see below).

## Which lessons use it

| Lesson | What happens in the Sandbox |
|---|---|
| 5.1 | First login, changing the password, `sudo`, a tour of the folders |
| 5.2 | Permissions; adding a user and a group |
| 5.3 | Installing packages; breaking things and fixing them; a reset |
| 5.11 | Challenge: pushing a git repository to the Sandbox over `ssh` |
| 5.16 | The Stage 5 checkpoint |
| 11.1–11.4 | A second computer on the network: `ping`, routes, `/etc/hosts`, `nc` chats, and watching its own packets with `tcpdump` |
| 11.13 | Logging in with a key instead of a password |
| 11.15 | Open ports and a firewall (`ufw`) |

**Stage 11 needs the Sandbox rebuilt**, because it adds network tools
(`ping`, `tracepath`, `dig`, `tcpdump`, `curl`, `ufw`, `openssl`) and
starts the container with permission to run a firewall. Online, from
`labs/sandbox`: `./sandbox.sh build LEARNER`, then `./sandbox.sh reset`
(the password goes back to the learner's name), then
`ssh-keygen -R '[localhost]:2222'` in the learner's account.

Scripts, git and the other lessons happen on the family computer, in
the learner's own account. Work kept in the Sandbox doesn't survive a
reset, so anything worth keeping lives on the family computer.

## Good to know

- **Internet.** If your computer is online, so is the Sandbox, and
  `sudo apt install` can fetch any Ubuntu package. Nothing in the
  lessons needs that. If you'd rather the learner didn't install things
  freely, keep an eye on it the same way you would any computer use, or
  only start the Sandbox for Stage 5 sessions.
- **Rebuilding** (`build` again, for example for a different learner)
  gives the Sandbox a new identity, and `ssh` will warn about it with
  `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!`. That's expected:
  the learner runs `ssh-keygen -R '[localhost]:2222'` once and logs in
  again. A `reset` doesn't cause that warning.
- **Siblings.** One Sandbox is built for one learner's name. For a second
  learner, either share it (they `adduser` themselves: good practice!) or
  build it again with the other name.
- **Space.** The image is about 700 MB. `docker image rm sandbox` removes
  it when Stage 5 is over.
- **Keeping a Sandbox's state.** If the learner made something they want
  to keep inside it, copy it out before a reset, from your account:
  `docker cp sandbox:/home/LEARNER/thing ./thing`.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `ssh: connect to host localhost port 2222: Connection refused` | The Sandbox is off | `./sandbox.sh start` |
| `Permission denied, please try again.` | Wrong password | If nobody remembers it, `./sandbox.sh reset`. |
| `LEARNER is not in the sudoers file.` | The learner removed themselves from the `sudo` group | Can't be fixed from inside. `./sandbox.sh reset`. |
| `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!` | The Sandbox was rebuilt | `ssh-keygen -R '[localhost]:2222'`, then log in again. |
| `E: Unable to locate package ...` or `Temporary failure resolving` | That package isn't saved in the Sandbox, and there's no internet | Only `cowsay`, `figlet`, `sl` and `toilet` work offline. |
| `docker: Error response from daemon: ... port is already allocated` | Something else is using port 2222 | Change `PORT=2222` in `sandbox.sh` (and tell the learner the new number). |
| `permission denied while trying to connect to the Docker daemon socket` | Running from the learner's account, or you're not in the `docker` group | Run it from your own account (see [docs/SETUP.md](../../docs/SETUP.md)). |

## How it works (for curious guides)

- `Dockerfile` starts from Ubuntu 24.04, puts the manual pages back with
  `unminimize` (the Docker image leaves them out), installs the tools and
  an `ssh` server, and makes the learner's account.
- `sandbox.sh start` gives the container the `NET_ADMIN` capability, so
  the learner's `sudo ufw` can change the Sandbox's own firewall rules
  (and nothing outside it).
- To make `apt` work offline, it downloads the four packages into apt's
  cache, removes Docker's rule that empties that cache, and tells apt to
  keep downloaded files, so reinstalling works offline too.
- `sshd-sandbox.conf` allows password logins and blocks logging in as
  root. `motd` is the welcome message.
- `stop` and `start` pause and resume the same container. `reset` deletes
  the container and makes a new one from the image, which is why
  everything goes back to how it was built.
- A container shares your computer's kernel, but has its own users,
  files and processes. Root inside it can't see your files. Stage 10
  looks at how that works.

## Other breakable computers

A Raspberry Pi or a virtual machine works too, and feels even more like a
separate computer. [docs/SETUP.md](../../docs/SETUP.md) has both. The
lessons are written for the Sandbox; with a Pi or VM, use its address
instead of `localhost -p 2222`, and "re-flash the spare card" or
"restore the snapshot" instead of `./sandbox.sh reset`. Lesson 5.3's
offline packages need the internet on a Pi or VM.
