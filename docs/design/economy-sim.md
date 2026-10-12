# Fuse Lane economy simulation

The original's economy is one random walk that scales every price, plus five commodities nobody else touches. Fuse Lane replaces it with a small but living economy that **players move with their own choices**, because the game is about beating each other. Everything here runs once per week inside the deterministic rules fold, from the room's seeded generator, so every device computes the same world.

Design rules:
- **Readable cause and effect.** Every big move has a headline that explains it ("Gadget Garage sales up 30%: the Tower crowd is buying").
- **Players are real market participants.** Their spending is company revenue, their labour is company output, their trades move prices, their savings fund loans.
- **Small enough to balance.** About a dozen state variables at the macro level, eight companies, six asset classes. Tunable tables, no hidden magic.

---

## 1. Macro layer (weekly)

| State | Meaning | Model |
|---|---|---|
| `cycle` | expansion / boom / slowdown / recession | Markov chain with weekly transition odds (e.g. expansion stays 92%, → boom 4%, → slowdown 4%). Average cycle about 25–40 weeks, so a typical game sees one or two turns. |
| `growth` | weekly real growth, % | Drawn around the cycle's mean (boom +0.4, expansion +0.2, slowdown 0, recession −0.4) plus noise. |
| `inflation` | weekly inflation, % | Mean-reverting toward 0.05% a week, pushed up by booms and by **player spending** relative to the baseline, down by recessions. |
| `policyRate` | central bank rate, % per year | Taylor-style rule with a lag: `rate += 0.25 × ((inflation − target) × k1 + (growth − trend) × k2)`, clamped 0–12%. Changes are announced in the Monday briefing. |
| `unemployment` | % | Rises in slowdowns and recessions, falls in booms. Drives hiring odds and wage pressure. |
| `sentiment` | −1..1 | Smoothed growth plus headline shocks. Drives stock multiples and crypto hype. |

Crashes are no longer a separate dice roll: they are the **sharp entry into recession** (a 1-week sentiment shock, stocks −15..−35%, layoffs). Booms are the mirror image. That keeps the drama of the original's crashes but ties them to visible warning signs (rising rates, slowing sales), which rewards players who read the news.

## 2. Prices (weekly)

Each category has its own price index: **food, housing, gadgets, clothing, services (fast food, delivery), education**.

`index_c(t+1) = index_c(t) × (1 + inflation + categoryShock_c + demandPressure_c)`

- `demandPressure_c` comes from what players bought last week in that category compared with an NPC baseline. If everyone buys gadgets, gadgets get pricier; a player who shops against the herd gets bargains.
- Shop shelf price = base price × category index × shop markup (MegaMart −25% with lower durability, Gadget Garage +0%, delivery +50%).
- **Rent** follows the housing index but is **locked for a 12-week lease** when you sign. Signing at the right moment matters. Breaking a lease costs 4 weeks' rent.
- A price never moves more than ±8% in a week, so the player can plan.

## 3. Companies (the heart of the interaction)

Eight companies, one per employer place: **Gigafactory, Neobank, FreshCo, Mono Burger, Gadget Garage, Threads, MegaMart, KeyNest**. City College is public and not listed.

Each company has a sector sensitivity to the cycle, and weekly:

```
revenue   = npcBaseline × cycleFactor(sector) + Σ player spending at this company
output    = Σ shifts worked × productivity(role)           # NPC staff + players
costs     = wages paid + fixed costs
profit    = revenue − costs
health    = smoothed profit margin  (drives hiring, raises, layoffs)
```

