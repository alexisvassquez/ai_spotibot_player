# ai_spotibot_player
# AudioMIX
# audioscript_runtime_safe.py

import os, sys, importlib, shlex

print ("AudioMIX Ultra-safe Shell - type load(\"module.py\") or Ctrl+C to exit")

LOADED = {}

def load(mod_file: str):
    mod_file = mod_file.strip().strip('"').strip("'")
    if not mod_file.endswith(".py"):
        print ("⚠️ pass a .py file (e.g., load(\"shell_tools.py\"))")
        return
    name = mod_file[:-3]
    mod_path = f"performance_engine.modules.{name}".replace("-", "_")
    print (f"....importing {mod_path}")
    try:
        m = importlib.import_module(mod_path)
        LOADED[name] = m
        if hasattr(m, "register"):
            try:
                m.register()    # self register
                print (f"✅ registered commands from {name}")
            except Exception as e:
                print (f"⚠️ register() failed in {name}: {e}")
        else:
            print (f"ℹ️ no register() in {name}")
    except Exception as e:
        print (f"❌ import failed for {name}: {e}")


def list_loaded():
    if not LOADED:
        print ("ℹ️ no modules loaded yet")
        return
    for k in LOADED:
        print (f" - {k}")

def parse_and_execute(line: str):
    line = (line or "").strip()
    if not line or line.startswith("#"):
        return
    if "(" in line and line.endswith(")"):
        cmd, arg = line.split("(", 1)
        arg = arg[:-1]
        if cmd == "load":
            load(arg)
        elif cmd == "list_loaded":
            list_loaded()
        else:
            print (f"⚠️ unknown command: {cmd}")
    else:
        print ("ℹ️ use load(\"module.py\") or list_loaded()")

try:
    while True:
        line = input("🛡️  > ")
        parse_and_execute(line)
except KeyboardInterrupt:
    print("\nsee you later! 👋")
