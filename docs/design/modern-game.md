# Fuse Lane: a modern game in the spirit of Jones in the Fast Lane

Working title **Fuse Lane**, game id `fuse-lane`. It lives in [fuse-riders](https://github.com/andeplane/fuse-riders) as a new game under `games/fuse-lane`, on the same room service, WebRTC mesh, rollback netcode and accounts as the other Fuse games.

The aim is a game anyone who played the original recognises within a minute (the ring of buildings, the ticking week, the four goal stars, the deadpan shopkeepers) but which plays as a modern party game: everyone lives the same week at the same time, rounds are short, and it runs on a phone or around a TV.

Numbers below default to the original's (see [original/](original/)) unless marked **changed**. The original's bugs are fixed, not copied.

---

## 1. Core loop (kept)

- A city of **13 places on a loop road**. You walk your character between them; walking and every action cost hours from your week.
- Each week has **60 hours**. Entering a place costs 2, a work shift 6 (paid as 8 hours), a class 6, relaxing 6, a job interview 4. Walking costs about 1 hour per 15 road steps.
- **Four goals**, each 10..100 in steps of 10, chosen at setup: **Wealth** (liquid assets / $100), **Happiness**, **Education** (1 + 9 × degrees), **Career** (10 × ⌊dependability / 8⌋ while employed). Meet all four at the start of a week to win.
- Weekly upkeep: rent every 4 weeks, food every week, clothes that wear out, dependability that decays by 3 a week, an economy that drifts and sometimes crashes.

## 2. Simultaneous weeks (changed: the big one)

The original is strictly turn-based: three friends wait while one plays. Here **every player plays the same week at the same time**.

### Week structure
1. **Monday briefing** (shared, about 10 seconds, skippable when everyone taps READY). Headlines, the economy ticker, and each player's private notices: food spoiled, rent due, burglary, lottery win, pay cut. Goal check happens here.
2. **The week** (simultaneous). Everyone starts at home with 60 hours. Your clock only moves when *you* walk or act, so there is no twitch pressure inside the week, just your own budget. A shared **real-time week timer** (room setting: 90 s, 2 min default, 3 min, or off for relaxed play) keeps the party moving.
3. **Your week ends** when your hours reach 60 or you tap **CALL IT A WEEK**. Hours left unused when you call it a week, or when the timer runs out, count as rest: every 6 unused hours = one relax press (relax +3), happiness bonus included once. Finished players watch the others on the board.
4. **Weekend** (shared, a few seconds): each player's weekend story and its cost, then the next Monday.

### Making "same week" matter
Simultaneity is only interesting if players touch each other. Light, readable contention:

- **One holder per job.** Each of the 37 positions can be held by one player at a time. If a rival is the Bank Manager, the posting shows their face and is closed to you. When two players apply for the same opening in the same moment, the input log's order decides, deterministically on every device.
- **Limited deals.** MegaMart (the discount store) shows a few deals per week with shared stock ("2 left"). The resale shop's forfeited items are first come, first served.
- **Market impact.** Buying or selling a lot of one investment nudges its index a little for everyone that week.
- **Hanging out.** Two or more players relaxing at the same home, or the same café, in the same week each get an extra happiness point. Cooperation is a valid strategy.
- **Visible rivals.** Everyone's avatar walks the same board in real time and the goal thermometers are public, so you see who is about to win.

### Winning
Win check at every Monday briefing. If several players meet all goals the same week, rank by total overshoot (Σ stat − goal), then net worth, then share the win. The original's "whoever's turn came first" tie rule cannot apply. Others may play on for places, as in the original.

### Bots
Bots play the same simultaneous week. Their brain is a port of the original's 49-rule priority list (get a job, pay rent, keep food and clothes, climb jobs, then spend surplus), driven from the shared log so every device agrees. Difficulty shifts their goal targets as in the original (−10/0/+10 per goal); a **changed** "Sharp" level also lets them read the news and the job board for rivals.

## 3. The modern city

Same 13 roles, modern skins. Names are placeholders to iterate on.

| Original | Fuse Lane | Notes |
|---|---|---|
| Low-cost apartment | **Roomshare** (shared flat) | $325/4 wk. Burglary chance 1/(relax+1) per week; it is now package theft and break-ins. |
| Security apartment | **The Tower** (doorman condo) | $475/4 wk. Immune to theft. |
| Rent office | **KeyNest** (landlord office) | Pay, extensions (100/75/50/25%), wage garnishment for arrears. |
| Black's Market | **FreshCo** (grocery) | Groceries for 1/2/4 weeks, scratch cards (the lottery), news subscription. |
| Monolith Burger | **Mono Burger** drive-thru | Burgers feed you one week; **changed:** order delivery from anywhere for +50% price and 1 hour, no walking. |
| Bank + broker | **Neobank** | Savings, loans, trading. **changed:** savings earn 0.5% a week. Investments: Bonds (T-bills), Gold, Index Fund (blue chip), Tech Stocks, Commodities (pork bellies), Crypto (penny stocks, risk 10). |
| Factory | **Gigafactory** | Shift work; the biggest ladder (janitor to general manager). |
| Employment office | **Job Hub** | Postings for every employer, applications, raises. **changed:** gig work (rideshare, delivery) anywhere: $5/h, no requirements, builds no career. |
| Hi-Tech U | **City College** | Same two course trees, reskinned: Trade Cert → IoT Technician, Pre-Engineering → Engineering; Community College → Business (MBA), Liberal Arts → Grad School → PhD → Research → Publishing. $50 enrollment, 10 lessons, books and a laptop each cut one. |
| Socket City | **Gadget Garage** | Smart fridge, chest freezer, induction stove, smart TV, game console, speakers, air fryer, hot tub, laptop. Happiness on first purchase of each (the original's version of this bonus never fired; we make it work). |
| QT Clothing | **Threads** | Casual, smart casual, business: 11/13/13 weeks, gate jobs. |
| Z-Mart | **MegaMart** | Cheaper, flimsier versions (break more often), joke items that cost happiness, weekly limited deals. |
| Pawn shop | **Second Life** resale | Pawn at 40% of price paid, redeem at 50%, forfeit after 3 weeks, then sold to anyone. |

Keep the original's humour: every place has a rotating one-liner greeting and shopkeeper quips (we write our own; the originals stay in the reference only).

## 4. Fixes to the original

- The economy updates **once per week**, not once per player turn, and crash/boom odds no longer scale with player count.
- Upside price spikes can happen (the original tests the lower bound twice).
- Investment headlines actually show in the news.
- A crash wipes the whole savings balance, not its low 16 bits; better, a crash costs a percentage of savings (severity 1: 50%) rather than everything.
- Garnishment respects partial shifts. Purchases respect the clock.
- Astro Chicken's accidental multi-week stacking is either made a feature (a "meal prep" item) or removed.
- Wealth updates whenever liquid assets change, including market moves.
- Fast-food prices: the original's base values (a burger at 79 against 55 for a week of groceries) read oddly; we set our own after checking the original in play.

## 5. Presentation

- **Board:** a stylised top-down city block, the loop road around it, 13 buildings as chunky readable icons with their signs. Characters walk the road; the clock is a ring around your portrait. Phones show your own view plus rival markers; a shared TV shows the whole board, every clock and the four thermometers per player.
- **Places:** a panel slides up with the shopkeeper portrait and quip, items as large cards with price, effect and a stat-delta preview (for example "+2 ☺, 13 weeks"). Every action shows its hour cost before you tap it.
- **Monday briefing:** a newspaper/phone-feed hybrid with the headline, an economy sparkline, and your notices as cards.
- **Feel:** snappy transitions, coins and stars flying to the HUD, a satisfying stamp when a goal fills, a jingle when a rival hits a goal. Muted by default for agents (`?mute`).
- **Art:** see the art pipeline below. Style: bright flat vector with soft shading, one consistent outline weight, readable at phone size. It does not need to copy Fuse Riders' neon look, but uses the shared `fuse-ui` menus.

### Art pipeline
This environment has no image generator, and Anthropic does not offer one. Plan:
1. **First pass, shipped with the game:** hand-authored SVG generated from a script (as `scripts/generate-powerup-sprites.ts` does for Fuse Riders): buildings, character bodies in 10 colours, item icons, portraits. Crisp at any size and consistent.
2. **Raster pass when an image tool is available:** a prompt sheet (`games/fuse-lane/art/prompts.md`) with one prompt per asset, a shared style reference and exact canvas/anchor specs, so the PNGs can be generated and dropped in without code changes, the way Fuse Riders' desert prop pack was made.

## 6. Architecture on the Fuse platform

Start from Pig (`npx tsx scripts/new-game.ts fuse-lane`), which gives rooms, QR invites, shared TV, bots, rollback over the shared input log, checkpoints and accounts.

- `src/game/rules.ts`: the whole game as one pure fold per log tick. State: week, phase, per-player stats, inventories, job holders, economy indices, RNG. Inputs: `walkTo(place)`, `act(place, action, arg)`, `callItAWeek`, `ready`. Walking advances per tick so avatars move in real time; hours are charged by distance.
- Everything random (economy, events, lottery, bots) comes from the room's seeded generator in state, so every device agrees and rollback replays exactly.
- `src/game/data/`: jobs, courses, items, places and quips as typed tables. Balance lives here.
- `src/game/bot.ts`: the 49-rule planner, emitting ordinary inputs.
- `src/app/`: Phaser board scene plus DOM panels from `fuse-ui`. Renders every frame from the view.
- `src/platform.ts`: per-player stats for accounts (games played, wins, weeks to win, best net worth).

## 7. Milestones

1. **Playable core.** Board, walking, hours, the 13 places with their core actions (work, apply, study, groceries and fast food, clothes, gadgets, rent, deposit/withdraw), Monday upkeep, economy, goals and win, simultaneous weeks with the timer, simple bots. Solo, room and shared TV.
2. **Full economy and life.** Trading, loans, resale shop, lottery, theft and breakdowns, weekend stories, news, crashes and booms, job contention, full bot rules.
3. **Art and feel.** Final art pass, sound and music, animation, onboarding, balance pass from playtests.
