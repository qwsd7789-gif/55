from pathlib import Path
p = Path(r'C:\Users\Administrator\.openclaw\workspace\skills\clawchain-miner\scripts\mine.py')
text = p.read_text(encoding='utf-8')
start = text.index('def solve_with_llm(')
end = text.index('def _call_anthropic(')
print(text[start:end].encode('unicode_escape').decode())
