#!/usr/bin/env python3
"""Network gatekeepers for levels 16 and 19. Runs as root inside the container."""
import random
import socketserver
import threading


def password(n):
    with open(f"/etc/mineshaft/pass/miner{n}") as f:
        return f.read().strip()


class Gatekeeper(socketserver.StreamRequestHandler):
    """Level 16: send this level's password, get the next one."""

    def handle(self):
        self.wfile.write(b"GATEKEEPER: Who goes there? Type the password for miner16.\n")
        self.request.settimeout(120)
        try:
            got = self.rfile.readline().decode(errors="replace").strip()
        except OSError:
            return
        if got == password(16):
            self.wfile.write(f"GATEKEEPER: Welcome, friend. The password for miner17 is: {password(17)}\n".encode())
        else:
            self.wfile.write(b"GATEKEEPER: That is not the password for miner16. Go away!\n")


class VaultGuard(socketserver.StreamRequestHandler):
    """Level 19: twenty sums, one second each. Needs a script."""

    def handle(self):
        self.request.settimeout(1.0)
        self.wfile.write(b"HELLO MINER. 20 QUESTIONS. 1 SECOND EACH.\n")
        for _ in range(20):
            a, b = random.randint(1000, 9999), random.randint(1000, 9999)
            self.wfile.write(f"WHAT IS {a} + {b}?\n".encode())
            try:
                got = self.rfile.readline().decode(errors="replace").strip()
            except OSError:
                got = None
            if got != str(a + b):
                self.wfile.write(b"BOOM\n")
                return
            self.wfile.write(b"CORRECT\n")
        self.wfile.write(f"THE VAULT OPENS. The password for miner20 is: {password(20)}\n".encode())


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    servers = [Server(("127.0.0.1", 30016), Gatekeeper), Server(("127.0.0.1", 30019), VaultGuard)]
    for s in servers[1:]:
        threading.Thread(target=s.serve_forever, daemon=True).start()
    servers[0].serve_forever()
