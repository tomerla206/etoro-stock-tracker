import re

ROWS_FILE = "all_rows.html"

# Native/raw scraped currency per exchange (matches whatever eToro/TipRanks actually
# displayed when the ticker was scraped — no conversion, just labeling reality).
# London/London AIM: eToro shows LSE main-board/AIM prices in GBX (pence), not GBP —
# confirmed repeatedly in SESSION_LOG_LONDON.md ("GBX-pence-scale"). A handful of
# ADR-based London-listed names were once believed to have their analyst target
# quoted in USD while price stayed in GBX (see TARGET_CURRENCY_OVERRIDE below) -
# that turned out to no longer hold for the current scraping method as of
# 2026-09-10, so this per-exchange mapping is currently applied uniformly with
# no active per-ticker exceptions, but the override mechanism is kept in case a
# genuine case is found again on this or another exchange.
EXCHANGE_CURRENCY = {
    "NASDAQ": "USD",
    "NYSE": "USD",
    "OTC Markets": "USD",
    "Chicago": "USD",
    "Saudi Arabia": "SAR",
    "Frankfurt": "EUR",
    "Paris": "EUR",
    "Milan": "EUR",
    "Amsterdam": "EUR",
    "Brussels": "EUR",
    "Helsinki": "EUR",
    "Lisbon": "EUR",
    "Madrid": "EUR",
    "Stockholm": "SEK",
    "Copenhagen": "DKK",
    "Oslo": "NOK",
    "Zurich": "CHF",
    "Sydney": "AUD",
    "Hong Kong": "HKD",
    "Tokyo": "JPY",
    "Abu Dhabi": "AED",
    "Dubai": "AED",
    "London": "GBX",
    "London AIM": "GBX",
}

# Per-ticker overrides for the ANALYST TARGET (Low/Avg/High) currency only, for
# cases confirmed to differ from the exchange's own price currency above - kept
# empty for now (see 2026-09-10 removal note below), not deleted, since the
# underlying situation (an ADR-covered ticker whose analyst target ends up in a
# different currency than its own price) is a real category that could recur;
# only the label would change here, no values are ever touched.
#
# 2026-09-10: previously listed BP.L/AZN.L/BHP.L/GSK.L as USD, per
# SESSION_LOG_LONDON.md's original discovery that their TipRanks coverage was
# ADR-sourced in USD while price stayed in GBX pence. Verified directly against
# the live TipRanks widget (widgets.tipranks.com/content/etoro/etoro-widget.html)
# for all 4 tickers and found the mismatch NO LONGER HOLDS: the widget's own
# displayed upside % (e.g. BP.L "645.71 14.85%") is computed from a target
# that's on the exact same GBX-pence scale as price, not USD - likely because
# the scraping method changed to the public per-ticker widget URL on
# 2026-08-30 (see SESSION_LOG_LONDON.md), which apparently surfaces LSE-native
# targets for these names instead of ADR-based ones. Keeping this override
# active was actively wrong: it made the site tag a correctly-GBX-scaled
# target as USD (visibly showing a "$" prefix on the Low/Avg/High cells) and
# fed a currency-mismatched value into compute_score.py's upside_pts for
# these 4 tickers - see git history around 2026-09-10 for the two commits
# that introduced and then reverted that scoring attempt. If a genuine
# mismatch is found again (for these or other tickers), verify it the same
# way - live against the actual widget for the current scraping method -
# before re-adding an entry here.
TARGET_CURRENCY_OVERRIDE = {}

def esc(s):
    return s.replace('&', '&amp;').replace('"', '&quot;')

def main():
    with open(ROWS_FILE, encoding='utf-8') as f:
        html = f.read()

    # idempotent: strip any previously-injected currency attrs first
    html = re.sub(r'\s*data-currency="[^"]*"', '', html)
    html = re.sub(r'\s*data-target-currency="[^"]*"', '', html)

    def repl(m):
        ticker = m.group(1)
        exchange = m.group(2)
        currency = EXCHANGE_CURRENCY.get(exchange, "USD")
        target_currency = TARGET_CURRENCY_OVERRIDE.get(ticker, currency)
        attrs = f' data-currency="{esc(currency)}"'
        if target_currency != currency:
            attrs += f' data-target-currency="{esc(target_currency)}"'
        return m.group(0)[:-1] + attrs + '>'

    html, n = re.subn(r'<tr data-ticker="([^"]+)" data-price="[^"]*" data-exchange="([^"]+)"[^>]*>', repl, html)

    with open(ROWS_FILE, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Currency labels added to {n} rows ({len(TARGET_CURRENCY_OVERRIDE)} target-currency overrides applied).")

if __name__ == '__main__':
    main()
