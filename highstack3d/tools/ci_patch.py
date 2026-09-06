from pathlib import Path

path = Path(__file__).resolve().parents[1] / "scripts" / "game.gd"
text = path.read_text(encoding="utf-8")
old = '        var level:=int(s[key]);var title:=key.to_upper()+" Lv.%d"%level'
new = '        var level: int = int(s[key]); var title: String = str(key).to_upper()+" Lv.%d"%level'
if old not in text and new not in text:
    raise SystemExit("Expected skills title source line was not found")
text = text.replace(old, new)
path.write_text(text, encoding="utf-8")
print("Applied deterministic GDScript compatibility patch")
