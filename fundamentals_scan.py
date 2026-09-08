"""
FUNDAMENTALS SCAN - Short Interest + Fundamentals (Beta/PE) + Technicals (RSI/MA)
for every ticker, feeding the composite Score (1-10) column.

Pure HTTP (requests + ThreadPoolExecutor), no browser - same class of method as
insider_scan.py. Two Yahoo Finance endpoints per ticker:
  - quoteSummary (defaultKeyStatistics + summaryDetail): shortPercentOfFloat,
    beta, trailingPE
  - chart (daily closes, 1y): used locally to compute RSI(14) and the 50/200-day
    moving averages - Yahoo's own page doesn't expose these as raw numbers
    anywhere, only as a chart, so they're computed here instead of scraped.

quoteSummary requires a crumb+cookie handshake (Yahoo locked it down after this
project's earlier scripts were written) - fetched ONCE at startup, then reused
as plain (cookies dict, crumb string) values passed into each thread's own
request. Session objects are NOT shared across threads (avoids any thread-safety
question); the immutable cookies/crumb values are safe to share since they're
never mutated after the handshake.

Run: python fundamentals_scan.py
Progress:  FUNDAMENTALS_SCAN_LOG.md
Result:    FUNDAMENTALS_SCAN_RESULTS.md, fundamentals_data.tsv
           (TICKER, shortPctFloat, beta, trailingPE, rsi14, price, ma50, ma200,
           marketCap, marketCapFmt, volumeRatio, priceChangePct, peg, range52Pos,
           debtToEquity, shortRatio, earningsSurpriseAvg, epsTrendPct,
           profitMargins, revenueGrowth, ratingTrendDelta, returnOnEquity,
           currentRatio, institutionalOwnership, quickRatio, returnOnAssets,
           grossMargins, operatingMargins, fcfYield, heldPctInsiders,
           numAnalystOpinions, forwardPE, priceToBook, evToEbitda, payoutRatio,
           epsGrowth5y, relativeStrength52w, shortInterestTrendPct, evToRevenue,
           ebitdaMargins, cashToMcap, ocfMargin, earningsQuarterlyGrowth,
           epsGrowthNextYear, floatPct)

Also resolves eToro-style exchange suffixes that don't match Yahoo's own
convention (e.g. .ASX -> .AX, .HK's 5-digit codes -> 4-digit) before giving up
on a ticker - see yahoo_symbol_candidates()/resolve_yahoo_symbol() - found
2026-09-06 after noticing "no data" tickers were almost entirely one of these
mismatched-suffix exchanges, not genuinely missing from Yahoo.
"""

import concurrent.futures
import glob
import json
import time
from pathlib import Path

import requests

ROOT = Path(__file__).parent
HEADERS = {"User-Agent": "Mozilla/5.0 (eToroStockTracker research contact@example.com)"}
WORKERS = 8
LOG_EVERY = 100


def load_all_tickers():
    tickers = []
    files = sorted(f for f in glob.glob(str(ROOT / "analyst_targets_*.txt")) if "_OLD" not in f)
    for fname in files:
        for line in Path(fname).read_text(encoding="utf-8").split("\n"):
            if not line.strip():
                continue
            parts = line.split("\t")
            if len(parts) != 8:
                continue
            tickers.append(parts[0])
    return tickers


def get_crumb():
    s = requests.Session()
    s.headers.update(HEADERS)
    s.get("https://fc.yahoo.com", timeout=15)
    crumb = s.get("https://query1.finance.yahoo.com/v1/test/getcrumb", timeout=15).text
    return s.cookies.get_dict(), crumb


