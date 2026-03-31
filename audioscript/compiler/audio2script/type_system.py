# ai_spotibot_player
# AudioMIX
# audioscript/compiler/audio2script/type_system.py

from __future__ import annotations
from typing import Dict, List, Optional, Tuple

"""
AudioScript Type System (v0.1-dev)

This module defines the type system for AudioScript Live.
It is responsible for:
  1. Representing the types that exist in AudioScript
  2. Storing type signatures for all known commands
  3. Tracking types of let bindings during compilation
  4. Resolving the type of binary expressions (FXChain + FXChain, for instance)

Current grammar structures defines what can be written.
Our type system defines what makes sense.
They are intentionally separate.
The + operator is generic - its meaning is resolved here
"""

# Layer 1 - Type Represenation
# Primitive types right now
# New types will be added here as AS expands
class ASType:
    FXCHAIN = "FXChain"    # signal processing chain (stutter(2) + reverb)
    NUMBER  = "Number"     # a numeric value (128, 0.8, -6.5)
    STRING  = "String"     # a text value ("hype", "song_title")
    PATTERN = "Pattern"    # a rhythmic sequence (["kick", "snare", "kick", "hate"])
    VOID    = "Void"       # commands that cause an effect w/o producing a value
    UNKNOWN = "Unknown"    # type could not be resolved (using inference, not valid final type)

# Layer 2 - Type Signatures
# Maps known AS commands to its type signature
# Parameter types use ordered lists, optional parameters not yet modeled
# Variadic parameters (like trigger_zones) are marked as UNKNOWN until
# I introduce a richer signature model
TYPE_SIGNATURES: Dict[str, Tuple[List[str], str]] = {

    # --- Playback ---
    # play(pattern) -> Void
    # plays a rhythmic pattern through the engine
    "play":             ([ASType.PATTERN], ASType.VOID),

    # stop() -> Void
    # halts playback
    "stop":             ([], ASType.VOID),

    # sleep(ms) -> Void
    # pauses execution for a given number of ms
    "sleep":            ([ASType.NUMBER], ASType.VOID),

    # set_mode(mode, codec) -> Void
    # sets playback mode to lossless/lossy
    # second param (codec) is optional in runtime; modeled as Str for now
    "set_mode":         ([ASType.STRING, ASType.STRING], ASType.VOID),

    # get_mode() -> Void
    # prints current playback mode (side effect only)
    "get_mode":         ([], ASType.VOID),

    # --- FX/Signal chain ---
    # SFX are in development

    # stutter(rate) -> FXChain
    # creates a stutter FX at given rate
    "stutter":          ([ASType.NUMBER], ASType.FXCHAIN),

    # reverb() -> FXChain
    # creates a reverb FX w/ default params
    "reverb":           ([], ASType.FXCHAIN),

    # delay(time) -> FXChain
    # creates a delay FX w/ the given time in ms
    "delay":            ([ASType.NUMBER], ASType.FXCHAIN),

    # compressor(threshold) -> FXChain
    # creates a compressor w/ the given threshold in dB
    "compressor":       ([ASType.NUMBER], ASType.FXCHAIN),

    # --- EQ ---
    # eq.preset(name) -> FXChain
    # loads a named EQ preset > returns it as an FXChain
    "eq.preset":        ([ASType.STRING], ASType.FXCHAIN),

    # --- LED ---
    # glow(color) -> Void
    # sets ambient LED color
    "glow":             ([ASType.STRING], ASType.VOID),

    # fade(color, duration) -> Void
    # fades LED to a color over a given duration in ms
    "fade":             ([ASType.STRING, ASType.NUMBER], ASType.VOID),

    # pulse(color, bpm) -> Void
    # pulses LEDs at a given BPM
    "pulse":            ([ASType.STRING, ASType.NUMBER], ASType.VOID),

    # trigger_zones(zones, mood, bpm) -> Void
    # triggers LED zones w/ mood + BPM context
    # zones is a Pattern (list); variadic kwargs modeled simply for now
    "trigger_zones":    ([ASType.PATTERN, ASType.STRING, ASType.NUMBER], ASType.VOID),

    # --- Mood ---
    # mood.set(mood_name) -> Void
    # sets the current mood context
    "mood.set":         ([ASType.STRING], ASType.VOID),

    # --- Patterns ---
    # repeat(pattern) -> Pattern
    # wraps a pattern in a repeating loop structure
    "repeat":           ([ASType.PATTERN], ASType.PATTERN),
}

# Layer 3 - Type Environment
# Tracks the types of let bindings as the compiler walks a script
# Grows incrementally; each resolved binding is stored immediately
# Currently flat (no nested scopes) - TODO: add scope support
class TypeEnvironment:
    # holds the type of every let binding seen so far in a script
    # memory management
    def __init__(self):
        # mapes identifier name -> ASType str
        self._bindings: Dict[str, str] = {}

        # tracks identifiers whose types could not be resolved
        # used for deferred resolution + error reporting
        self._unresolved: List[str] = []

    # record identifier 'name' has type 'resolved_type'
    # called after a let binding is successfully type-checked
    def bind(self, name: str, resolved_type: str) -> None:
        self._bindings[name] = resolved type
        # if prev unresolved, clear that flag
        if name in self._unresolved:
            self._unresolved.remove(name)

    # return type of identifier 'name' or None if not found
    def lookup(self, name: str) -> Optional[str]:
        return self._bindings.get(name, None)

    # flags 'name' as a binding that the type checker could not resolve
    # stores ASType.UNKNOWN so later passes know to revisit
    def mark_unresolved(self, name: str) -> None:
        self._bindings[name] = ASType.UNKNOWN
        if name not in self._unresolved:
            self._unresolved.append(name)

    # returns True is any bindings could not be resolved
    # designed to be useful for a final validation pass after type checking completes
    def has_unresolved(self) -> bool:
        return len(self._unresolved) > 0

    # returns the list of identifier names that remain unresolved
    # for generating meaningful/verbose error logs
    def unresolved_names(self) -> List[str]:
        return list(self._unresolved)

    # human-readable snapshot of environ (Live)
    # designed to be used for debugging type checker for development
    def __repr__(self) -> str:
        lines = ["TypeEnvironment {"]
        for name, t in self._bindings.items():
            flag = " ⚠️  unresolved" if name in self._unresolved else ""
            lines.append(f"  {name}: {t}{flag}")
        lines.append("}")
        return "\n".join(lines)
