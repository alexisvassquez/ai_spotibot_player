# ai_spotibot_player
# AudioMIX
# performance_engine/dsp_bridge.py

# Translates AudioMIX EventBus events into NDJSON
# commands for the C++ audiomix DSP engine.
# The C++ process is started separately for now.
# DSPBridge connects to it via stdin/stdout pipes.
# TODO: DSPBridge will launch the process itself via
# subprocess.Popen

from __future__ import annotations
import json
import sys
import os
import threading
from typing import Optional

class DSPBridge:
    def __init__(self, event_bus, dsp_stdin=None, dsp_stdout=None, verbose=False):
        self._bus = event_bus
        self._lock = threading.Lock()
        self._verbose = verbose

        """
        For now: default to sys.stdout as the pipe to the
        DSP engine.
        When Popen launch is added later, these will get replaced w/ process.stdin / process.stdout TODO
        """
        # write commands here
        self._dsp_in = dsp_stdin or sys.stdout
        # read acks here
        # (acknowledgments / tests to see if DSP picked up signal)
        self._dsp_out = dsp_stdout or sys.stdin

        # register all DSP event handlers on the bus
        self._register_handlers()

    # Registration
    def _register_handlers(self):
        self._bus.on("dsp.eq.set", self._handle_eq_set)
        self._bus.on("dsp.compressor.set", self._handle_compressor_set)
        self._bus.on("dsp.gain.set", self._handle_gain_set)
        self._bus.on("dsp.ping", self._handle_ping)

    # Handlers
    # one per DSP command type
    def _handle_eq_set(self, payload: dict):
        """
        Expected payload keys mirror EqParams in C++:
        band (int), freq (float), gain_db (float), q (float),
        type (str)
        """
        self._send({"cmd": "eq.set", **payload})

    def _handle_compressor_set(self, payload: dict):
        """
        Expected payload keys mirror CompressorParams in C++:
        threshold (float), ratio (float), attack_ms (float),
        release_ms (float)
        """ 
        self._send({"cmd": "compressor.set", **payload})

    def _handle_gain_set(self, payload: dict):
        """
        Expected payload keys:
        gain_db (float)
        """
        self._send({"cmd": "gain.set", **payload})

    def _handle_ping(self, payload=None):
        self._send({"cmd": "ping"})

    # Core send
    # serializes to NDJSON, writes to DSP process stdin
    def _send(self, message: dict):
        line = json.dumps(message)
        with self._lock:
            try:
                self._dsp_in.write(line + "\n")
                self._dsp_in.flush()
                if self._verbose:
                    print(f"[DSPBridge -> DSP] {line}")
            except (BrokenPipeError, OSError) as e:
                print(f"[DSPBridge] ! Could not reach DSP engine: {e}")
                print("[DSPBridge] Is the audiomix process running?")

    # Ack listener
    # reads responses from DSP process stdout
    # Run this in a background thread once process launching
    # is added.
    # Stubbed for now so the interface is ready TODO
    def listen_for_acks(self):
        """
        Reads NDJSON ack lines from the DSP engine stdout.
        Intended to run in a daemon thread.

        Usage (TODO, future - Popen integration):
            t = threading.Thread(target=bridge.listen_for_acks, daemon=True)
            t.start()
        """
        for raw_line in self._dsp_out:
            raw_line = raw_line.strip()
            if not raw_line:
                continue
            try:
                msg = json.loads(raw_line)
                cmd = msg.get("cmd")
                if cmd == "ack":
                    if self._verbose:
                        print(f"[DSPBridge <- DSP] ack: {msg.get('ack')}")
                elif cmd == "pong":
                    if self._verbose:
                        print("[DSPBridge <- DSP] pong received")
                elif cmd == "error":
                    print(f"[DSPBridge <- DSP] ! DSP error: {msg.get('error')}")
            except json.JSONDecodeError:
                print(f"[DSPBridge <- DSP] malformed response: {raw_line}!r")

# Convenience factory
def attach_dsp_bridge(event_bus, verbose=False) -> DSPBridge:
    """
    Creates a DSPBridge and attaches it to the given EventBus
    Call this once at AudioMIX startup.
    """
    return DSPBridge(event_bus, verbose=verbose)
