import glob, sys

def tickers_from_tsv(path):
    out = set()
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line.strip():
                continue
            t = line.split('\t')[0].strip()
            if t:
                out.add(t)
    return out

def tickers_from_targets(pattern):
    out = set()
    files = glob.glob(pattern)
    for fp in files:
        with open(fp, encoding='utf-8') as f:
            for line in f:
                line = line.rstrip('\n')
                if not line.strip():
                    continue
                t = line.split('\t')[0].strip()
                if t:
                    out.add(t)
    return out, files

exchanges = [
    ("NASDAQ", "nasdaq_data.tsv", "analyst_targets_[A-Z].txt analyst_targets_[A-Z][0-9].txt"),
    ("NYSE", "nyse_data.tsv", "analyst_targets_NYSE_*.txt"),
    ("Frankfurt", "frankfurt_data.tsv", "analyst_targets_FRANKFURT_*.txt"),
    ("Paris", "paris_data.tsv", "analyst_targets_PARIS_*.txt"),
    ("Sydney", "sydney_data.tsv", "analyst_targets_SYDNEY_*.txt"),
    ("Stockholm", "stockholm_data.tsv", "analyst_targets_STOCKHOLM_*.txt"),
    ("HongKong", "hongkong_data.tsv", "analyst_targets_HONGKONG_*.txt"),
    ("Oslo", "oslo_data.tsv", "analyst_targets_OSLO_*.txt"),
    ("Tokyo", "tokyo_data.tsv", "analyst_targets_TOKYO_*.txt"),
    ("Milan", "milan_data.tsv", "analyst_targets_MILAN_*.txt"),
]

for name, tsv, pattern in exchanges:
    try:
        src = tickers_from_tsv(tsv)
    except FileNotFoundError:
        print(f"{name}: SOURCE TSV MISSING ({tsv})")
        continue
    patterns = pattern.split()
    got = set()
    files_all = []
    for p in patterns:
        g, files = tickers_from_targets(p)
        got |= g
        files_all += files
    # exclude backup/old files
    files_all = [f for f in files_all if 'OLD' not in f and 'backup' not in f]

    missing = src - got
    extra = got - src
    print(f"{name}: src={len(src)} scraped={len(got)} files={len(files_all)} missing={len(missing)} extra_not_in_src={len(extra)}")
    if missing:
        print(f"  MISSING SAMPLE: {sorted(missing)[:20]}")
    if extra:
        print(f"  EXTRA SAMPLE: {sorted(extra)[:20]}")
