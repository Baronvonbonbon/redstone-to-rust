# Lesson 10.4: Whose Turn Is It? Scheduling

**Time:** 2–3 sessions of 45 min · **You need:** a terminal; a text
editor; squared paper and three coloured pencils; `~/lab/os` · **New
words:** scheduler, FIFO, shortest job first, round robin, turnaround
time, response time, average

## Goal *(read this to the learner)*

> There's one CPU and lots of programs that want it. The part of the
> kernel that decides who goes next is the **scheduler**. You'll try
> three ways of choosing, on paper first, then with a simulator you
> write in Rust, and measure which is fairest with a bit of maths.

## Before the lesson *(guide, 10 min)*

- [ ] Read this whole lesson once.
- [ ] Squared paper, and pencils in three colours (A, B and C).

## Warm-up (5 min)

"Three people are queuing for the one swing. A wants it for 20 minutes,
B and C for 5 each. A got there first. Is it fair if A goes first?"
Let them argue. "Today we'll measure it."

## Activity

### Session 1: on paper

1. **Jobs and ticks.** **Say:** "Each program that wants the CPU is a
   **job**. Time is in **ticks**. Job A needs 20 ticks, B needs 5, and C
   needs 5. They all arrive at tick 0." Write that at the top of the
   paper.

2. **FIFO.** **Say:** "The simplest rule is **FIFO**: first in, first
   out, like a queue at a shop. A arrived first." On a row of squares,
   colour 20 squares A, then 5 B, then 5 C. **Say:** "A job's
   **turnaround time** is how long from arriving until it's finished:
   here, the number of the square where it ends." Write them down:
   *(A: 20, B: 25, C: 30.)*

   **Say:** "The **average** is all of them added up, divided by how
   many there are." **Ask:** "What's the average turnaround?" *((20 + 25
   + 30) ÷ 3 = 75 ÷ 3 = 25.)*

3. **Shortest job first.** **Ask:** "What if the short jobs go first?"
   Colour a new row: 5 B, 5 C, then 20 A. Work out the turnarounds and
   the average together. *(B: 5, C: 10, A: 30. 45 ÷ 3 = 15.)* **Say:**
   "Much better on average! That's **shortest job first**."

4. **Round robin.** **Say:** "But what if you're A, typing in a game,
   and the game has to wait 10 ticks before it gets *any* go? Another
   time we measure is **response time**: how long until a job first
   gets a turn." Colour a new row: one tick each, A, B, C, A, B, C... and
   when B and C are finished, A has the rest. **Say:** "That's **round
   robin**: everyone gets a slice, in turn, like passing the pencil in
   Lesson 10.1." Work out each job's response time on all three rows
   (the square *before* its first one: A's response in FIFO is 0).
   **Ask:** "Which rule has the best response time?" *(Round robin: 0, 1
   and 2.)*

### Session 2: the simulator

5. **Write it.**
   ```
   cd ~/lab/os
   cargo new scheduler
   cd scheduler
   ```
   Type the job, and FIFO:
   ```rust
   /// A job for the CPU: a letter for its name, and how many ticks it needs.
   #[derive(Clone, Copy)]
   struct Job {
       name: char,
       length: usize,
   }

   /// Makes a job.
   fn job(name: char, length: usize) -> Job {
       Job { name, length }
   }

   /// First In, First Out: each job runs to the end, in the order it came.
   fn fifo(jobs: &[Job]) -> String {
       let mut timeline = String::new();
       for job in jobs {
           for _ in 0..job.length {
               timeline.push(job.name);
           }
       }
       timeline
   }
   ```
   **Say:** "`job('A', 20)` will be a short way to make a job. The
   **timeline** is a string with one letter for each tick: the job that
   had the CPU then. It's your coloured row of squares."

6. **Measuring.** Add `report`:
   ```rust
   /// Prints the timeline, then each job's turnaround and response times, and the averages.
   fn report(title: &str, timeline: &str, jobs: &[Job]) {
       println!("{title}");
       println!("  {timeline}");
       let mut total_turnaround = 0;
       let mut total_response = 0;
       for job in jobs {
           let name = job.name;
           let turnaround = timeline.rfind(name).unwrap() + 1;
           let response = timeline.find(name).unwrap();
           println!("  {name}: turnaround {turnaround}, response {response}");
           total_turnaround += turnaround;
           total_response += response;
       }
       let count = jobs.len() as f64;
       println!(
           "  Average turnaround {:.1}, average response {:.1}",
           total_turnaround as f64 / count,
           total_response as f64 / count
       );
       println!();
   }
   ```
   **Say:** "`find` gives the place of the *first* A in the string, and
   `rfind` the *last*, counting from 0. **Ask:** "Why `+ 1` for the
   turnaround?" *(If A's last tick is square 19, counting from 0, it
   has finished at the end of tick 20.)* "`{:.1}` prints one digit after
   the point."

   And `main`:
   ```rust
   fn main() {
       let jobs = [job('A', 20), job('B', 5), job('C', 5)];
       report("FIFO", &fifo(&jobs), &jobs);
   }
   ```
   `cargo run`. **They should see:**
   ```
   FIFO
     AAAAAAAAAAAAAAAAAAAABBBBBCCCCC
     A: turnaround 20, response 0
     B: turnaround 25, response 20
     C: turnaround 30, response 25
     Average turnaround 25.0, average response 15.0
   ```
   Check it against the paper. Commit.

