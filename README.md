
# period data

## todo

 - [ ] predict period for next 3 months
 - [ ] distinguish 2 types of aches:
  - red: day with bodily aches
  - blue: day with mental aches
  - purple: day with both aches
 - [ ] add unit tests.
 - [ ] provide as mobile app for android (maybe use another programming language for this).

## feature ideas: symptoms to track

 - track PMS symptoms.
   - acne breakout
   - swollen or tender breasts.
   - fatigue
   - bloating or constipation
   - diarrhea
   - cramps
   - appetite changes
   - joint pain
   - muscle pain
   - mood swings
   - anxiety or depression

 - track period symptoms.
   - cramps
   - fatigue
   - water retention
   - dizziness
   - headache
   - backache
   - nausea
   - vomiting
   - pelvic pressure

 - track blood flow cycle.
   - spotting
   - blood flow (light/moderate/heavy)

## implementation ideas

### programming language

For now use python.

Later, use some language that can generate an executable on Windows systems, like rust.

 - [https://www.rust-lang.org/tools/install](rust-lang.org)
 - [https://crates.io/crates/genpdf](pdf generator package for rust)
 - [https://rust-lang-nursery.github.io/rust-cookbook/datetime/duration.html](official rust docs on datetime manipulation)
 - [https://doc.rust-lang.org/book/ch01-02-hello-world.html](official rust docs on hello world)
 - [https://www.youtube.com/watch?v=2vBQFIWl36k](Rust Testing and TDD by TensorProgramming) ... a video on tdd in rust.
 - [https://doc.rust-lang.org/book/appendix-04-useful-development-tools.html](get some rust goodies)

### predictions

Expect input like the follwoing CSV table:

```markdown
start datetime; end datetime; commment
```

With the comment having the follwing structure:

`observed-symptom@(location+or+other+tags)[strength]`

For the period being active a tag will be created:

`period@(active)[]`

Create the following output:

 - [2023-02-01] prediction: pain
 - [2023-02-10]--[2023-02-16] prediction: period.
 - [2023-02-22] prediction: moody.

### examples of symptoms

 - `blood-flow@(spotting)[]`
 - `blood-flow@(flow)[strong]`
 - `fatigue@()[]`
 - `dizziness@()[]`
 - `headache@()[]`
 - `vomiting@()[]`
 - `swollen-breasts@()[]`
 - `bloating@()[strong]`
 - `appetite@(gone)[]
 - `pain(arm muscles)[weak]
 - `mood(swings)[]

