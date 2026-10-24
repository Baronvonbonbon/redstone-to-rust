# Lesson 11.7: The Web, by Hand and in Rust

**Time:** 2–3 sessions of 45 min · **You need:** a terminal with two
tabs; a text editor; Firefox; `~/lab/net`; the internet for step 9
(optional) · **New words:** HTTP, request, response, status code,
header, URL, HTML, HTTPS

## Goal *(read this to the learner)*

> Every web page you've ever seen arrived as a few lines of text, in a
> protocol called HTTP, much like your vault's. Today you'll speak HTTP
> yourself, by typing it, then write your own web server in Rust, make
> a website for the Creeper Club, and open it in Firefox.

## Before the lesson *(guide, 5 min)*

- [ ] Read this whole lesson once.
- [ ] Lesson 5.12 served a folder with Python and talked to it with
      `nc`. Glance at it, if you did it.

## Warm-up (5 min)

"In the vault's protocol, what did a command look like? And a reply?"
*(One line; replies start with `OK` or `NO`.)* "What do you think a
web browser sends when you visit a page?" Guess, and write it down.

## Activity

### Session 1: speaking HTTP

1. **A website.** Make a project for the Creeper Club's web server,
   with a folder for its site:
   ```
   cd ~/lab/net
   cargo new web
   mkdir web/site
   cd web/site
   ```
   Make three files in `site`.
   `index.html`:
   ```html
   <!DOCTYPE html>
   <html>
   <head>
     <title>The Creeper Club</title>
     <link rel="stylesheet" href="style.css">
   </head>
   <body>
     <h1>Welcome to the Creeper Club!</h1>
     <p>Members only. Ssssss...</p>
     <p><a href="rules.html">The club rules</a></p>
   </body>
   </html>
   ```
   `rules.html`:
   ```html
   <!DOCTYPE html>
   <html>
   <head><title>Club rules</title><link rel="stylesheet" href="style.css"></head>
   <body>
     <h1>The rules</h1>
     <ol>
       <li>No exploding indoors.</li>
       <li>Always hiss politely.</li>
     </ol>
     <p><a href="/">Back</a></p>
   </body>
   </html>
   ```
   `style.css`:
   ```css
   body { background: #2e7d32; color: white; font-family: sans-serif; }
   h1 { font-size: 3em; }
   a { color: yellow; }
   ```
   **Say:** "**HTML** is the page: `<h1>` is a big heading, `<p>` a
   paragraph, `<a>` a link to another page. CSS says how it looks."

2. **Serve it with Python**, as in Stage 5, in the `site` folder:
   ```
   python3 -m http.server --bind 127.0.0.1 8000
   ```
   Open `http://127.0.0.1:8000/` in Firefox, and click the link.

3. **Be the browser.** In tab 2:
   ```
   nc 127.0.0.1 8000
   ```
   Type exactly this, then press Enter **twice** (the empty line means
   "that's my whole request"):
   ```
   GET / HTTP/1.0
   ```
   **They should see:**
   ```
   HTTP/1.0 200 OK
   Server: SimpleHTTP/0.6 Python/3.12.3
   Date: Sat, 24 Oct 2026 13:56:00 GMT
   Content-type: text/html
   Content-Length: 260
   Last-Modified: Sat, 24 Oct 2026 13:55:59 GMT

   <!DOCTYPE html>
   <html>
   ...
   ```
   **Say:** "That's all a web page is! The browser sends a **request**:
   'GET me the page at `/`, I speak HTTP version 1.0'. The server sends a
   **response**: first a status line, `200 OK`; then **headers**, one
   per line, saying things about the page, like its type and its length
   in bytes; then an empty line; then the page itself."

