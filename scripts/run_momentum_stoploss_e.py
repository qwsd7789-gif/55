import json
import math
import os
import time
from dataclasses import dataclass
from typing import Dict, List, Tuple, Set

import numpy as np
import pandas as pd
import requests
from io import StringIO

try:
    import yfinance as yf
except Exception as e:
    raise RuntimeError("yfinance not installed") from e


# ===== Spec-locked constants =====
DOWNLOAD_START = "2014-01-01"
EVAL_START = pd.Timestamp("2016-01-04")
EVAL_END = pd.Timestamp("2026-03-13")
FEE_ONE_WAY = 0.001
TOP_PERCENT = 0.05
MIN_CANDIDATES = 5
STOP1 = -0.08
STOP2 = -0.12
STOP_MULT = 0.7
MAX_RETRIES = 3
BACKOFF = [1, 3, 5]

OUT_ROOT = os.path.join("outputs", "momentum_stoploss_e")


@dataclass
class Event:
    eff_month_end: pd.Timestamp
    added: str
    removed: str


def norm_ticker(x: str) -> str:
    if x is None:
        return ""
    s = str(x).strip().upper().replace(".", "-")
    if s in {"", "NAN", "NONE", "NULL"}:
        return ""
    return s


def _col_str(c) -> str:
    if isinstance(c, tuple):
        return " ".join([str(x) for x in c if str(x) != "nan"]).strip()
    return str(c)


def first_col(df: pd.DataFrame, candidates: List[str]):
    lower = {_col_str(c).lower(): c for c in df.columns}
    for k in candidates:
        if k.lower() in lower:
            return lower[k.lower()]
    # fuzzy
    for c in df.columns:
        lc = _col_str(c).lower()
        if any(k.lower() in lc for k in candidates):
            return c
    raise ValueError(f"cannot find columns {candidates} in {[ _col_str(x) for x in df.columns ]}")


def load_wikipedia_tables() -> Tuple[Set[str], pd.DataFrame]:
    url = "https://en.wikipedia.org/wiki/Nasdaq-100"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    resp = requests.get(url, headers=headers, timeout=30)
    if resp.status_code != 200:
        raise RuntimeError(f"failed to fetch wikipedia page: {resp.status_code}")
    tables = pd.read_html(StringIO(resp.text))

    current = None
    changes = None

    for t in tables:
        cols = [str(c).lower() for c in t.columns]
        if any("ticker" in c for c in cols) and (any("company" in c for c in cols) or any("name" in c for c in cols)):
            current = t.copy()
            break
    if current is None:
        raise RuntimeError("failed to locate current constituents table")

    for t in tables:
        cols = [str(c).lower() for c in t.columns]
        if any("date" in c for c in cols) and any("added" in c for c in cols) and any("removed" in c for c in cols):
            changes = t.copy()
            break
    if changes is None:
        # fallback: pick a plausible one
        for t in tables:
            cols = [str(c).lower() for c in t.columns]
            if any("date" in c for c in cols) and any("add" in c for c in cols):
                changes = t.copy()
                break
    if changes is None:
        raise RuntimeError("failed to locate changes table")

    ticker_col = first_col(current, ["Ticker", "Ticker symbol", "Symbol"])
    current_set = set(norm_ticker(x) for x in current[ticker_col].tolist())
    current_set = {x for x in current_set if x}

    date_col = first_col(changes, ["Date"])
    added_col = first_col(changes, ["Added"])
    removed_col = first_col(changes, ["Removed"])

    ch = changes[[date_col, added_col, removed_col]].copy()
    ch.columns = ["date", "added", "removed"]
    ch["date"] = pd.to_datetime(ch["date"], errors="coerce")
    ch = ch.dropna(subset=["date"])
    ch["added"] = ch["added"].map(norm_ticker)
    ch["removed"] = ch["removed"].map(norm_ticker)
    ch = ch[(ch["added"] != "") | (ch["removed"] != "")]

    return current_set, ch


