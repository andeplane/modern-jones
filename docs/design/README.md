# Design reference

Three parts:

- **[original/](original/)**: how *Jones in the Fast Lane* (Sierra, 1990) actually works, recovered from its bytecode. Numbers, formulas, odds and the computer opponent's decision list, each tagged with the script and address it came from and a confidence level.
- **[modern-game.md](modern-game.md)**: the design for our modern game, clearly inspired by the original: same core loop, a modern city, simultaneous one-minute multiplayer weeks.
- **[economy-sim.md](economy-sim.md)**: the player-driven economy: business cycle, prices, companies, labour market, stock market, credit.

## Where the original came from

[jonesinthefastlane.com](https://jonesinthefastlane.com) serves the DOS release in the browser: an `index.html` that loads js-dos (DOSBox compiled to WebAssembly: `js-dos/js-dos.js`, `wdosbox.wasm`) and runs `bundle.jsdos`. That bundle is a 1 MB zip of the original game files (`sciv256.exe`, `resource.map`, `resource.001`, `resource.002`, drivers) plus a DOSBox config. The game is a Sierra SCI game, interpreter version 1.000.060, with an SCI0-style resource map.

Nothing from the bundle is in this repository. `.gitignore` keeps `original/`, `extracted/` and `*.jsdos` out.

## How far the decompile got

| Resource | Count | State |
|---|---|---|
| Scripts (game logic bytecode) | 85 | Fully unpacked and disassembled with object, class, property, selector, kernel and string names resolved |
| Text | 50 | Fully readable (shop greetings, headlines, weekend stories, job and course names) |
| Vocab | 14 | Selector (485) and kernel (118) name tables decoded, used by the disassembler |
| Views, pics, fonts, sounds | ~145 | Not extracted (we make our own art and audio) |

All game data that matters for design (prices, wages, requirements, odds) sits either in object properties or as constants in the code, so the disassembly gives exact numbers. The output is disassembly rather than reconstructed source; the notes in `original/` are the readable result. To redo it, see [tools/sci/README.md](../../tools/sci/README.md).

## The original in one page

- **Loop.** Each player's week is a budget of **60 time units**. Walking around a 13-building ring costs about 1 unit per 15 steps (the longest trip is about 6), entering a building costs 2, and working a shift, relaxing or attending a class costs 6. The turn ends only when time runs out.
- **Goals.** Four stats on 0..100: **wealth** (liquid assets / $100), **happiness** (an accumulator fed by purchases and events), **education** (1 + 9 × degrees) and **career** (10 × ⌊dependability / 8⌋ while employed). Each player sets four targets (10..100 in steps of 10); the first to meet all four at the start of their turn wins.
- **Economy.** A mean-reverting random walk on 8 indices; prices and wages are base × (index stretched ×5/3 around 100, floor 50%). Crashes (about 1 in 20 weeks) wipe savings or cost jobs; booms raise prices.
- **Jobs.** 37 jobs at 9 employers, $4..$25/h base. Hiring needs degrees, dependability, experience and a luck roll. Dependability decays by 3 a week, so you must keep working to keep both your job and your career score.
- **Education.** 11 courses in two trees (trade/engineering, college/academic), 10 lessons each, $50 enrollment. Books and a computer cut lessons.
- **Living.** Rent $325 (low-cost, burglaries) or $475 (security) per 4 weeks; food spoils without a fridge; clothes wear out and gate jobs; starving and illness cost time and money.
- **Money.** Bank (no interest), loans, a broker with five commodities and T-bills, a pawn shop, a lottery, muggings.
- **Computer opponent.** A 49-rule priority list: get a job, pay rent, keep food and clothes, climb the job ladder, then spend surplus on study, appliances and stocks.

See each note for the detail and the original's bugs worth not copying.
