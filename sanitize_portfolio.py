"""
GIT CLEAN FILTER - strips real/virtual portfolio data (positions, P&L, TP
badges) out of all_rows.html/nasdaq-stocks.html before the content ever
enters git history, so a public GitHub repo never exposes real account
holdings even if someone runs `git add`/`git commit` locally without
thinking about it first.

This is NOT a one-time script - it's wired as a git "clean" filter via
.gitattributes (`all_rows.html filter=sanitize-portfolio`) and local repo
config (`git config filter.sanitize-portfolio.clean "python sanitize_portfolio.py"`).
Git runs it automatically on every `git add`/`git commit` of those two files;
the local working copy on disk is never touched, only what goes into the
git blob. Reads HTML from stdin, writes sanitized HTML to stdout - mirrors
merge_portfolio.py's own "strip previously-injected data" regexes exactly
(lines 66/98/99 there), since that script's own clearing logic is the
authoritative definition of "everything this feature owns".

Strips: data-pf-<acct>-* attributes (units/avg/pl/plpct/netvalue/tp/status,
both v=virtual and r=real accounts) and the pf-badge/tp-badge spans (which
would otherwise leak "you hold this ticker" as a bare yes/no signal even
without exact numbers).
"""

import re
import sys


def sanitize(html):
    html = re.sub(r'\s*data-pf-[a-z]+(?:-[a-z]+)?="[^"]*"', '', html)
    html = re.sub(r'<span class="pf-badge[^"]*"(?: data-acct="[a-z]")?></span>', '', html)
    html = re.sub(r'<span class="tp-badge[^"]*"(?: data-acct="[a-z]")?></span>', '', html)
    return html


if __name__ == "__main__":
    data = sys.stdin.buffer.read().decode("utf-8")
    sys.stdout.buffer.write(sanitize(data).encode("utf-8"))
