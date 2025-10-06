# AudioScript Specification (v0.2-dev)

---

## Language Overview
**AudioScript** is a domain-specific language designed for controlling emotional, mood-aware, and LED-reactive audio experiences in the **AudioMIX** environment.
It draws influence from *Python*, *Haskell*, *Shell Script*, *C/C++*, and *CMake*, blending readable high-level logic with real-time creative control.

---

## Syntax Philosophy
- **Whitespace-sensitive** (like *Python*)
- **Pure function chaining** (like *Haskell*)
- **Dot notation** for namespace-like structures (e.g., `mood.set("happy")`)
- **Block syntax** for events and loops (`on track("chorus") { ... }`)
- **Lazy evaluation** (e.g., `repeat()` and `take()`)
- **Pattern-first** and **emotionally expressive**

---

## Comment Style
`# This is a comment`

---

## New Features (v0.2)

### Functional Expressions
```python
let beat = repeat(["kick", "snare"])
let fx = stutter(2) + reverb

play("<sound_file_name>.wav") with fx
```

### Pattern Reactivity
```python
on mood("happy") {
  glow("yellow")
  play("<sound_file_name>.wav")
}

every(8, strobe("white"))
```

### Lazy Evaluation Helpers
```python
let kick_loop = take(4, repeat(["kick", "snare"]))
play(kick_loop)
```

### User Macros (in development)
```python
def introDrop() {
  play("<sound_file_name>.wav")
  pulse("blue", bpm=120)
}
introDrop()
```

---

## Core Functions (v0.2)

### Playback
```python
play("<sound_file_name>.wav")    # Play audio track
pause()                          # Pause playback
stop()                           # Stop playback
set_mode("lossy", "mp3_128")     # Set playback codec
get_mode()
```

### Mood + Lighting
```python
mood.set("euphoric")             # Set the emotional context
glow("pink")                     # Static LED color
pulse("blue", bpm=128)           # Pulse color with BPM
fade("warm", duration=3000)      # Fade to color (ms)
strobe("red", intensity=1.0)     # Flash effect
```

### Flow Control
```python
sleep(500)                       # Wait time (ms)
loop(3) {                        # Repeat n times
  pulse("blue", bpm=100)
  sleep(1000)
}
```

### Event Hooks (in development)
```python
on track("chorus") {
  glow("gold")
  mood.set("inspired")
}

on mood("sad") {
  fade("blue", duration=4000)
}
```

---

## Runtime & Interpreter
The **AudioScript (AS)** interpreter is written in Python and supports:
- CLI parsing and execution
- `.audioscript` and `.as` file evaluation
Interactive shell mode
- Lazy generators and Haskell-inspired function chaining

### Sample command line:
```bash
audioscript run scripts/club_set.audioscript
```

---

## Notes
- All string values must be in double quotes: `"value"`
- Durations are in milliseconds(ms) - e.g., `sleep(3000)`
- BPM is an integer
- Expressions using `let` can hold infinite generators
- Use `with` to apply FX chains like `reverb`, `stuttuer`, etc.

**AudioScript** is *modular*, *expressive*, *customizable*, and *emotionally-alive*. It is a musical programming language designed for live coders who want to write their performances.

(c) Alexis Marie Vasquez, AMV Digital Studios 2025 
Creator of AudioMIX/AudioScript
