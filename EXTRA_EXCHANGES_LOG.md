# Extra Exchanges Project — Handoff Log (Zurich, Amsterdam, Brussels, Helsinki, Copenhagen, Lisbon, Madrid, OTC Markets, Abu Dhabi, Dubai, London/LSE, Saudi Arabia, Chicago)

**Read this file, then `EXTRA_EXCHANGES_STATUS.md`.** These 13 exchanges were all added in one batch (2026-08-26) alongside the existing sibling projects (NASDAQ `PROJECT_LOG.md`, NYSE, Frankfurt, Paris, Sydney, Stockholm, Hong Kong, Oslo, Tokyo, Milan). Rather than 13 separate project-log/status-board file pairs, they share this one log + one combined status board, to keep the file count manageable — same v4 methodology and file-naming spirit as the others, just consolidated.

## ⚠️ Policy: SEQUENTIAL — joins the back of the existing queue

Same policy as Hong Kong/Oslo/Tokyo/Milan: one exchange project active at a time, in order. These 13 join the back of the queue, after Milan. Do not start any group from this batch while another sibling project's agent is active.

## The goal and method — identical to every other exchange

Analyst Low/Average/High price target + tradeability per stock, via the **v4 text-based method** — see `PROJECT_LOG.md`'s "v4 METHOD UPDATE" section, read in full before starting any group here. Quick summary:
- Analyst Low/Avg/High: `https://widgets.tipranks.com/content/etoro/etoro-widget.html?lang=en&ticker={TICKER}&theme=light`, `get_page_text`. "This stock has no research data" = NOFAQ.
- Price + tradeability: `https://www.etoro.com/markets/{ticker-lower}/research`, `get_page_text` for price, `Array.from(document.querySelectorAll('button')).filter(b=>b.textContent.trim()==='Trade').map(b=>b.disabled)` for tradeability.
- Mandatory human-paced protocol: randomized 3-8s per ticker, batches of 12-15 then randomized 30-50s pause.
- Rigorously verify eToro login before starting (AAPL check).

## Per-exchange specifics — ticker suffix, source quirks, master file

All built 2026-08-26 from user-provided CSV exports in `H:\קלוד\הורדות\New folder\`. Same 6-column tsv format as every other exchange (`TICKER<TAB>Name<TAB>Price<TAB>Consensus%<TAB>Rating<TAB>DividendYield`) — Consensus%/Rating blank in all of these (source CSVs didn't include those columns), same as most other CSV-based imports in this project family.

| Exchange | Master file | Tickers | Suffix | Notes |
|---|---|---|---|---|
| Zurich | `zurich_data.tsv` | 56 | `.ZU` | Some K-notation prices (e.g. `GIVN.ZU` = `3.32K`) — handled same as other exchanges. |
| Amsterdam | `amsterdam_data.tsv` | 95 | `.NV` | Some K-notation prices (`ADYEN.NV`, `ASML.NV`). |
| Brussels | `brussels_data.tsv` | 83 | `.BR` | Some K-notation prices (`LOTB.BR`). |
| Helsinki | `helsinki_data.tsv` | 94 | `.HE` | — |
| Copenhagen | `copenhagen_data.tsv` | 78 | `.CO` | Frequent K-notation prices (many Danish stocks quoted in the thousands, e.g. `MAERSKB.CO` = `22.09K`). |
| Lisbon | `lisbon_data.tsv` | 24 | `.LS` (3 legacy tickers use `.LSB`: `BCP.LSB`, `EDP.LSB`, `JMT.LSB`) — keep exactly as exported, don't renormalize. | Smallest full-letter exchange in this batch. |
| Madrid | `madrid_data.tsv` | 51 | `.MC` | — |
| OTC Markets | `otc_data.tsv` | 72 | **No consistent suffix** — most tickers are bare (e.g. `MTBLY`), a few carry `.US` (e.g. `LUNA.US`, `REEAF.US`). Use exactly as given in the tsv, don't add a suffix. | Many prices are `0.00` — confirmed legitimate (delisted/bankrupt/near-worthless OTC tickers), not a parsing error, same pattern seen on NASDAQ's own OTC-adjacent tickers earlier in this project. |
| Abu Dhabi | `abudhabi_data.tsv` | 29 | `.DH` | Source CSV had no dividend-yield column (6 cols: avatar/ticker/name/price/volume/PE, dividend skipped) — dividend field left blank, doesn't block scraping. |
| Dubai | `dubai_data.tsv` | 29 | `.AE` | Source CSV only had 4 columns (avatar/ticker/name/price), like Tokyo's — no dividend/volume/PE at all. |
| London | `london_data.tsv` | 414 | `.L` | **The main London Stock Exchange board** (built 2026-08-29 from a proper `לונדון.csv` export — includes blue-chip names like `HSBA.L` HSBC). This is distinct from London AIM below; 0 ticker overlap confirmed between the two files. |
| London AIM | `london_aim_data.tsv` | 145 | `.L` | Smaller-cap/alternative segments: **combined from three separate user exports**: `LSE AIM.csv` (74), `LSE AIM Auction.csv` (63), `LSE AUCTION.csv` (8) — different LSE market/order-type segments, same `.L` suffix convention, merged into one list. Verified 0 duplicate tickers across all three sources, and 0 overlap with the main `london_data.tsv`. **Originally mislabeled "London"** — renamed 2026-08-29 after the user provided a proper main-board export and the gap was discovered (a spot-check on `1833.HK`/general site-completeness question revealed the main LSE board, including HSBC, was missing entirely). No scraping had started on this group before the rename, so no data was affected. |
| Saudi Arabia | `saudiarabia_data.tsv` | **1** (`SAOC`, Aramco Saudi Arabian Oil Corp) | none | Source CSV (`SAUDI ARABIA+שיקגו.csv`) was a malformed/corrupted export (captured raw screener UI markup instead of a clean ticker list) — only one usable data row was recoverable for each of the two exchanges it mixed together. If the user provides a proper Saudi Arabia export later, rebuild this file from that instead. |
| Chicago | `chicago_data.tsv` | **1** (`CBOE`, Cboe Global Markets Inc.) | none | Same malformed source file as Saudi Arabia above — only one usable row recovered. Rebuild from a proper export if the user provides one. |

## File naming convention

- Output: `analyst_targets_<EXCHANGE>_<GROUP>.txt` (e.g. `analyst_targets_ZURICH_A.txt`, `analyst_targets_LONDON_S.txt`).
- Session log: `SESSION_LOG_<EXCHANGE>_<GROUP>.md`.
- Claim board: the shared `EXTRA_EXCHANGES_STATUS.md`.
- Saudi Arabia and Chicago (1 ticker each): just do the single ticker directly, output to `analyst_targets_SAUDIARABIA.txt` / `analyst_targets_CHICAGO.txt` (no letter/group suffix needed), no letter split.

## Completeness audit

Same technique as every other project: diff every ticker in the group's slice of the exchange's `*_data.tsv` against the output file, both directions, before declaring done.

## The eventual site

Already covered by the existing multi-exchange site (`nasdaq-stocks.html`, titled "Global Stock Snapshot") — extend `generate_exchange_rows.py`'s `EXCHANGES` list with entries like `("zurich_data.tsv", "Zurich")` for each of these 13 and re-run the merge, same process used for every other exchange.
