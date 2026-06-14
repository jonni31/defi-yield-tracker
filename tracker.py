#!/usr/bin/env python3
import json, time, argparse
import httpx

def fetch():
    print("[*] Fetching DefiLlama...")
    with httpx.Client(timeout=30) as c:
        return c.get("https://yields.llama.fi/pools").json()["data"]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--protocol"); ap.add_argument("--min-apy", type=float, default=0)
    ap.add_argument("--limit", type=int, default=20); ap.add_argument("--export")
    a = ap.parse_args()
    pools = fetch()
    r = [p for p in pools if (p.get("apy") or 0) >= a.min_apy and (not a.protocol or (p.get("project") or "").lower() == a.protocol.lower()) and (p.get("tvlUsd") or 0) > 100000]
    r.sort(key=lambda x: x.get("apy",0) or 0, reverse=True)
    print(f"\n{'Project':<18} {'Chain':<12} {'APY':>8} {'TVL':>14}")
    print("-"*56)
    for p in r[:a.limit]:
        print(f"{p['project']:<18} {p['chain']:<12} {(p.get('apy') or 0):>7.2f}% ${(p.get('tvlUsd') or 0):>13,.0f}")
    if a.export:
        import csv
        with open(a.export,"w",newline="") as f:
            w = csv.DictWriter(f, fieldnames=["project","chain","symbol","apy","tvlUsd"])
            w.writeheader()
            for p in r: w.writerow({k: p.get(k) for k in ["project","chain","symbol","apy","tvlUsd"]})
        print(f"[+] Exported to {a.export}")

if __name__ == "__main__": main()