def compute_rsi14(closes):
    """Standard 14-period RSI (Wilder smoothing) from a list of daily closes,
    oldest first. Returns None if there isn't enough history."""
    if len(closes) < 15:
        return None
    gains, losses = [], []
    for i in range(1, len(closes)):
        diff = closes[i] - closes[i - 1]
        gains.append(max(diff, 0))
        losses.append(max(-diff, 0))
    avg_gain = sum(gains[:14]) / 14
    avg_loss = sum(losses[:14]) / 14
    for i in range(14, len(gains)):
        avg_gain = (avg_gain * 13 + gains[i]) / 14
        avg_loss = (avg_loss * 13 + losses[i]) / 14
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def yahoo_symbol_candidates(ticker):
    """eToro's exchange suffixes often don't match Yahoo Finance's own
    convention (e.g. eToro's .ASX vs Yahoo's .AX), which used to make every
    ticker on those exchanges silently fall into "no data". Returns the
    original ticker first, then known Yahoo-equivalent rewrites to try if it
    fails - checked empirically against real examples from the no-data list."""
    if "." not in ticker:
        return [ticker]
    base, suffix = ticker.rsplit(".", 1)
    candidates = [ticker]
    if suffix == "ASX":
        candidates.append(f"{base}.AX")
    elif suffix in ("US", "EUR", "24-7"):
        # .EUR/.24-7 are eToro's own alternate-venue/currency listings of an
        # otherwise-ordinary US stock (e.g. AAPL.EUR, AMZN.24-7) - not a
        # separate Yahoo-listed security, so the bare ticker is the fix.
        candidates.append(base)
    elif suffix == "ZU":
        candidates.append(f"{base}.SW")
    elif suffix == "NV":
        candidates.append(f"{base}.AS")
    elif suffix == "HK":
        digits = base.lstrip("0") or "0"
        candidates.append(f"{digits.zfill(4)}.HK")
    elif suffix in ("ST", "CO") and len(base) > 1 and base[-1].isalpha():
        candidates.append(f"{base[:-1]}-{base[-1].upper()}.{suffix}")
    return candidates


def resolve_yahoo_symbol(ticker):
    """Try each candidate symbol's chart endpoint until one returns real data;
    fall back to the original ticker (so the caller still gets a clean
    no-data result) if none do. Only probes candidates when the ticker's
    suffix is one of the known eToro/Yahoo mismatches - otherwise returns the
    ticker unchanged with no extra request, so the ~5500 tickers that already
    work aren't slowed down."""
    candidates = yahoo_symbol_candidates(ticker)
    if len(candidates) == 1:
        return ticker
    for candidate in candidates:
        try:
            r = requests.get(
                f"https://query1.finance.yahoo.com/v8/finance/chart/{candidate}",
                params={"range": "5d", "interval": "1d"}, headers=HEADERS, timeout=15,
            )
            if r.status_code != 200:
                continue
            result = r.json().get("chart", {}).get("result")
            # A malformed symbol can still get a 200 with a "result" shell but
            # null closes (seen on 00002.HK, WALLb.ST) - only a real close
            # price counts as confirmation this candidate is a valid symbol.
            if result and any(c is not None for c in (result[0]["indicators"]["quote"][0].get("close") or [])):
                return candidate
        except Exception:
            continue
    return ticker


