import re

ROWS_FILE = "all_rows.html"

# Native/raw scraped currency per exchange (matches whatever eToro/TipRanks actually
# displayed when the ticker was scraped — no conversion, just labeling reality).
# London/London AIM: eToro shows LSE main-board/AIM prices in GBX (pence), not GBP —
# confirmed repeatedly in SESSION_LOG_LONDON.md ("GBX-pence-scale"). A handful of
# ADR-based London-listed names (e.g. BP.L, GSK.L, AZN.L, BHP.L) are actually quoted
# in USD on eToro — this per-exchange mapping can't capture that per-ticker exception,
# it's a known simplification, not a data conversion (the underlying number is untouched).
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

# Per-ticker overrides for the ANALYST TARGET (Low/Avg/High) currency only, where it's
# confirmed to differ from the exchange's own price currency above. Found and documented
# in SESSION_LOG_LONDON.md: these London-listed names have eToro/TipRanks analyst
# coverage sourced from their US ADR, in USD, while their own price is still the LSE
# quote in GBX pence — a genuine mixed-currency row, not a mistake to "fix" by picking
# one. Only the label reflects this; no values are touched. Not exhaustive — only the
# cases actually caught and logged so far; other undiscovered ADR-coverage tickers on
# any exchange would still show the (wrong) exchange-default target currency.
TARGET_CURRENCY_OVERRIDE = {
    "BP.L": "USD",
    "AZN.L": "USD",
    "BHP.L": "USD",
    "GSK.L": "USD",
}

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
