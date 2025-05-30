# AudioScript (AS) Language Specification & Syntax Support

Welcome to the `audioscript/` directory - the official home of the **AudioScript (AS)** domain-specific language used in [AudioMIX](https://github.com/alexisvassquez/ai_spotibot_player). **AudioScript** is a modular, *expressive* scripting language designed to power **real-time music behavior, emotional audio cues, light-reactive visuals, and live performance logic** directly from the terminal.

> 🎛️  AudioScript is for those who feel sound, code emotion, and live at the intersection of creativity and computation.

---

## Included Files
| File | Purpose |
| ------ | ---------|
| `AudioScript.ebnf` | Official EBNF grammar definition for AudioScript |
| `audioscript.nanorc` | Syntax highlighting rules for GNU Nano |
| `example.as` | Sample AudioScript program demonstarting current supported syntax |
| *Future* `audioscript.tmLanguage.json` | VS Code/TextMate syntax highlighting (in progress) |
| *Future* `audioscript.vim` | Vim highlighting (in progress) |

---

## Syntax Highlighting Setup (Nano)

To enable syntax highlighting for **AudioScript (AS)** in Nano:

1. Copy `audioscript.nanorc` into your Nano config directory:
```bash
mkdir -p ~/.nano
cp audioscript.nanorc ~/.nano.
```

2. Add the following line to you `~/.nanorc`:
`include ~/.nano/audioscript.nanorc`

3. Open your `.as` or `.audioscript` files like this:
`nano -Y audioscript example.as`

---

## About the Language

**AudioScript** syntax blends the *minimalism of Bash*, the *readability of Python*, and the *modular precision of C/C++ and CMake*. It's engineered for low-latency programming, enabling instant response in live-performance settings - whether you're syncing audio, controlling LED arrays, or programming emotional shifts on stage.

Core design influences:
- **Python** - for intuitive flow and logic
- **Bash** - for command-style expressiveness
- **C / C++** - for speed, structure, and future module compilation
- **CMake** - for declarative, layered configuration logic

**AudioScript** is built to power:
- `play()`, `pause()`, `stop()`, `rewind()` - Real-time audio control
- `glow()`, `pulse()`, `mood.set()` - Emotionally-driven light mapping
- `@define`, `@wait`, `@loop`, `@if` - Performance scripting and state logic

Declared file extensions:
- `.audioscript`
- `.as`

## 💚🎧 Made With Love

**AudioScript** is being actively developed as part of the **AudioMIX** project by *Alexis M Vasquez (@alexisvassquez)*, terminal-loving creative engineer and musical systems thinker. If you'd like to contribute to syntax themes or parsers for your favorite editor, feel free to open a PR, issue, or email [alexis@alexismvasquez.com](mailto:alexis@alexismvasquez.com).

## License

This project is licensed under the **GNU General Public License v3.0 (GPLv3)**.

This means:
- You are free to use, modify, and distribute the software.
- Any derivative work must also be open source under the same license.
- Commercial use is permitted as long as credit and license compliance are maintained.

[Read the full license →](https://www.gnu.org/licenses/gpl-3.0.en.html)
