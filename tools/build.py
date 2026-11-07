"""Build data/events.json from data/events.txt and data/world.json from Atlas Arcade's world data."""
import json, sys, pathlib, ast
root = pathlib.Path(__file__).resolve().parent.parent
CATS = {"invention","everyday","empire","nation","conflict","exploration","trade","science","culture","religion"}
out, seen = [], set()
for n, line in enumerate((root/"data/events.txt").read_text().splitlines(), 1):
    if not line.strip() or line.startswith("#"): continue
    parts = line.split("|")
    if len(parts) != 7: sys.exit(f"line {n}: expected 7 fields, got {len(parts)}")
    y, t, p, la, lo, c, f = parts
    circa = y.startswith("~"); y = int(y.lstrip("~")); la = float(la); lo = float(lo)
    assert -12000 < y <= 2026, (n, y)
    assert -90 <= la <= 90 and -180 <= lo <= 180, (n, la, lo)
    assert c in CATS, (n, c)
    key = (y, t.lower())
    assert key not in seen, (n, "duplicate", t); seen.add(key)
    out.append({"id": len(out), "y": y, "ca": circa, "t": t, "p": p, "la": la, "lo": lo, "c": c, "f": f})
out.sort(key=lambda e: e["y"])
for i, e in enumerate(out): e["id"] = i
(root/"data/events.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
print(len(out), "events")
src = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else None
if src:
    feats = []
    def rnd(x): return [rnd(v) for v in x] if isinstance(x, list) else round(x, 2)
    for c in json.loads(src.read_text()):
        g = c["g"] if isinstance(c["g"], dict) else ast.literal_eval(c["g"])
        feats.append({"type": "Feature", "properties": {"n": c["n"]}, "geometry": {"type": g["type"], "coordinates": rnd(g["coordinates"])}})
    (root/"data/world.json").write_text(json.dumps({"type": "FeatureCollection", "features": feats}, separators=(",", ":")))
    print(len(feats), "countries")