7. **Shortest job first.** Add, after `fifo`:
   ```rust
   /// Shortest Job First: like FIFO, but the shortest jobs go first.
   fn sjf(jobs: &[Job]) -> String {
       let mut sorted = jobs.to_vec();
       sorted.sort_by_key(|job| job.length);
       fifo(&sorted)
   }
   ```
   and in `main`: `report("Shortest Job First", &sjf(&jobs), &jobs);`.
   **Say:** "Sort the jobs by length, then it's just FIFO." **They
   should see:**
   ```
   Shortest Job First
     BBBBBCCCCCAAAAAAAAAAAAAAAAAAAA
     A: turnaround 30, response 10
     B: turnaround 5, response 0
     C: turnaround 10, response 5
     Average turnaround 15.0, average response 5.0
   ```

### Session 3: round robin

8. **Taking turns.** Add:
   ```rust
   /// Round Robin: each job runs for one slice, then goes to the back of the line.
   fn round_robin(jobs: &[Job], slice: usize) -> String {
       let mut timeline = String::new();
       let mut left: Vec<usize> = jobs.iter().map(|job| job.length).collect();
       while left.iter().any(|&ticks| ticks > 0) {
           for (i, job) in jobs.iter().enumerate() {
               let run = left[i].min(slice);
               for _ in 0..run {
                   timeline.push(job.name);
               }
               left[i] -= run;
           }
       }
       timeline
   }
   ```
   and in `main`: `report("Round Robin, slice 1", &round_robin(&jobs, 1),
   &jobs);`. **Say:** "`left` is how many ticks each job still needs.
   Each time round, every job runs for one slice, or less if it needs
   less. When nothing's left, we stop." **They should see:**
   ```
   Round Robin, slice 1
     ABCABCABCABCABCAAAAAAAAAAAAAAA
     A: turnaround 30, response 0
     B: turnaround 14, response 1
     C: turnaround 15, response 2
     Average turnaround 19.7, average response 1.0
   ```
   **Ask:** "Which rule is best?" *(It depends what you want: shortest
   job first has the best turnaround, round robin the best response.
   That's why real schedulers mix them.)*

9. **Experiments.** Try `round_robin(&jobs, 5)` and `round_robin(&jobs,
   100)` (change the title too). With a slice of 5, **they should see**
   `AAAAABBBBBCCCCCAAAAAAAAAAAAAAA`. **Ask:** "What does a huge slice turn into?" *(FIFO: every job
   finishes in its first slice.)* Then try three jobs all of length 10
   with FIFO and round robin. Commit.

## If something goes wrong

| What you see | What it means | What to do |
|---|---|---|
| `error[E0277]: the trait bound \`Job: Clone\` is not satisfied` | `to_vec` copies the jobs, so `Job` must be copyable | Keep `#[derive(Clone, Copy)]` above the struct. |
| `called \`Option::unwrap()\` on a \`None\` value` in `report` | A job never appears in the timeline: its length is 0 | Give every job at least 1 tick. |
| Round robin never stops | `left[i] -= run;` is missing, so nothing goes down | Add it. |
| `error[E0277]: cannot divide \`usize\` by \`f64\`` | Dividing a whole number by a decimal | Turn the whole number into `f64` first: `total_turnaround as f64 / count`. |
| The averages differ from the paper | A sum on paper, or a typing mistake in the jobs | Check each turnaround line first. |

## Talk about it

- What does a scheduler do?
- What's turnaround time? Response time? How do you work out an
  average?
- Why is shortest job first good for turnaround, but bad for a game?
- Why can't a real kernel do shortest job first exactly? *(It doesn't
  know how long a program will take!)*

## Challenge *(if there's time, or for next time)*

- Add a fourth job, `job('D', 1)`. Predict each average first, then
  check.
- With three jobs of lengths x, 5 and 5 under FIFO, the average
  turnaround is (x + (x + 5) + (x + 10)) ÷ 3 = x + 5. Check it with the
  simulator for x = 20 and x = 50. What does it become with shortest
  job first, if x is the biggest? *(Work it out on paper, then test it.)*
- Write `lottery(jobs, seed)`: each tick, a random job that still needs
  time gets it. (Real schedulers have done this! It's called **lottery
  scheduling**.)

## Checkpoint

The learner can, without help:
- [ ] Draw FIFO, shortest job first and round robin on squared paper
- [ ] Work out turnaround and response times, and their averages
- [ ] Explain the scheduler simulator's three functions
- [ ] Say which rule is best for what, and why

## Lab notebook

Stick in the three coloured rows. Write the table of averages. Write
which rule you'd want for a game, and which for a computer that does
long jobs overnight. Commit. Add *scheduler*, *FIFO*, *round robin*,
*turnaround time*, *response time* and *average* to `dictionary.md`.

## Guide's background *(optional reading)*

This follows OSTEP Chapter 7, "Scheduling: Introduction", and uses the
same measures. Shortest job first is provably the best order for
average turnaround when all jobs arrive together, and round robin has
the best response time; real schedulers try to get both. OSTEP Chapter 8
describes the **multi-level feedback queue**, which guesses which
programs are interactive by watching how they behave.

Linux's scheduler since version 6.6 is called **EEVDF** ("earliest
eligible virtual deadline first"): every runnable process gets a fair
share, and the ones that have had less than their share go first. The
kernel switches about every few milliseconds, interrupted by a hardware
timer.

The challenge's algebra (average turnaround x + 5) is the stage's maths
gate: linear expressions, and checking them by trying numbers.
