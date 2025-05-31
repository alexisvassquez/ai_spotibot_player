# AudioScript Specification (v0.1)

---

## Language Overview
**AudioScript** is a domain-specific language designed for controlling emotional, mood-aware, and LED-reactive audio experiences in the **AudioMIX** environment.
It draws influence from *Python*, *Shell Script*, *C/C++*, and *CMake*, blending readable high-level logic with real-time creative control.

---

## Syntax Philosophy
- **Whitespace-sensitive** (similar to *Python*)
- **Dot notation** for namespace-like structures (e.g., `mood.set("happy")`)
- **Function-call style** execution (`glow("blue")`)
- **Block syntax** for events and loops (`on track("chorus") { ... }`)
- **String-first language**: readable, expressive, emotional

---

## Comment Style
`# This is a comment`

---

## Core Functions (v0.1)
### Playback
```python
play("track_name.wav") # Play audio track
pause() # Pause playback
stop() # Stop playback
```

### Mood
```python
mood.set("euphoric") # Set the emotional context
```

### LED/Lighting
```python
glow("pink") # Set LED color
pulse("blue", bpm=128) # Pulse color to BPM
fade("warm", duration=3000) # Fade to color over time (ms)
strobe("red", intensity=1.0) # Flashing effect
```

### Flow Control
```python
sleep(500) # Wait for 500ms
loop(3) {  # Repeat N times
    pulse("blue", bpm=100)
    sleep(1000)
}
```

---

## Event Hooks (coming in v0.2)
```python
on track("chorus") {
    glow("gold")
    mood.set("inspired")
}
```

---

## Example Script
```python
mood.set("uplifted") # Set opening mood
glow("lilac")

play("intro.wav") # Start track
pulse("yellow", bpm=120)

sleep(2000) # Add fade for build
fade("electric_blue", duration=3000)
```

---

## Planned Features (v0.2+)
- `on mood("happy") {}`: Reactive mood triggers
- External input listeners (e.g., MIDI, DJ controller)
- Function chaining:
```python
track("intro").glow("orange").pulse("orange", 130)
```
- User-defined functions (macros)
- Config blocks (`audio { bpm: 128, gain: 0.9 }`)

---


## Runtime & Interpreter (v0.1)

The first version of the **AudioScript** runtime is currently in development. It will support:

- CLI parsing and execution of commands
- Function registry for AudioScript commands
- Interactive shell mode for live control
- File-based `.audioscript` execution

The interpreter will be written in Python (initially), with future hooks to C++/audio/LED engines.

Sample command line:
```bash
audioscript run scripts/club_set.audioscript
```

### Notes
- All string values must be in double quotes: `"value"`
- All durations are in milliseconds (ms)
- BPM is an integer

**AudioScript** is meant to be *playful*, *modular*, and deeply *expressive* - your code should feel like writing a performance.
Stay tuned for the first interpreter and CLI integration.

(c) Alexis M Vasquez, AMV Digital Studios 
Creator of AudioMIX/AudioScript 2025
