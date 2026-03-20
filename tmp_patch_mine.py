from pathlib import Path
p = Path(r'C:\Users\Administrator\.openclaw\workspace\skills\clawchain-miner\scripts\mine.py')
text = p.read_text(encoding='utf-8')
old = '''def solve_with_llm(prompt, challenge_type, config):
    "Solve with LLM (auto-detect available provider)""
    provider = config.get("llm_provider", "auto")
    model = config.get("llm_model", "")
    system_prompt = SYSTEM_PROMPTS.get(challenge_type, "Answer concisely and accurately. Return only the answer.")
    # Auto-detect provider based on available API keys
    if provider == "auto":
        if os.getenv("OPENAI_API_KEY"):
            provider = "openai"
            model = model or "gpt-4o-mini"
        elif os.getenv("GEMINI_API_KEY"):
            provider = "gemini"
            model = model or "gemini-2.0-flash"
        elif os.getenv("ANTHROPIC_API_KEY"):
            provider = "anthropic"
            model = model or "claude-3-5-haiku-latest"
        else:
            print("⚠️ No LLM API key found (OPENAI_API_KEY/GEMINI_API_KEY/ANTHROPIC_API_KEY)")
            return None
    if provider == "openai":
        return _call_openai(prompt, system_prompt, model or "gpt-4o-mini")
    elif provider == "anthropic":
        return _call_anthropic(prompt, system_prompt, model or "claude-3-5-haiku-latest")
    elif provider == "gemini":
        return _call_gemini(prompt, system_prompt, model or "gemini-2.0-flash")
    else:
        print(f"⚠️ Unsupported LLM provider: {provider}")
        return None

def _call_openai(prompt, system_prompt, model):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️ OPENAI_API_KEY not set")
        return None
    try:
        resp = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1,
                "max_tokens": 200,
            },
            timeout=30
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"⚠️ OpenAI API failed: {e}")
        return None
'''
new = '''def _load_openclaw_provider(provider_name):
    "Load provider config from ~/.openclaw/openclaw.json without exposing secrets.""
    cfg_path = Path.home() / ".openclaw" / "openclaw.json"
    if not cfg_path.exists():
        return None
    try:
        with open(cfg_path, encoding="utf-8") as f:
            data = json.load(f)
        providers = (((data or {}).get("models") or {}).get("providers") or {})
        return providers.get(provider_name)
    except Exception:
        return None

def solve_with_llm(prompt, challenge_type, config):
    "Solve with LLM (auto-detect available provider, including OpenClaw codexmanager).""
    provider = config.get("llm_provider", "auto")
    model = config.get("llm_model", "")
    system_prompt = SYSTEM_PROMPTS.get(challenge_type, "Answer concisely and accurately. Return only the answer.")
    if provider == "auto":
        if os.getenv("OPENAI_API_KEY"):
            provider = "openai"
            model = model or "gpt-4o-mini"
        else:
            codex_cfg = _load_openclaw_provider("codexmanager")
            if codex_cfg and codex_cfg.get("apiKey") and codex_cfg.get("baseUrl"):
                provider = "openai"
                model = model or config.get("codexmanager_model") or "gpt-5.3-codex"
                config["_runtime_openai_base_url"] = codex_cfg.get("baseUrl")
                config["_runtime_openai_api_key"] = codex_cfg.get("apiKey")
            elif os.getenv("GEMINI_API_KEY"):
                provider = "gemini"
                model = model or "gemini-2.0-flash"
            elif os.getenv("ANTHROPIC_API_KEY"):
                provider = "anthropic"
                model = model or "claude-3-5-haiku-latest"
            else:
                print("⚠️ No LLM API key found and no OpenClaw codexmanager provider available")
                return None
    if provider == "openai":
        return _call_openai(prompt, system_prompt, model or "gpt-4o-mini", config)
    elif provider == "anthropic":
        return _call_anthropic(prompt, system_prompt, model or "claude-3-5-haiku-latest")
    elif provider == "gemini":
        return _call_gemini(prompt, system_prompt, model or "gemini-2.0-flash")
    else:
        print(f"⚠️ Unsupported LLM provider: {provider}")
        return None

def _call_openai(prompt, system_prompt, model, config=None):
    api_key = (config or {}).get("_runtime_openai_api_key") or os.getenv("OPENAI_API_KEY")
    base_url = ((config or {}).get("_runtime_openai_base_url") or os.getenv("OPENAI_BASE_URL") or "https://api.openai.com/v1").rstrip("/")
    if not api_key:
        print("⚠️ OPENAI_API_KEY not set")
        return None
    try:
        resp = requests.post(
            f"base_url}/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1,
                "max_tokens": 200,
            },
            timeout=30
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"⚠️ OpenAI-compatible API failed: {e}")
        return None
'''
if old not in text:
    raise SystemExit('target block not found')
text = text.replace(old, new, 1)
p.write_text(text, encoding='utf-8')
print('patched')