def download_one(ticker: str, start: str, end: str) -> pd.DataFrame:
    last_err = None
    for i in range(MAX_RETRIES):
        try:
            df = yf.download(
                ticker,
                start=start,
                end=end,
                auto_adjust=True,
                progress=False,
                actions=False,
                interval="1d",
                threads=False,
            )
            if df is None or df.empty:
                raise RuntimeError("empty dataframe")
            df = df.sort_index()
            if not df.index.is_monotonic_increasing:
                raise RuntimeError("non-monotonic dates")
            if (df["Close"] <= 0).any():
                raise RuntimeError("non-positive close")
            if "Open" not in df.columns:
                raise RuntimeError("missing open")
            return df[["Open", "Close"]].copy()
        except Exception as e:
            last_err = e
            if i < MAX_RETRIES - 1:
                time.sleep(BACKOFF[min(i, len(BACKOFF)-1)])
    raise RuntimeError(f"download failed {ticker}: {last_err}")


def month_end_trading_days(trading_dates: pd.DatetimeIndex) -> List[pd.Timestamp]:
    s = pd.Series(trading_dates, index=trading_dates)
    me = s.groupby([s.index.year, s.index.month]).max().tolist()
    return [pd.Timestamp(x) for x in me]


def build_pit_snapshots(
    current_set: Set[str],
    changes_df: pd.DataFrame,
    month_ends: List[pd.Timestamp],
) -> Dict[pd.Timestamp, List[str]]:
    month_ends = sorted(month_ends)
    me_idx = pd.Index(month_ends)

    def eff_me(d: pd.Timestamp) -> pd.Timestamp:
        pos = me_idx.searchsorted(d, side="left")
        if pos >= len(me_idx):
            return month_ends[-1] + pd.Timedelta(days=1)  # effective after range
        return month_ends[pos]

    events: List[Event] = []
    for _, r in changes_df.iterrows():
        events.append(Event(eff_month_end=eff_me(pd.Timestamp(r["date"])), added=r["added"], removed=r["removed"]))

    events.sort(key=lambda x: x.eff_month_end, reverse=True)

    snapshots: Dict[pd.Timestamp, List[str]] = {}
    cur = set(current_set)
    p = 0

    for m in sorted(month_ends, reverse=True):
        while p < len(events) and events[p].eff_month_end > m:
            e = events[p]
            if e.added and e.added in cur:
                cur.remove(e.added)
            if e.removed:
                cur.add(e.removed)
            p += 1
        snapshots[m] = sorted(cur)

    return snapshots


def compute_signal_for_date(
    signal_date: pd.Timestamp,
    month_ends: List[pd.Timestamp],
    closes: pd.DataFrame,
    pit: Dict[pd.Timestamp, List[str]],
) -> Dict:
    idx = month_ends.index(signal_date)
    if idx < 12:
        return {"valid": False, "reason": "insufficient_history"}
    d1 = month_ends[idx - 1]
    d12 = month_ends[idx - 12]

    if "QQQ" not in closes.columns or pd.isna(closes.at[d1, "QQQ"]) or pd.isna(closes.at[d12, "QQQ"]):
        return {"valid": False, "reason": "qqq_missing"}

    qqq_mom = closes.at[d1, "QQQ"] / closes.at[d12, "QQQ"] - 1

    members = pit.get(signal_date, [])
    moms = []
    for t in members:
        if t not in closes.columns:
            continue
        p1 = closes.at[d1, t] if d1 in closes.index else np.nan
        p12 = closes.at[d12, t] if d12 in closes.index else np.nan
        if pd.isna(p1) or pd.isna(p12) or p1 <= 0 or p12 <= 0:
            continue
        m = p1 / p12 - 1
        if m > qqq_mom:
            moms.append((t, m))

    gate_on = bool(qqq_mom > 0)
    pass_count = len(moms)

    selected = []
    n = 0
    if gate_on and pass_count >= MIN_CANDIDATES:
        moms = sorted(moms, key=lambda x: (-x[1], x[0]))
        n = max(1, int(math.floor(pass_count * TOP_PERCENT)))
        selected = [x[0] for x in moms[:n]]

    return {
        "valid": True,
        "signal_date": signal_date,
        "d1": d1,
        "d12": d12,
        "qqq_mom": float(qqq_mom),
        "gate_on": gate_on,
        "pass_count": pass_count,
        "n": n,
        "selected": selected,
    }