def scan_one(ticker, cookies, crumb, results, log_state):
    try:
        symbol = resolve_yahoo_symbol(ticker)
        qs = requests.get(
            f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{symbol}",
            params={
                "modules": (
                    "defaultKeyStatistics,summaryDetail,financialData,"
                    "earningsHistory,earningsTrend,recommendationTrend,assetProfile"
                ),
                "crumb": crumb,
            },
            cookies=cookies, headers=HEADERS, timeout=15,
        )
        short_pct, beta, pe, market_cap, market_cap_fmt = None, None, None, None, None
        peg, week52_high, week52_low = None, None, None
        debt_to_equity, short_ratio, earnings_surprise_avg, eps_trend_pct = None, None, None, None
        profit_margins, revenue_growth, rating_trend_delta = None, None, None
        sector, industry = None, None
        quick_ratio, return_on_assets, gross_margins, operating_margins = None, None, None, None
        free_cash_flow, held_pct_insiders, num_analyst_opinions, forward_pe = None, None, None, None
        price_to_book, ev_to_ebitda, payout_ratio, eps_growth_5y = None, None, None, None
        change_52week, sandp_52week_change, shares_short, shares_short_prior = None, None, None, None
        ev_to_revenue, ebitda_margins, total_cash, operating_cashflow = None, None, None, None
        total_revenue, earnings_quarterly_growth, float_shares, shares_outstanding = None, None, None, None
        eps_growth_next_year = None
        if qs.status_code == 200:
            result = qs.json().get("quoteSummary", {}).get("result")
            if result:
                dks = result[0].get("defaultKeyStatistics", {}) or {}
                sd = result[0].get("summaryDetail", {}) or {}
                fd = result[0].get("financialData", {}) or {}
                eh = result[0].get("earningsHistory", {}) or {}
                et = result[0].get("earningsTrend", {}) or {}
                rt = result[0].get("recommendationTrend", {}) or {}
                ap = result[0].get("assetProfile", {}) or {}
                sector = ap.get("sector")
                industry = ap.get("industry")
                short_pct = (dks.get("shortPercentOfFloat") or {}).get("raw")
                beta = (sd.get("beta") or dks.get("beta") or {}).get("raw")
                pe = (sd.get("trailingPE") or {}).get("raw")
                mcap_field = sd.get("marketCap") or {}
                market_cap = mcap_field.get("raw")
                market_cap_fmt = mcap_field.get("fmt")
                peg = (dks.get("pegRatio") or {}).get("raw")
                week52_high = (sd.get("fiftyTwoWeekHigh") or {}).get("raw")
                week52_low = (sd.get("fiftyTwoWeekLow") or {}).get("raw")
                debt_to_equity = (fd.get("debtToEquity") or {}).get("raw")
                short_ratio = (dks.get("shortRatio") or {}).get("raw")
                profit_margins = fd.get("profitMargins", {}).get("raw") if fd.get("profitMargins") else None
                revenue_growth = fd.get("revenueGrowth", {}).get("raw") if fd.get("revenueGrowth") else None
                return_on_equity = fd.get("returnOnEquity", {}).get("raw") if fd.get("returnOnEquity") else None
                current_ratio = fd.get("currentRatio", {}).get("raw") if fd.get("currentRatio") else None
                institutional_ownership = (dks.get("heldPercentInstitutions") or {}).get("raw")
                quick_ratio = (fd.get("quickRatio") or {}).get("raw")
                return_on_assets = (fd.get("returnOnAssets") or {}).get("raw")
                gross_margins = (fd.get("grossMargins") or {}).get("raw")
                operating_margins = (fd.get("operatingMargins") or {}).get("raw")
                free_cash_flow = (fd.get("freeCashflow") or {}).get("raw")
                num_analyst_opinions = (fd.get("numberOfAnalystOpinions") or {}).get("raw")
                ev_to_revenue = (dks.get("enterpriseToRevenue") or {}).get("raw")
                ebitda_margins = (fd.get("ebitdaMargins") or {}).get("raw")
                total_cash = (fd.get("totalCash") or {}).get("raw")
                operating_cashflow = (fd.get("operatingCashflow") or {}).get("raw")
                total_revenue = (fd.get("totalRevenue") or {}).get("raw")
                earnings_quarterly_growth = (dks.get("earningsQuarterlyGrowth") or {}).get("raw")
                float_shares = (dks.get("floatShares") or {}).get("raw")
                shares_outstanding = (dks.get("sharesOutstanding") or {}).get("raw")
                held_pct_insiders = (dks.get("heldPercentInsiders") or {}).get("raw")
                # forwardPE lives under defaultKeyStatistics on most tickers, but
                # falls back to summaryDetail on some - same fallback pattern as beta.
                forward_pe = (dks.get("forwardPE") or sd.get("forwardPE") or {}).get("raw")
                price_to_book = (dks.get("priceToBook") or {}).get("raw")
                ev_to_ebitda = (dks.get("enterpriseToEbitda") or {}).get("raw")
                payout_ratio = (sd.get("payoutRatio") or {}).get("raw")
                change_52week = (dks.get("52WeekChange") or {}).get("raw")
                sandp_52week_change = (dks.get("SandP52WeekChange") or {}).get("raw")
                shares_short = (dks.get("sharesShort") or {}).get("raw")
                shares_short_prior = (dks.get("sharesShortPriorMonth") or {}).get("raw")

                for t in (et.get("trend") or []):
                    period = t.get("period")
                    if period == "+5y":
                        eps_growth_5y = (t.get("growth") or {}).get("raw")
                    elif period == "+1y":
                        eps_growth_next_year = (t.get("growth") or {}).get("raw")

                surprises = [
                    (h.get("surprisePercent") or {}).get("raw")
                    for h in (eh.get("history") or [])
                ]
                surprises = [s for s in surprises if s is not None]
                if surprises:
                    earnings_surprise_avg = sum(surprises) / len(surprises) * 100

                for t in (et.get("trend") or []):
                    if t.get("period") == "0q":
                        eps_trend = t.get("epsTrend") or {}
                        current = (eps_trend.get("current") or {}).get("raw")
                        ago90 = (eps_trend.get("90daysAgo") or {}).get("raw")
                        if current is not None and ago90:
                            eps_trend_pct = (current - ago90) / abs(ago90) * 100
                        break

                def avg_rating(period_row):
                    """Weighted average of the analyst headcount buckets, on a
                    1 (Strong Sell) to 5 (Strong Buy) scale."""
                    weights = {"strongBuy": 5, "buy": 4, "hold": 3, "sell": 2, "strongSell": 1}
                    total_n = sum(period_row.get(k) or 0 for k in weights)
                    if not total_n:
                        return None
                    return sum((period_row.get(k) or 0) * w for k, w in weights.items()) / total_n

                trend_rows = {row.get("period"): row for row in (rt.get("trend") or [])}
                now_avg = avg_rating(trend_rows["0m"]) if "0m" in trend_rows else None
                ago_avg = avg_rating(trend_rows["-3m"]) if "-3m" in trend_rows else None
                if now_avg is not None and ago_avg is not None:
                    rating_trend_delta = now_avg - ago_avg

        chart = requests.get(
            f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}",
            params={"range": "1y", "interval": "1d"}, headers=HEADERS, timeout=15,
        )
        rsi14, price, ma50, ma200, volume_ratio, price_change_pct = None, None, None, None, None, None
        if chart.status_code == 200:
            chart_result = chart.json().get("chart", {}).get("result")
            if chart_result:
                quote = chart_result[0]["indicators"]["quote"][0]
                closes = quote.get("close") or []
                closes = [c for c in closes if c is not None]
                if closes:
                    price = closes[-1]
                    rsi14 = compute_rsi14(closes)
                    if len(closes) >= 50:
                        ma50 = sum(closes[-50:]) / 50
                    if len(closes) >= 200:
                        ma200 = sum(closes[-200:]) / 200
                    if len(closes) >= 2:
                        prev_close = closes[-2]
                        if prev_close:
                            price_change_pct = (closes[-1] - prev_close) / prev_close * 100
                volumes = [v for v in (quote.get("volume") or []) if v is not None]
                if len(volumes) >= 2:
                    today_volume = volumes[-1]
                    baseline = volumes[-31:-1] if len(volumes) >= 31 else volumes[:-1]
                    avg_volume = sum(baseline) / len(baseline) if baseline else None
                    if avg_volume:
                        volume_ratio = today_volume / avg_volume

        range52_pos = None
        ref_price = price if price is not None else None
        if ref_price is not None and week52_high is not None and week52_low is not None and week52_high > week52_low:
            range52_pos = (ref_price - week52_low) / (week52_high - week52_low) * 100

        # FCF Yield (%) - free cash flow as a % of market cap, the standard
        # way to compare cash generation across companies of different sizes
        # (a raw FCF dollar figure alone isn't comparable between a $10B and
        # a $500B company).
        fcf_yield = None
        if free_cash_flow is not None and market_cap:
            fcf_yield = free_cash_flow / market_cap * 100

        # Relative strength (pct points) - the stock's own 52-week % change
        # minus the S&P 500's over the same window, so "this stock is up 15%"
        # reads very differently depending on whether the market as a whole
        # was up 5% (real outperformance) or up 25% (actually lagging).
        relative_strength_52w = None
        if change_52week is not None and sandp_52week_change is not None:
            relative_strength_52w = (change_52week - sandp_52week_change) * 100

        # Short interest trend (%) - whether the raw short-share count grew or
        # shrank vs. a month ago, distinct from the STATIC short-interest-%
        # level already used elsewhere (a rising trend is a bearish-sentiment
        # signal even if the absolute level is still low).
        short_interest_trend_pct = None
        if shares_short is not None and shares_short_prior:
            short_interest_trend_pct = (shares_short - shares_short_prior) / shares_short_prior * 100

        # Cash cushion (%) - total cash relative to market cap, a balance-sheet
        # safety-margin signal distinct from FCF Yield (which measures ongoing
        # generation, not the stockpile already on hand).
        cash_to_mcap = None
        if total_cash is not None and market_cap:
            cash_to_mcap = total_cash / market_cap * 100

        # Operating cash flow margin (%) - operating cash flow / revenue, a
        # cash-quality check distinct from FCF Yield (which nets out capex)
        # and from Profit Margin (which is accounting profit, not cash).
        ocf_margin = None
        if operating_cashflow is not None and total_revenue:
            ocf_margin = operating_cashflow / total_revenue * 100

        # Public float (%) - how much of the company's shares are actually
        # freely tradeable vs. locked up (insiders/institutions/restricted).
        # A small float means the same dollar of buying/selling pressure
        # moves the price much more - a liquidity/volatility risk factor,
        # not a quality signal.
        float_pct = None
        if float_shares is not None and shares_outstanding:
            float_pct = float_shares / shares_outstanding * 100

        if short_pct is None and beta is None and pe is None and rsi14 is None and market_cap is None:
            results["no_data"].append(ticker)
        else:
            results["data"][ticker] = {
                "short_pct": short_pct, "beta": beta, "pe": pe,
                "rsi14": rsi14, "price": price, "ma50": ma50, "ma200": ma200,
                "market_cap": market_cap, "market_cap_fmt": market_cap_fmt,
                "volume_ratio": volume_ratio, "price_change_pct": price_change_pct,
                "peg": peg, "range52_pos": range52_pos,
                "debt_to_equity": debt_to_equity, "short_ratio": short_ratio,
                "earnings_surprise_avg": earnings_surprise_avg, "eps_trend_pct": eps_trend_pct,
                "profit_margins": profit_margins, "revenue_growth": revenue_growth,
                "rating_trend_delta": rating_trend_delta,
                "sector": sector, "industry": industry,
                "return_on_equity": return_on_equity, "current_ratio": current_ratio,
                "institutional_ownership": institutional_ownership,
                "quick_ratio": quick_ratio, "return_on_assets": return_on_assets,
                "gross_margins": gross_margins, "operating_margins": operating_margins,
                "fcf_yield": fcf_yield, "held_pct_insiders": held_pct_insiders,
                "num_analyst_opinions": num_analyst_opinions, "forward_pe": forward_pe,
                "price_to_book": price_to_book, "ev_to_ebitda": ev_to_ebitda,
                "payout_ratio": payout_ratio, "eps_growth_5y": eps_growth_5y,
                "relative_strength_52w": relative_strength_52w,
                "short_interest_trend_pct": short_interest_trend_pct,
                "ev_to_revenue": ev_to_revenue, "ebitda_margins": ebitda_margins,
                "cash_to_mcap": cash_to_mcap, "ocf_margin": ocf_margin,
                "earnings_quarterly_growth": earnings_quarterly_growth,
                "eps_growth_next_year": eps_growth_next_year, "float_pct": float_pct,
            }
            results["updated"].append(ticker)
    except Exception:
        results["errors"].append(ticker)
    finally:
        log_state["done"] += 1
        if log_state["done"] % LOG_EVERY == 0:
            write_progress_log(log_state, results)
            write_data_file(results)
            write_sector_file(results)


