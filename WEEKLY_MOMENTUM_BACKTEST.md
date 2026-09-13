# Weekly Momentum Score - Backtest Report

Sample: 400 tickers from the current liquid universe, 394 with usable 9-month history. 6 as-of points, 10-trading-day holding period, -8% hard stop, top 20 ranked vs 20 random tickers as the control group.

**This backtest uses only the price/volume components (momentum-with-turnover, volume persistence, RSI(2)) - the 52-week-position, relative-strength-vs-SPY, and analyst-revision components are not included here** (the first two need per-date historical fundamentals data this project doesn't retroactively have; the third has no historical depth yet). Treat this as a partial validation of the price/volume half of the score, not the full production formula.

## Overall: scored top-N vs random-N

| Group | N trades | Win rate | Avg return | Sharpe (rough) |
|---|---|---|---|---|
| Scored top-N | 120 | 46.7% | +2.00% | 0.12 |
| Random control | 120 | 51.7% | +0.99% | 0.10 |

**Edge over random: +1.01 percentage points per 10-trading-day trade.** This is a positive sign but a single backtest run is not proof of a real edge - paper-trade forward before risking real money, per the research's explicit guidance.

## Per as-of-date detail

| As-of index | Scored N | Scored win% | Scored avg | Random N | Random win% | Random avg |
|---|---|---|---|---|---|---|
| 70 | 20 | 50% | +1.64% | 20 | 70% | +5.37% |
| 80 | 20 | 75% | +5.70% | 20 | 60% | +3.78% |
| 90 | 20 | 50% | +0.25% | 20 | 50% | +2.63% |
| 100 | 20 | 50% | +10.46% | 20 | 40% | -3.03% |
| 110 | 20 | 15% | -6.97% | 20 | 40% | -2.43% |
| 120 | 20 | 40% | +0.91% | 20 | 50% | -0.37% |