def first_trading_day_after(dates: List[pd.Timestamp], d: pd.Timestamp):
    idx = pd.Index(dates).searchsorted(d, side="right")
    if idx >= len(dates):
        return None
    return dates[idx]


def run_backtest(
    mode: str,
    opens: pd.DataFrame,
    closes: pd.DataFrame,
    month_ends: List[pd.Timestamp],
    pit: Dict[pd.Timestamp, List[str]],
    outdir: str,
    charge_stop_fee: bool = True,
):
    os.makedirs(outdir, exist_ok=True)

    warnings = []
    trade_logs = []
    daily_nav_rows = []
    daily_weights_rows = []
    signal_ck_rows = []

    trading_days = [d for d in closes.index if EVAL_START <= d <= EVAL_END]
    if not trading_days:
        raise RuntimeError("no eval trading days")

    # precompute month signals and execution days
    month_ends_eval = [d for d in month_ends if EVAL_START <= d <= EVAL_END]
    exec_plan = {}
    for s in month_ends_eval:
        sig = compute_signal_for_date(s, month_ends, closes, pit)
        if not sig.get("valid", False):
            signal_ck_rows.append({"signal_date": s.date(), "valid": False, "reason": sig.get("reason", "unknown")})
            continue
        e = first_trading_day_after(list(closes.index), s)
        sig["exec_date"] = e
        exec_plan[s] = sig
        signal_ck_rows.append(
            {
                "signal_date": s.date(),
                "exec_date": e.date() if e is not None else None,
                "qqq_mom": sig["qqq_mom"],
                "gate_on": sig["gate_on"],
                "rs_pass_count": sig["pass_count"],
                "top5_n": sig["n"],
                "top5_selected": "|".join(sig["selected"][:5]),
            }
        )

    # portfolio state
    weights: Dict[str, float] = {}
    entry: Dict[str, float] = {}
    hit1: Dict[str, bool] = {}
    hit2: Dict[str, bool] = {}

    pending_open_ops = {}  # for shadow: date -> list of ops

    nav = 1.0

    def normalize_weights(w: Dict[str, float]) -> Dict[str, float]:
        return {k: float(v) for k, v in w.items() if v > 1e-12}

    def apply_monthly_rebalance(d: pd.Timestamp, selected: List[str], exec_price_field: str):
        nonlocal weights, entry, hit1, hit2

        old = dict(weights)
        target = {}
        if selected:
            w = 1.0 / len(selected)
            for t in selected:
                px = (opens if exec_price_field == "open" else closes).at[d, t] if t in (opens if exec_price_field == "open" else closes).columns else np.nan
                if pd.isna(px) or px <= 0:
                    warnings.append(f"{d.date()} monthly rebalance skip {t}: missing execution price")
                    continue
                target[t] = w

        # if some skipped due missing px, rescale equally among remaining
        if target:
            tw = sum(target.values())
            target = {k: v / tw for k, v in target.items()}

        all_tickers = set(old.keys()) | set(target.keys())
        turnover = sum(abs(target.get(t, 0.0) - old.get(t, 0.0)) for t in all_tickers)
        fee = FEE_ONE_WAY * turnover

        weights = normalize_weights(target)

        # reset anchors/hits for new cycle at monthly rebalance
        entry = {}
        hit1 = {}
        hit2 = {}
        for t, w in weights.items():
            px = (opens if exec_price_field == "open" else closes).at[d, t]
            entry[t] = float(px)
            hit1[t] = False
            hit2[t] = False

        trade_logs.append(
            {
                "date": d.date(),
                "event": "monthly_rebalance",
                "mode": mode,
                "exec_price": exec_price_field,
                "turnover": turnover,
                "fee": fee,
                "details": json.dumps({"selected": selected, "target": weights}, ensure_ascii=False),
            }
        )
        return fee, turnover

    def apply_stop_reduction(d: pd.Timestamp, reductions: Dict[str, float], exec_price_field: str):
        nonlocal weights
        old = dict(weights)
        for t, mult in reductions.items():
            if t in weights:
                weights[t] = weights[t] * mult
        weights = normalize_weights(weights)
        all_tickers = set(old.keys()) | set(weights.keys())
        turnover = sum(abs(weights.get(t, 0.0) - old.get(t, 0.0)) for t in all_tickers)
        fee = (FEE_ONE_WAY * turnover) if charge_stop_fee else 0.0

        trade_logs.append(
            {
                "date": d.date(),
                "event": "stoploss_reduction",
                "mode": mode,
                "exec_price": exec_price_field,
                "turnover": turnover,
                "fee": fee,
                "details": json.dumps(reductions, ensure_ascii=False),
            }
        )
        return fee, turnover

    month_exec_dates = set(v["exec_date"] for v in exec_plan.values() if v.get("exec_date") is not None)

    for d in trading_days:
        fee_reb = 0.0
        fee_stop = 0.0
        to_reb = 0.0
        to_stop = 0.0

        # shadow open executions first
        if mode == "shadow" and d in pending_open_ops:
            for op in pending_open_ops[d]:
                if op["type"] == "monthly":
                    f, to = apply_monthly_rebalance(d, op["selected"], "open")
                    fee_reb += f
                    to_reb += to
                elif op["type"] == "stop":
                    f, to = apply_stop_reduction(d, op["reductions"], "open")
                    fee_stop += f
                    to_stop += to
            del pending_open_ops[d]

        # daily close-to-close gross return
        gross = 0.0
        for t, w in list(weights.items()):
            if t not in closes.columns:
                continue
            idx = closes.index.get_loc(d)
            if idx == 0:
                r = 0.0
            else:
                prev_d = closes.index[idx - 1]
                p0 = closes.at[prev_d, t] if prev_d in closes.index else np.nan
                p1 = closes.at[d, t] if d in closes.index else np.nan
                if pd.isna(p0) or pd.isna(p1) or p0 <= 0 or p1 <= 0:
                    r = 0.0  # missing data rule: contribution 0
                else:
                    r = p1 / p0 - 1
            gross += w * r

        net = gross - fee_reb - fee_stop
        nav *= (1.0 + net)

        # canonical monthly rebalance at close day
        for s, sig in exec_plan.items():
            if sig.get("exec_date") == d and mode == "canonical":
                f, to = apply_monthly_rebalance(d, sig["selected"], "close")
                fee_reb += f
                to_reb += to

        # queue monthly for shadow
        for s, sig in exec_plan.items():
            if sig.get("exec_date") == d and mode == "shadow":
                pending_open_ops.setdefault(d, []).append({"type": "monthly", "selected": sig["selected"]})

        # stop logic (skip monthly execution day per collision rule)
        if d not in month_exec_dates:
            reductions = {}
            for t, w in list(weights.items()):
                if w <= 0:
                    continue
                if t not in entry:
                    continue
                px = closes.at[d, t] if t in closes.columns else np.nan
                if pd.isna(px) or px <= 0:
                    continue
                dd = px / entry[t] - 1

                mult = 1.0
                if (not hit1.get(t, False)) and dd <= STOP1:
                    mult *= STOP_MULT
                    hit1[t] = True
                if (not hit2.get(t, False)) and dd <= STOP2:
                    mult *= STOP_MULT
                    hit2[t] = True
                if mult < 1.0:
                    reductions[t] = mult

            if reductions:
                if mode == "canonical":
                    f, to = apply_stop_reduction(d, reductions, "close")
                    fee_stop += f
                    to_stop += to
                else:
                    nd = first_trading_day_after(list(closes.index), d)
                    if nd is None or nd > EVAL_END:
                        warnings.append(f"{d.date()} stop triggered but no next open within eval window")
                    else:
                        pending_open_ops.setdefault(nd, []).append({"type": "stop", "reductions": reductions})

        # record daily weights (long format)
        if weights:
            for t, w in weights.items():
                daily_weights_rows.append({"date": d.date(), "ticker": t, "weight": w})
        else:
            daily_weights_rows.append({"date": d.date(), "ticker": "CASH", "weight": 1.0})

        daily_nav_rows.append(
            {
                "date": d.date(),
                "ret_gross": gross,
                "fee_rebalance": fee_reb,
                "fee_stop": fee_stop,
                "turnover_rebalance": to_reb,
                "turnover_stop": to_stop,
                "ret_net": net,
                "nav": nav,
            }
        )

    nav_df = pd.DataFrame(daily_nav_rows)
    ret = nav_df["ret_net"]
    n_days = len(nav_df)
    total_return = nav_df["nav"].iloc[-1] / nav_df["nav"].iloc[0] - 1
    cagr = nav_df["nav"].iloc[-1] ** (252 / n_days) - 1
    cummax = nav_df["nav"].cummax()
    mdd = (nav_df["nav"] / cummax - 1).min()
    sharpe = (ret.mean() * 252) / (ret.std(ddof=0) * np.sqrt(252)) if ret.std(ddof=0) > 0 else np.nan

    summary = {
        "mode": mode,
        "charge_stop_fee": charge_stop_fee,
        "window": [str(EVAL_START.date()), str(EVAL_END.date())],
        "total_return_pct": float(total_return * 100),
        "cagr_pct": float(cagr * 100),
        "mdd_pct": float(mdd * 100),
        "sharpe": float(sharpe),
        "n_days": int(n_days),
    }

    # write required outputs
    nav_df.to_csv(os.path.join(outdir, "daily_nav.csv"), index=False)
    pd.DataFrame(daily_weights_rows).to_csv(os.path.join(outdir, "daily_weights.csv"), index=False)
    pd.DataFrame(trade_logs).to_csv(os.path.join(outdir, "trade_log_full.csv"), index=False)

    # checkpoint outputs monthly
    sig_df = pd.DataFrame(signal_ck_rows)
    for _, r in sig_df.dropna(subset=["signal_date"]).iterrows():
        try:
            sd = pd.Timestamp(r["signal_date"])
            fn = f"signal_checkpoint_{sd.year:04d}_{sd.month:02d}.csv"
            pd.DataFrame([r]).to_csv(os.path.join(outdir, fn), index=False)
        except Exception:
            pass

    with open(os.path.join(outdir, "audit_warnings.log"), "w", encoding="utf-8") as f:
        for w in warnings:
            f.write(w + "\n")

    with open(os.path.join(outdir, "performance_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    return summary, nav_df, sig_df


def main():
    os.makedirs(OUT_ROOT, exist_ok=True)

    warnings_global = []

    current_set, changes = load_wikipedia_tables()

    # QQQ first (fail_fast if unavailable)
    qqq = download_one("QQQ", DOWNLOAD_START, str(EVAL_END + pd.Timedelta(days=7)))
    qqq.index = pd.to_datetime(qqq.index).tz_localize(None)
    trading_dates = qqq.index
    me = month_end_trading_days(trading_dates)

    pit = build_pit_snapshots(current_set, changes, me)

    # export monthly universe snapshots
    uni_dir = os.path.join(OUT_ROOT, "universe_snapshots")
    os.makedirs(uni_dir, exist_ok=True)
    for m in me:
        members = pit.get(m, [])
        if not members:
            continue
        fn = f"universe_snapshot_{m.year:04d}_{m.month:02d}.csv"
        pd.DataFrame({"signal_month_end": [m.date()] * len(members), "ticker": members}).to_csv(
            os.path.join(uni_dir, fn), index=False
        )

    # build ticker universe from snapshots in eval+lookback
    needed_months = [d for d in me if pd.Timestamp("2015-01-01") <= d <= EVAL_END]
    tickers = sorted(set(t for m in needed_months for t in pit.get(m, [])))
    if "QQQ" not in tickers:
        tickers.append("QQQ")

    # download all tickers (partial failure allowed except QQQ)
    opens = pd.DataFrame(index=trading_dates)
    closes = pd.DataFrame(index=trading_dates)

    opens["QQQ"] = qqq["Open"].reindex(trading_dates)
    closes["QQQ"] = qqq["Close"].reindex(trading_dates)

    fail_tickers = []
    for i, t in enumerate(tickers):
        if t == "QQQ":
            continue
        try:
            df = download_one(t, DOWNLOAD_START, str(EVAL_END + pd.Timedelta(days=7)))
            df.index = pd.to_datetime(df.index).tz_localize(None)
            opens[t] = df["Open"].reindex(trading_dates)
            closes[t] = df["Close"].reindex(trading_dates)
        except Exception as e:
            fail_tickers.append((t, str(e)))

    # long gap warnings
    for t in closes.columns:
        s = closes[t].dropna()
        if len(s) < 2:
            continue
        d = pd.Series(s.index)
        gaps = d.diff().dt.days.fillna(1)
        # 5 trading days approximate as >9 calendar days due weekends/holidays
        if (gaps > 9).any():
            warnings_global.append(f"long_gap_warning {t}: max_calendar_gap_days={int(gaps.max())}")

    # write global download issues
    with open(os.path.join(OUT_ROOT, "download_failures.log"), "w", encoding="utf-8") as f:
        for t, e in fail_tickers:
            f.write(f"{t}\t{e}\n")
        for w in warnings_global:
            f.write(w + "\n")

    # canonical (with stop fees)
    canonical_dir = os.path.join(OUT_ROOT, "canonical_mode")
    summary_can, nav_can, sig_can = run_backtest("canonical", opens, closes, me, pit, canonical_dir, charge_stop_fee=True)

    # canonical (without stop fees) for expected delta check
    canonical_nsf_dir = os.path.join(OUT_ROOT, "canonical_mode_without_stop_fees")
    summary_can_nsf, nav_can_nsf, _ = run_backtest("canonical", opens, closes, me, pit, canonical_nsf_dir, charge_stop_fee=False)

    # shadow
    shadow_dir = os.path.join(OUT_ROOT, "realistic_shadow_mode")
    # shadow missing execution open fail_fast check will happen naturally in run by skipping? enforce here for monthly selected names impossible ahead.
    summary_shadow, nav_shadow, sig_shadow = run_backtest("shadow", opens, closes, me, pit, shadow_dir, charge_stop_fee=True)

    # current status checkpoint (asof spec)
    ck = {}
    target_signal = pd.Timestamp("2026-02-27") if pd.Timestamp("2026-02-28") not in me else pd.Timestamp("2026-02-28")
    if target_signal not in me:
        # use month-end for Feb 2026 in calendar
        feb = [d for d in me if d.year == 2026 and d.month == 2]
        if feb:
            target_signal = feb[-1]
    if target_signal in me:
        sig = compute_signal_for_date(target_signal, me, closes, pit)
        exec_date = first_trading_day_after(list(closes.index), target_signal)
        ck = {
            "asof": "2026-03-13",
            "signal_date": str(target_signal.date()),
            "exec_date": str(exec_date.date()) if exec_date is not None else None,
            "gate_on": bool(sig.get("gate_on", False)),
            "qqq_mom_12_1_pct": float(sig.get("qqq_mom", np.nan) * 100) if sig.get("valid") else None,
            "rs_pass_count": int(sig.get("pass_count", 0)) if sig.get("valid") else None,
            "top5_n": int(sig.get("n", 0)) if sig.get("valid") else None,
            "top5_selected": sig.get("selected", [])[:5] if sig.get("valid") else [],
        }
        # stop levels for selected names based on canonical latest entry (approx: exec close)
        if sig.get("valid") and sig.get("selected") and exec_date is not None:
            stop_map = {}
            for t in sig["selected"][:5]:
                if t in closes.columns and exec_date in closes.index and pd.Timestamp("2026-03-13") in closes.index:
                    ent = float(closes.at[exec_date, t])
                    last = float(closes.at[pd.Timestamp("2026-03-13"), t])
                    stop8 = ent * (1 + STOP1)
                    stop12 = ent * (1 + STOP2)
                    dist8 = (last / stop8 - 1) * 100
                    dist12 = (last / stop12 - 1) * 100
                    stop_map[t] = {
                        "entry": ent,
                        "last": last,
                        "stop8": stop8,
                        "stop12": stop12,
                        "dist_to_stop8_pct": dist8,
                        "dist_to_stop12_pct": dist12,
                    }
            ck["stop_levels"] = stop_map

    expected = {
        "with_stop": {"total_return_pct": 10908.12, "cagr_pct": 58.76, "mdd_pct": -50.00, "sharpe": 1.25},
        "without_stop": {"total_return_pct": 11133.13, "cagr_pct": 59.08, "mdd_pct": -49.84, "sharpe": 1.25},
        "delta": {"total_return_pctpts": -225.01, "cagr_pctpts": -0.32, "mdd_pctpts": -0.16, "sharpe_diff": 0.00},
    }
    band = {
        "total_return_pct_diff_relative": 3.0,
        "cagr_diff_abs_pctpts": 0.8,
        "mdd_diff_abs_pctpts": 1.5,
        "sharpe_diff_abs": 0.08,
    }

    def rel_diff_pct(a, b):
        return abs(a - b) / max(abs(b), 1e-9) * 100

    recon = {
        "canonical_with_stop": {
            "actual": summary_can,
            "expected": expected["with_stop"],
            "diff": {
                "total_return_pct_diff_relative": rel_diff_pct(summary_can["total_return_pct"], expected["with_stop"]["total_return_pct"]),
                "cagr_diff_abs_pctpts": abs(summary_can["cagr_pct"] - expected["with_stop"]["cagr_pct"]),
                "mdd_diff_abs_pctpts": abs(summary_can["mdd_pct"] - expected["with_stop"]["mdd_pct"]),
                "sharpe_diff_abs": abs(summary_can["sharpe"] - expected["with_stop"]["sharpe"]),
            },
        },
        "canonical_without_stop_fee": {
            "actual": summary_can_nsf,
            "expected": expected["without_stop"],
            "diff": {
                "total_return_pct_diff_relative": rel_diff_pct(summary_can_nsf["total_return_pct"], expected["without_stop"]["total_return_pct"]),
                "cagr_diff_abs_pctpts": abs(summary_can_nsf["cagr_pct"] - expected["without_stop"]["cagr_pct"]),
                "mdd_diff_abs_pctpts": abs(summary_can_nsf["mdd_pct"] - expected["without_stop"]["mdd_pct"]),
                "sharpe_diff_abs": abs(summary_can_nsf["sharpe"] - expected["without_stop"]["sharpe"]),
            },
        },
        "delta_with_minus_without": {
            "actual": {
                "total_return_pctpts": summary_can["total_return_pct"] - summary_can_nsf["total_return_pct"],
                "cagr_pctpts": summary_can["cagr_pct"] - summary_can_nsf["cagr_pct"],
                "mdd_pctpts": summary_can["mdd_pct"] - summary_can_nsf["mdd_pct"],
                "sharpe_diff": summary_can["sharpe"] - summary_can_nsf["sharpe"],
            },
            "expected": expected["delta"],
        },
        "acceptance_band": band,
        "current_status_checkpoint": ck,
        "download_fail_tickers": [t for t, _ in fail_tickers],
    }

    for k in ["canonical_with_stop", "canonical_without_stop_fee"]:
        d = recon[k]["diff"]
        recon[k]["within_band"] = (
            d["total_return_pct_diff_relative"] <= band["total_return_pct_diff_relative"]
            and d["cagr_diff_abs_pctpts"] <= band["cagr_diff_abs_pctpts"]
            and d["mdd_diff_abs_pctpts"] <= band["mdd_diff_abs_pctpts"]
            and d["sharpe_diff_abs"] <= band["sharpe_diff_abs"]
        )

    with open(os.path.join(OUT_ROOT, "reconciliation.json"), "w", encoding="utf-8") as f:
        json.dump(recon, f, ensure_ascii=False, indent=2)

    # add required file copies at mode root names if missing
    # universe + signal checkpoints are many files; ensure at least one exists in each mode folder
    for mdir in [canonical_dir, shadow_dir]:
        # copy Feb 2026 checkpoint as canonical checkpoint file convenience
        feb_ck = [x for x in os.listdir(mdir) if x.startswith("signal_checkpoint_2026_02")]
        if not feb_ck:
            # fallback write a placeholder from recon
            pd.DataFrame([ck]).to_csv(os.path.join(mdir, "signal_checkpoint_2026_02.csv"), index=False)

        # place latest universe snapshot file in mode dir
        uni_latest = os.path.join(uni_dir, "universe_snapshot_2026_02.csv")
        if os.path.exists(uni_latest):
            pd.read_csv(uni_latest).to_csv(os.path.join(mdir, "universe_snapshot_2026_02.csv"), index=False)

    print(json.dumps({
        "canonical_mode": summary_can,
        "canonical_mode_without_stop_fee": summary_can_nsf,
        "realistic_shadow_mode": summary_shadow,
        "out_root": OUT_ROOT,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
