from pathlib import Path
p = Path(r"C:\Users\Administrator\.openclaw\workspace\scripts\run_momentum_stoploss_e.py")
t = p.read_text(encoding="utf-8")
old = '''def load_wikipedia_tables() -> Tuple[Set[str], pd.DataFrame]:
    url = "https://en.wikipedia.org/wiki/Nasdaq-100"
    tables = pd.read_html(url)

    current = None
    changes = None
'''
new = '''def load_wikipedia_tables() -> Tuple[Set[str], pd.DataFrame]:
    url = "https://en.wikipedia.org/wiki/Nasdaq-100"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    resp = requests.get(url, headers=headers, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(f"failed to fetch wikipedia page: {resp.status_code}")
    tables = pd.read_html(resp.text)

    current = None
    changes = None
'''
if old not in t:
    raise SystemExit('target block not found')
t = t.replace(old, new)
p.write_text(t, encoding="utf-8")
print("patched")
