# ai_spotibot_player
# AudioMIX
# audio/ai/compiler/audio2script/event_mapper.py

from typing import List
from audio.ai.compiler.audio2script.script_ir import ShowIR, Section, Event

"""
Event Mapper v0

Intro version. This version generates basic semantic events based purely on
section labels.
Allows for testing the IR -> generator -> AudioScript(AS) pipeline before adding
DSP frame-based rules.
"""

# Generates basic ShowIR from stub analysis
# Produces one event per section using simple semantic mapping
def map_features_to_events(
    audio_path: str,
    sections: List[Section],
    bpm: float,
) -> ShowIR:
    show = ShowIR(
        audio_path=audio_path,
        bpm=bpm,
        sections=sections,
        events=[],
        profile_name="stub-basic"
    )

    for sec in sections:
        if sec.label == "intro":
            show.add_event(Event(
                time=sec.start,
                type="ambient_fade_in",
                params={"intensity": 0.3}
            ))

        elif sec.label == "build":
            show.add_event(Event(
                time=sec.start,
                type="build_rise",
                params={"duration": sec.duration()}
            ))

        elif sec.label == "drop":
            show.add_event(Event(
                time=sec.start,
                type="drop_flash",
                params={"strobe_intensity": 1.0}
            ))

        elif sec.label == "outro":
            show.add_event(Event(
                time=sec.start,
                type="ambient_fade_out",
                params={"duration": sec.duration()}
            ))

        # for unknown sections, fallback to ambient fade
        else:
            show.add_event(Event(
                time=sec.start,
                type="ambient_fade_in",
                params={"intensity": 0.2}
            ))

    return show
