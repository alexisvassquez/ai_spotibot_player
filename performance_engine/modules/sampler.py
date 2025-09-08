# ai_spotibot_player
# AudioMIX
# performance_engine/modules/sampler.py

import os, json, subprocess
from typing import Dict, Any
from .performance_engine.modules.track_engine import track_registry
from .performance_engine.modules.led_controller import pulse
from .performance_engine.utils.shell_output import say

sample_registry: Dict[str, str] = {}

def load_sample(name: str, path: str):
    if not os.path.exists(path):
        say(f"❌ File not found: {path}", "⚠️")
        return
    sample_registry[name] = path
    say(f"Sample loaded: {name} -> {path}", "📂")

def trigger_sample(name: str):
    path = sample_registry.get(name)
    if not path:
        say(f"❌ Sample not found: {name}", "🚫")
        return
    say(f"💥 Triggering sample: {name}", "🎧")
    subprocess.Popen(["aplay", path])
    # Pulse LED for feedback
    pulse("yellow", 140)

# Sampler bank with aliases + attribution
_BANKS: Dict[str, Dict[str, Any]] = {}

def sampler_bank_load(path: str):
    """Load sampler bank JSON with alias -> file mapping + attribution."""
    if not os.path.exists(path):
        say(f"[sampler] bank not found: {path}", "⚠️")
        return
    try:
        with open(path, "r") as f:
            data = json.load(f)
        name = data.get("name", os.path.splitext(os.path.basename(path))[0])
        sounds = data.get("sounds", {})
        if not isinstance(sounds, dict) or not sounds:
            say(f"[sampler] no 'sounds' in bank: {path}", "⚠️")
            return
        _BANKS[name] = data
        say(f"[sampler] loaded bank '{name}' ({len(sounds)} sounds)", "✅")
    except Exception as e:
        say(f"[sampler] failed to load bank: {e}", "❌")

def sampler_play(bank: str, alias: str):
    b = _BANKS.get(bank)
    if not b:
        say(f"[sampler] bank not loaded: {bank}", "⚠️")
        return
    meta = b["sounds"].get(alias)
    if not meta:
        say(f"[sampler] alias not found in '{bank}': {alias}", "⚠️")
        return

    path = meta.get("file")
    if not path or not os.path.exists(path):
        say(f"[sampler] file missing {bank}:{alias} -> {path}", "⚠️")
        return

    say(f"💥 {bank}:{alias} -> {os.path.basename(path)}", "🎧")
    subprocess.Popen(["aplay", path])
    # Pulse LED for feedback
    pulse("yellow", 140)

def sampler_list(bank: str = ""):
    """List loaded banks + aliases."""
    if not _BANKS:
        say("[sampler] no banks loaded yet", "ℹ️")
        return
    if not bank:
        say("Loaded banks:", "📤")
        for n, b in _BANKS.items():
            say(f" - {n} ({len(b.get('sounds', {}))} sounds)")
        return
    b = _BANKS.get(bank)
    if not b:
        say(f"[sampler] bank not loaded: {bank}", "⚠️")
        return
    say(f"Bank '{bank}' sounds:", "🎼")
    for alias, meta in b.get("sounds", {}).items():
        say(f" - {alias} -> {meta.get('file', '?')}")

def sampler_credits(bank: str):
    """Print attribution lines for a bank (console/show notes + credits)."""
    b = _BANKS.get(bank)
    if not b:
        say(f"[sampler] bank not loaded: {bank}", "⚠️")
        return
    say(f"Credits for bank '{bank}':", "🏷️")
    for alias, meta in b.get("sounds", {}).items():
        title = meta.get("title", os.path.basename(meta.get("file", "?")))
        author = meta.get("author", "?")
        source = meta.get("source", "")
        license = meta.get("license", "")
        url = meta.get("url", "")
        line = f"- {alias}: \"{title}\" by {author}"
        if source:    line += f" - {source}"
        if license_:  line += f" ({license_})"
        if url:       line += f" - {url}"
        say(line)

def sampler_export_credits(bank: str, out_path: str = "docs/CREDITS.md"):
    """Write credits to a Markdown file."""
    b = _BANKS.get(bank)
    if not b:
        say(f"[sampler] bank not loaded: {bank}", "⚠️")
        return
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    lines = [f"# Credits for sampler bank '{bank}'", ""]
    for alias, meta in b.get("sounds", {}).items():
        title = meta.get("title", os.path.basename(meta.get("file", "?")))
        author = meta.get("author", "?")
        source = meta.get("source", "")
        license_ = meta.get("license", "")
        url = meta.get("url", "")
        entry = f"- **{alias}** - *{title}* by **{author}**"
        if source:    entry += f" - {source}"
        if license_:  entry += f" ({license_})"
        if url:       entry += f" - {url}"
        lines.append(entry)
    with open(out_path, "w") as f:
        f.write("\n".join(lines) + "\n")
    say(f"[sampler] wrote credits -> {out_path}", "📝")

def register():
    return {
        "load_sample": load_sample,
        "trigger_sample": trigger_sample,
        "sampler.bank_load": sampler_bank_load,
        "sampler.play": sampler_play,
        "sampler.list": sampler_list,
        "sampler.credits": sampler_credits,
        "sampler.export_credits": sampler_export_credits,
    }
