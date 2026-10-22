# Contributing

Thanks for helping. This course is meant to be run by parents and
mentors who may not be programmers, so every contribution has to pass
one test: **could a guide with no computer experience run it from the
page?**

## Writing a lesson

- Copy [docs/LESSON-TEMPLATE.md](docs/LESSON-TEMPLATE.md) and keep its sections.
- Write exact commands, and what the learner should see after each one.
- Fill in the "If something goes wrong" table with real mistakes. Try the
  lesson yourself and note every place you stumbled.
- Write kid-facing text so a strong young reader can read it aloud. Silly
  is welcome; mean is not.
- Number lessons `N.M`, and name files `NN-short-name.md` inside the stage folder.
- Update the stage README's lesson table, and the stage's row in
  [docs/SYLLABUS.md](docs/SYLLABUS.md) if its length or prerequisites change.

## Rules for resources

- **No accounts, logins, or email addresses** for the learner. Optional online
  extras must be marked **(online, optional)**, and still need no personal account.
- **Offline first.** If a resource can be downloaded, add it to
  `scripts/mirror-library.sh`.
- **Free and open.** Paid resources may only be optional extras, marked
  **(optional purchase)**.
- Link to third-party material; never copy it into this repo.

## Labs

- Labs are Python 3 standard library, Bash, or Docker. No other dependencies.
- Every lab with a right answer needs an automated check. See
  `labs/mineshaft/test_solutions.sh`.
- The answers must never be readable by the learner's account.