def write_progress_log(log_state, results):
    elapsed = time.time() - log_state["start"]
    rate = log_state["done"] / elapsed if elapsed > 0 else 0
    remaining = (log_state["total"] - log_state["done"]) / rate if rate > 0 else 0
    with open(ROOT / "FUNDAMENTALS_SCAN_LOG.md", "w", encoding="utf-8") as f:
        f.write("# FUNDAMENTALS SCAN progress\n\n")
        f.write(f"Done: {log_state['done']} / {log_state['total']}\n\n")
        f.write(f"Elapsed: {elapsed/60:.1f} min | Rate: {rate:.2f}/s | ETA: {remaining/60:.1f} min\n\n")
        f.write(f"Updated: {len(results['updated'])}\n")
        f.write(f"No data: {len(results['no_data'])}\n")
        f.write(f"Errors: {len(results['errors'])}\n")


def write_data_file(results):
    with open(ROOT / "fundamentals_data.tsv", "w", encoding="utf-8") as f:
        for ticker, d in results["data"].items():
            f.write(
                f"{ticker}\t{d['short_pct']}\t{d['beta']}\t{d['pe']}\t"
                f"{d['rsi14']}\t{d['price']}\t{d['ma50']}\t{d['ma200']}\t"
                f"{d['market_cap']}\t{d['market_cap_fmt']}\t"
                f"{d['volume_ratio']}\t{d['price_change_pct']}\t"
                f"{d['peg']}\t{d['range52_pos']}\t"
                f"{d['debt_to_equity']}\t{d['short_ratio']}\t"
                f"{d['earnings_surprise_avg']}\t{d['eps_trend_pct']}\t"
                f"{d['profit_margins']}\t{d['revenue_growth']}\t{d['rating_trend_delta']}\t"
                f"{d['return_on_equity']}\t{d['current_ratio']}\t{d['institutional_ownership']}\t"
                f"{d['quick_ratio']}\t{d['return_on_assets']}\t{d['gross_margins']}\t"
                f"{d['operating_margins']}\t{d['fcf_yield']}\t{d['held_pct_insiders']}\t"
                f"{d['num_analyst_opinions']}\t{d['forward_pe']}\t"
                f"{d['price_to_book']}\t{d['ev_to_ebitda']}\t{d['payout_ratio']}\t"
                f"{d['eps_growth_5y']}\t{d['relative_strength_52w']}\t{d['short_interest_trend_pct']}\t"
                f"{d['ev_to_revenue']}\t{d['ebitda_margins']}\t{d['cash_to_mcap']}\t"
                f"{d['ocf_margin']}\t{d['earnings_quarterly_growth']}\t{d['eps_growth_next_year']}\t"
                f"{d['float_pct']}\n"
            )


