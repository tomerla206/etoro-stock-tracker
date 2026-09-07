import csv
import html
import re
import sys

EXCHANGES = [
    ("nyse_data.tsv", "NYSE"),
    ("frankfurt_data.tsv", "Frankfurt"),
    ("paris_data.tsv", "Paris"),
    ("sydney_data.tsv", "Sydney"),
    ("stockholm_data.tsv", "Stockholm"),
    ("hongkong_data.tsv", "Hong Kong"),
    ("oslo_data.tsv", "Oslo"),
    ("tokyo_data.tsv", "Tokyo"),
    ("milan_data.tsv", "Milan"),
    ("zurich_data.tsv", "Zurich"),
    ("amsterdam_data.tsv", "Amsterdam"),
    ("brussels_data.tsv", "Brussels"),
    ("helsinki_data.tsv", "Helsinki"),
    ("copenhagen_data.tsv", "Copenhagen"),
    ("lisbon_data.tsv", "Lisbon"),
    ("madrid_data.tsv", "Madrid"),
    ("otc_data.tsv", "OTC Markets"),
    ("abudhabi_data.tsv", "Abu Dhabi"),
    ("dubai_data.tsv", "Dubai"),
    ("london_data.tsv", "London"),
    ("london_aim_data.tsv", "London AIM"),
    ("saudiarabia_data.tsv", "Saudi Arabia"),
    ("chicago_data.tsv", "Chicago"),
]

def parse_price(raw):
    raw = (raw or "").strip()
    if not raw:
        return ""
    if raw.upper().endswith("K"):
        try:
            return f"{float(raw[:-1]) * 1000:.2f}"
        except ValueError:
            return raw
    return raw

def rating_class(rating):
    if not rating:
        return "rating-none"
    r = rating.lower()
    if "sell" in r:
        return "rating-sell"
    if "hold" in r:
        return "rating-hold"
    if "buy" in r:
        return "rating-buy"
    return "rating-none"

def build_row(ticker, name, price, cons, rating, div, exchange):
    ticker = ticker.strip()
    name_esc = html.escape(name.strip())
    price = parse_price(price)
    cons = (cons or "").strip().rstrip("%")
    rating = (rating or "").strip()
    div = (div or "").strip().rstrip("%")
    slug = ticker.lower()

    cons_cell = f'<td class="cons-cell col-cons">{cons}%</td>' if cons else '<td class="cons-cell col-cons empty">&ndash;</td>'
    rating_cell = f'<td class="rating-cell col-rating {rating_class(rating)}">{html.escape(rating)}</td>' if rating else '<td class="rating-cell col-rating rating-none">&ndash;</td>'

    return (
        f'      <tr data-ticker="{html.escape(ticker)}" data-price="{price}" data-exchange="{exchange}" '
        f'data-cons="{cons}" data-rating="{html.escape(rating)}" data-div="{div}" '
        f'data-low="" data-avg="" data-high="">'
        f'<td class="rownum"></td>'
        f'<td><a class="stock-link" href="https://www.etoro.com/markets/{slug}/research" target="_blank" rel="noopener">'
        f'<span class="ticker">{html.escape(ticker)}</span><span class="name">{name_esc}</span></a></td>'
        f'<td class="exchange">{exchange}</td>'
        f'<td class="price">{price}</td>'
        f'{cons_cell}'
        f'{rating_cell}'
        f'<td class="div-cell col-div">{div}%</td>'
        f'<td class="analysis-cell analysis-low col-target empty">&ndash;</td>'
        f'<td class="analysis-cell analysis-avg col-target empty">&ndash;</td>'
        f'<td class="analysis-cell analysis-high col-target empty">&ndash;</td>'
        f'<td class="pct-cell col-target empty">&ndash;</td>'
        f'<td class="alloc-cell col-target empty">&ndash;</td>'
        f'<td class="pl-cell col-target empty">&ndash;</td>'
        f'<td class="pl-share-cell col-target empty">&ndash;</td></tr>\n'
    )

def main():
    out_path = "extra_exchange_rows.html"
    total = 0
    with open(out_path, "w", encoding="utf-8") as out:
        for tsv_file, exchange in EXCHANGES:
            count = 0
            with open(tsv_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.rstrip("\n")
                    if not line:
                        continue
                    fields = line.split("\t")
                    if len(fields) < 6:
                        fields += [""] * (6 - len(fields))
                    ticker, name, price, cons, rating, div = fields[:6]
                    out.write(build_row(ticker, name, price, cons, rating, div, exchange))
                    count += 1
            print(f"{exchange}: {count} rows from {tsv_file}")
            total += count
    print(f"Total: {total} rows written to {out_path}")

if __name__ == "__main__":
    main()