4. **A page that isn't there.** `nc` again, with `GET /nothing.html
   HTTP/1.0` and two Enters. **They should see:**
   ```
   HTTP/1.0 404 File not found
   ```
   **Say:** "`404` is a **status code**. You've seen 'Error 404' on
   websites: now you know where it comes from. Codes starting with 2 mean
   'here you go', 3 'it's moved', 4 'you asked for something wrong', and
   5 'the server broke'."

5. **`curl` shows both sides.**
   ```
   curl -v http://127.0.0.1:8000/rules.html
   ```
   **They should see**, among other lines, the request (lines starting
   `>`) and the response's head (lines starting `<`):
   ```
   > GET /rules.html HTTP/1.1
   > Host: 127.0.0.1:8000
   > User-Agent: curl/8.5.0
   > Accept: */*
   >
   < HTTP/1.0 200 OK
   < Server: SimpleHTTP/0.6 Python/3.12.3
   < Content-type: text/html
   < Content-Length: 261
   ```
   **Say:** "The request has headers too. `User-Agent` says which program
   is asking." Look at the Python server's tab: **they should see** a line
   for every request, like `"GET /rules.html HTTP/1.1" 200 -`. Stop it
   with Ctrl+C.

### Session 2: a web server in Rust

6. **The server.** In `~/lab/net/web` (the project, with `site` in it),
   `src/main.rs`:
   ```rust
   use std::fs;
   use std::io::{BufRead, BufReader, Write};
   use std::net::{TcpListener, TcpStream};
   use std::thread;

   const NOT_FOUND: &[u8] = b"<h1>404: no such page!</h1>";

   fn content_type(path: &str) -> &str {
       if path.ends_with(".html") {
           "text/html; charset=utf-8"
       } else if path.ends_with(".css") {
           "text/css"
       } else {
           "text/plain; charset=utf-8"
       }
   }

   fn serve(mut stream: TcpStream) {
       let reader = BufReader::new(stream.try_clone().unwrap());
       let mut request = Vec::new();
       for line in reader.lines() {
           let Ok(line) = line else { return };
           if line.is_empty() {
               break;
           }
           request.push(line);
       }
       let Some(first) = request.first() else { return };
       println!("{first}");
       let words: Vec<&str> = first.split_whitespace().collect();
       let ["GET", target, _] = words.as_slice() else {
           return;
       };
       let path = if *target == "/" {
           "site/index.html".to_string()
       } else {
           format!("site{target}")
       };
       let (status, kind, body) = match fs::read(&path) {
           Ok(body) => ("200 OK", content_type(&path), body),
           Err(_) => ("404 Not Found", "text/html", NOT_FOUND.to_vec()),
       };
       let head = format!(
           "HTTP/1.0 {status}\r\nContent-Type: {kind}\r\nContent-Length: {}\r\n\r\n",
           body.len()
       );
       let _ = stream.write_all(head.as_bytes());
       let _ = stream.write_all(&body);
   }

   fn main() {
       let listener = TcpListener::bind("127.0.0.1:7880").unwrap();
       println!("Open http://127.0.0.1:7880/ in Firefox");
       for stream in listener.incoming() {
           let Ok(stream) = stream else { continue };
           thread::spawn(move || serve(stream));
       }
   }
   ```
   Read it together:
   - "`serve` reads the request's lines until the empty one, and keeps
     them in `request`."
   - "The first line is `GET /rules.html HTTP/1.1`. `let ["GET", target,
     _] = ... else` checks it has that shape, and anything else (like
     `POST`) gets no answer."
   - "`/` means the home page. Anything else, we look for in `site`."
   - "`fs::read` gives the file's bytes. If there's no such file, it's a
     404 instead."
   - "Then the response: the status line, two headers, an empty line,
     and the page. `\r\n` is how HTTP ends lines: 'carriage return, new
     line', from typewriters."
   - "`let _ =` means 'I know this could fail, and I don't mind': if the
     visitor has gone, there's nobody to tell."

7. **Visit it.** `cargo run`, then open `http://127.0.0.1:7880/` in
   Firefox. **They should see** the Creeper Club: green, with a big white
   heading and a yellow link. Click the link, and **Back**. Then try
   `http://127.0.0.1:7880/nope`. **They should see** `404: no such page!`.
   Look at the server's tab. **They should see** something like:
   ```
   Open http://127.0.0.1:7880/ in Firefox
   GET / HTTP/1.1
   GET /style.css HTTP/1.1
   GET /favicon.ico HTTP/1.1
   GET /nope HTTP/1.1
   ```
   (with more lines for the rules page). **Ask:** "We asked for one page.
   Why three requests?" *(The page needed
   its `style.css`, and Firefox asked for `favicon.ico`, the little
   picture on the tab, which we haven't got.)*

8. **Look behind the page.** In Firefox, press **F12**, choose the
   **Network** tab, and reload the page (F5). **They should see** each
   request, with its status (`200`, `404`), type and size. Click one and
   look at its **Headers**. Commit.

### Session 3: HTTPS *(needs the internet; optional)*

9. **The padlock.** **Ask:** "Remember `tcpdump -A` in Lesson 11.4? If
   you sent a password to a website like this, who could read it?"
   *(Everyone on the way.)*
   ```
   curl -sI https://www.wikipedia.org | head -5
   ```
   **They should see** something like:
   ```
   HTTP/2 200
   date: Fri, 23 Oct 2026 15:36:17 GMT
   cache-control: s-maxage=86400, must-revalidate, max-age=3600
   server: ATS/9.2.15
   etag: W/"1de35-65e335ecb78c0"
   ```
   **Say:** "`https` is the same HTTP, but wrapped in encryption first,
   so nobody on the way can read it or change it. That's what the
   padlock in the address bar means. Our club site is plain HTTP, which
   is fine, because it only travels inside this computer."

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| Firefox: `Unable to connect` | The server isn't running, or the port's wrong | `cargo run` in the `web` folder; check `7880`. |
| Every page is `404: no such page!` | The server was started from the wrong folder, so `site/...` isn't there | `cd ~/lab/net/web` first; `ls site` should show the three files. |
| The page is plain, not green | `style.css` is missing or misnamed | Check its name, and the `href` in the HTML. |
| `nc` gives nothing back | Only one Enter was pressed | Press Enter again: the empty line ends the request. |
| `curl: (60) SSL certificate problem` | The computer's clock is very wrong | Ask the guide to check the date and time. |

## Talk about it

- What's in an HTTP request? What's in a response?
- What does 404 mean? And 200?
- Why did one page make three requests?
- What's the difference between `http` and `https`?

## Challenge *(if there's time, or for next time)*

- Add a page of your own (`members.html`) with a link to it from the
  home page.
- Make the 404 page funnier, and give it the club's style.
- Count the visitors (an `AtomicU32`) and print the count in the
  server's tab with each request.
- Add a picture: put a `.png` in `site`, add `<img src="creeper.png">`,
  and give `content_type` a line for `.png` (`image/png`).

## Checkpoint

The learner can, without help:
- [ ] Type an HTTP request with `nc`, and explain the response's parts
- [ ] Explain status codes 200 and 404
- [ ] Run their Rust web server and visit it in Firefox
- [ ] Use the browser's Network tab to see the requests

## Lab notebook

Copy a request and a response, and label the parts: status line,
headers, empty line, body. Draw Firefox asking for three things for one
page. Commit. Add *HTTP*, *request*, *response*, *status code*, *header*,
*HTML* and *HTTPS* to `dictionary.md`.

## Guide's background *(optional reading)*

HTTP is the protocol of the web, invented by Tim Berners-Lee in 1989–91;
*Computer Networks: A Systems Approach*, Section 9.1, covers it, and
*The Rust Programming Language*, Chapter 21 (`rustup doc --book`),
builds a similar server. HTTP/1.0 and 1.1 are text, exactly as typed
in step 3; HTTP/2 and HTTP/3, which big sites use, carry the same
requests and headers in a compact binary form. The server here speaks
HTTP/1.0 and closes the connection after each response, which is the
simplest correct behaviour.

HTTPS is HTTP inside **TLS**, which encrypts the connection and proves
the server's identity with a certificate (Lesson 11.13). The address
bar's padlock means TLS is on, not that the site is trustworthy.

This server has a deliberate weakness, kept for Lesson 11.14: it builds
the file path by gluing the request's target onto `site`, so a cleverly
written request can reach files outside the `site` folder. It's only
listening on `127.0.0.1`, so nobody else can try; Lesson 11.14 has the
learner find it and fix it.