- **Your spending is their revenue.** All the players buying gadgets make Gadget Garage healthier, which raises wages there, opens jobs and lifts its share price. KeyNest earns every rent payment.
- **Your labour is their output.** A company with many reliable players on staff runs better.
- **Jobs.** Each company has a fixed ladder of roles (the original's 37 positions, reskinned). A role can be held by one player at a time; the rest of the staff are NPCs. Healthy companies post more openings; sick ones freeze hiring and lay off, starting with the lowest-dependability staff (players included).

## 4. Labour market and salaries

- **Market wage** for a role = base × wage index of its sector × company health factor (0.8–1.25). The sector wage index follows inflation with a lag and rises when unemployment is low.
- **Offers lock at hire**, as in the original. Your wage then drifts away from the market.
- **Raise negotiation** at the Job Hub: you ask, and the company says yes when your wage is below market and your dependability clears the bar. **Changed:** you can ask for a specific amount; asking too high fails and costs dependability, asking modestly almost always works. Being underpaid while a rival holds the same job title elsewhere is a reason to job-hop.
- **Hiring** keeps the original's requirements (degrees, dependability, experience, clothing) and luck roll, but the roll's difficulty rises with unemployment and with competing applicants that week. Two players applying for the same opening in the same week: the stronger candidate wins; ties go to the earlier application in the log.
- **Performance.** Each shift adds experience and dependability as in the original; **changed:** a bonus at quarter end (every 12 weeks) of up to 2 weeks' pay, scaled by company profit and your dependability. Working for a company that your rivals make rich pays you too.
- **Gig work** is always available, pays the low end of the market and builds nothing, the safety net in a recession.

## 5. Investing and the stock market

Six asset classes, traded at Neobank (in person, or from the phone app for 1 hour and a fee):

| Asset | Price model | Character |
|---|---|---|
| **Company shares** (8) | `price = earningsPerShare × multiple(sentiment, policyRate) + noise`; pays a dividend every 12 weeks from profit | Players can own the company they work at or the shop their rivals keep using. |
| **Index fund** | Cap-weighted average of the 8 | Low risk, tracks the cycle. |
| **Bonds** | Yield = policyRate + 0.5%; price falls when rates rise | Safe income; rate hikes hurt holders. |
| **Gold** | Rises with inflation and fear (negative sentiment) | The hedge. |
| **Crypto** | High-volatility random walk with hype spikes from sentiment and headlines; risk 10 like the original's penny stocks | Lottery-like, can make or break a game. |
| **Savings account** | Weekly interest = (policyRate − 1%) / 52 | **Changed:** the original paid no interest at all. |

**Trading mechanics:**
- Buy and sell at the quoted price plus a spread (0.5% shares and index, 1% gold, 3% crypto, 0% bonds and savings).
- **Market impact.** A trade moves the price by `impact × quantity / liquidity`, decaying over the next weeks. Because everyone trades in the same week, a big buyer pushes the price up for a rival who buys later the same week. The input log's order decides who got the better fill, identically on every device.
- **No short selling** in milestone 2; optional later as an "advanced market" room setting.
- **Liquid assets for the Wealth goal** count investments at market value, so a crash can knock a player out of a winning position, and a well-timed sale can lock a goal in.

## 6. Credit

- **Loans** at Neobank: limit from wage, liquid assets and your **credit score** (late payments and garnishments lower it, on-time payments raise it). Interest = policyRate + 4% + credit spread, charged weekly.
- **Changed:** player savings fund the bank. When players hold a lot of savings, loan rates drop a little; when they all borrow, rates rise. It is a small effect, but it means the bank is shared.
- Rent arrears are garnished from wages as in the original, with the partial-shift fix.

## 7. Information as an edge

- **The news feed** (FreshCo subscription, or the phone for a small fee) prints next week's likely sector shocks with stated reliability ("Analysts expect gadget demand to cool: likely"). It is right about 70% of the time.
- **Public data** everyone sees: the policy rate, unemployment, last week's company results, the price ticker.
- **Private data**: your company's internal health (if you work there) gives an early read on layoffs and bonuses, a reason to hold a job at a company you also invest in.

## 8. Events

Random events stay (burglary, breakdowns, illness, muggings, lottery), but their odds are tied to state: breakdowns are likelier on cheap MegaMart gadgets, muggings likelier in recessions, illness likelier when relax is low. Each event names its cause in the Monday briefing.

## 9. Balancing and tooling

- All coefficients live in one typed table (`games/fuse-lane/src/game/data/economy.ts`).
- A headless simulator runs thousands of bot games per change and reports price ranges, weeks to win, how often crashes decide games and how strong each strategy is (the original's Python port in `tools/sim/econ.py` is the starting point).
- Targets: a 4-player game with default goals (50 each) ends in roughly 20–35 weeks; no single strategy (all-in crypto, pure grind, pure study) wins more than 40% of bot-vs-bot games.

## 10. Week timing (simultaneous play)

- Each week gives every player **60 game hours to spend in about 60 real seconds**. Everyone plays at once, so a week takes one minute regardless of player count (room setting: 45 / 60 / 90 seconds).
- Game hours only move when you walk or act. The real-time limit is what keeps the pressure on: plan fast or lose the week.
- When the minute ends, **unspent hours count as sleep**: every 6 unused hours is one relax press (relax +3), so a short week is not wasted, just less productive. Finishing early ("call it a week") works the same way.
- Walking is quick in real time (a full lap of the road in about 4 seconds) so the minute is spent deciding, not watching.