def write_sector_file(results):
    """Kept as its own file (not appended to fundamentals_data.tsv) so that
    file's field count - and every one of its readers' `len(parts) != N`
    check - doesn't need to grow again for two purely categorical strings
    that no score formula uses as a number."""
    with open(ROOT / "sector_data.tsv", "w", encoding="utf-8") as f:
        for ticker, d in results["data"].items():
            sector = d.get("sector") or ""
            industry = d.get("industry") or ""
            f.write(f"{ticker}\t{sector}\t{industry}\n")


def write_shard_output(shard_index, results):
    """Parallel cloud mode (SHARD_COUNT > 1): each shard only scans its own
    slice of tickers and can't safely rewrite fundamentals_data.tsv itself
    (concurrent shards would clobber each other's results) - it drops its
    results as JSON for aggregate_scan_shards.py to combine once every shard
    is done."""
    out_dir = ROOT / "shard_out"
    out_dir.mkdir(exist_ok=True)
    payload = {
        "data": results["data"], "updated": results["updated"],
        "no_data": results["no_data"], "errors": results["errors"],
    }
    with open(out_dir / f"fundamentals_shard{shard_index}.json", "w", encoding="utf-8") as f:
        json.dump(payload, f)


def main():
    tickers = load_all_tickers()
    import os
    limit = os.environ.get("FUNDAMENTALS_SCAN_LIMIT")
    if limit:
        tickers = tickers[: int(limit)]

    # Parallel cloud mode: SHARD_COUNT > 1 means this is one of several
    # concurrent GitHub Actions jobs each covering a slice of the full
    # universe. A stride (not contiguous chunks) spreads any clustering in
    # the source order evenly across shards.
    shard_index = int(os.environ.get("SHARD_INDEX", "0"))
    shard_count = int(os.environ.get("SHARD_COUNT", "1"))
    if shard_count > 1:
        tickers = tickers[shard_index::shard_count]
        print(f"Shard {shard_index}/{shard_count}: {len(tickers)} tickers assigned")
    print(f"Loaded {len(tickers)} tickers")

    print("Getting Yahoo crumb/cookie...")
    cookies, crumb = get_crumb()

    results = {"updated": [], "no_data": [], "errors": [], "data": {}}
    log_state = {"done": 0, "total": len(tickers), "start": time.time()}

    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futures = [ex.submit(scan_one, t, cookies, crumb, results, log_state) for t in tickers]
        concurrent.futures.wait(futures)

    write_progress_log(log_state, results)

    if shard_count > 1:
        write_shard_output(shard_index, results)
        print(f"Shard {shard_index} complete - wrote shard_out/fundamentals_shard{shard_index}.json "
              "(aggregate_scan_shards.py combines all shards and runs the score/site pipeline once every shard is done).")
        return

    write_data_file(results)
    write_sector_file(results)

    with open(ROOT / "FUNDAMENTALS_SCAN_RESULTS.md", "w", encoding="utf-8") as f:
        f.write("# FUNDAMENTALS SCAN Results\n\n")
        f.write(f"Total: {len(tickers)} | Updated: {len(results['updated'])} | "
                f"No data: {len(results['no_data'])} | Errors: {len(results['errors'])}\n")

    print(f"FUNDAMENTALS SCAN complete: {len(results['updated'])} updated, "
          f"{len(results['no_data'])} no data, {len(results['errors'])} errors")

    print("Refreshing Price and computing Score (raw data files only)...")
    import subprocess
    import sys
    subprocess.run([sys.executable, "update_price.py"], cwd=ROOT, check=False)
    subprocess.run([sys.executable, "compute_score.py"], cwd=ROOT, check=False)
    subprocess.run([sys.executable, "compute_secondary_score.py"], cwd=ROOT, check=False)
    subprocess.run([sys.executable, "compute_risk_score.py"], cwd=ROOT, check=False)
    subprocess.run([sys.executable, "compute_growth_score.py"], cwd=ROOT, check=False)
    subprocess.run([sys.executable, "compute_overall_score.py"], cwd=ROOT, check=False)
    subprocess.run([sys.executable, "compute_score_percentile.py"], cwd=ROOT, check=False)

    print("Appending today's snapshot to score_history.tsv...")
    subprocess.run([sys.executable, "score_history.py"], cwd=ROOT, check=False)

    print("Updating signal backtest (no-ops quietly until enough daily history accumulates)...")
    subprocess.run([sys.executable, "backtest_signals.py"], cwd=ROOT, check=False)

    print("Checking for meaningful day-over-day Score changes...")
    subprocess.run([sys.executable, "compute_score_change.py"], cwd=ROOT, check=False)

    print("Rebuilding site (build_site.py runs every merge script + reassembles)...")
    subprocess.run([sys.executable, "build_site.py"], cwd=ROOT, check=False)


if __name__ == "__main__":
    main()
