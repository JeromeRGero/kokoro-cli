# Kokoro TTS CLI

A simple command-line interface for [Kokoro-82M](https://github.com/hexgrad/kokoro), an open-source text-to-speech model.

## Features

- 🗣️ Natural-sounding text-to-speech
- 🎭 Multiple voices (male, female, British)
- 📄 Read from files or command-line text
- 💾 Auto-saves all audio files
- 🔊 Auto-plays generated speech
- 🌍 Cross-platform (macOS, Linux, Windows)

## Quick Start

### Installation

```bash
# Install dependencies
pip install kokoro soundfile

# Download the script
curl -O https://raw.githubusercontent.com/JeromeRGero/kokoro-cli/main/kokoro-tts.py

# Make it executable (macOS/Linux)
chmod +x kokoro-tts.py
```

### Usage

```bash
# macOS/Linux (if you set up the global command)
kokoro --michael "Hello world"

# Or use Python directly
python3 kokoro-tts.py --michael "Hello world"

# Read a file
python3 kokoro-tts.py --echo --file story.txt

# Get help
python3 kokoro-tts.py --help
```

## Available Voices

### Male Voices (⭐ = Best Quality)
- `am_fenrir` ⭐
- `am_michael` ⭐
- `am_puck` ⭐
- `am_adam`
- `am_echo`
- `am_eric`
- `am_liam`
- `am_onyx`
- `am_santa`

### Female Voices
- `af_heart` (default)
- `af_bella`
- `af_sarah`
- `af_sky`
- `af_nicole`
- `af_nova`
- `af_alloy`
- `af_aoede`
- `af_jessica`
- `af_river`
- `af_kore`

### British
- `bf_emma`

## Examples

```bash
# Use voice shortcuts
python3 kokoro-tts.py --michael "This is easy"
python3 kokoro-tts.py --fenrir "Best quality voice"
python3 kokoro-tts.py --bella "Female voice"

# Read from files
python3 kokoro-tts.py --echo story.txt
python3 kokoro-tts.py --michael --file README.md

# Use full voice names
python3 kokoro-tts.py -v am_michael "Using the -v flag"
```

## Global Command Setup (Optional)

### macOS/Linux

Add to your shell profile (~/.zshrc or ~/.bashrc):

```bash
mkdir -p ~/bin
cat > ~/bin/kokoro << 'EOF'
#!/bin/bash
exec python3 "$HOME/kokoro-tts.py" "$@"
EOF
chmod +x ~/bin/kokoro
export PATH="$HOME/bin:$PATH"
```

Then reload: `source ~/.zshrc`

Now you can just use: `kokoro --michael "text"`

### Windows

Create a batch file `kokoro.bat` in a folder that's in your PATH:

```batch
@echo off
python "%USERPROFILE%\kokoro-tts.py" %*
```

## Output

All audio files are saved with timestamps:
- **macOS/Linux**: `~/kokoro-audio/kokoro_TIMESTAMP.wav`
- **Windows**: `kokoro-audio/kokoro_TIMESTAMP.wav` (in current directory)

Files are 24kHz WAV format and can be replayed anytime.

## Platform Notes

### macOS
- Uses built-in `afplay` for audio playback
- Everything works out of the box

### Linux
- Attempts to use `paplay`, `aplay`, `ffplay`, or `mpv` for playback
- Install one of these if audio doesn't auto-play

### Windows
- Uses `os.startfile()` to open the default audio player
- Files save to `kokoro-audio/` in your current directory

## Command Options

```
Usage: kokoro [OPTIONS] <text>
       kokoro [OPTIONS] --file <file>

Options:
  --voice, -v VOICE    Choose a voice (default: af_heart)
  --file, -f FILE      Read text from a file
  --help, -h           Show this help message

Voice Shortcuts:
  Male:   --michael, --adam, --echo, --fenrir, --eric, 
          --liam, --onyx, --puck, --santa
  Female: --bella, --sarah, --heart, --sky, --nicole, --nova
  British: --emma
```

## How It Works

1. Takes your text input (direct or from file)
2. Processes through the Kokoro-82M neural TTS model
3. Generates audio in segments (for long texts)
4. Concatenates all segments into one file
5. Saves to disk with timestamp
6. Automatically plays the audio

## Technical Details

- **Model**: Kokoro-82M (82 million parameters)
- **Framework**: PyTorch
- **Sample Rate**: 24kHz
- **Output Format**: WAV
- **Language**: American English
- **Max Length**: Handles texts of any length (splits into segments)

## Troubleshooting

### "ModuleNotFoundError: No module named 'kokoro'"

Install the dependencies:
```bash
pip install kokoro soundfile
```

### Audio doesn't play

The file is still saved. Play it manually:
- **macOS**: `afplay ~/kokoro-audio/kokoro_*.wav`
- **Linux**: `mpv ~/kokoro-audio/kokoro_*.wav`
- **Windows**: Double-click the file in File Explorer

### "command not found: kokoro"

Either:
1. Set up the global command (see instructions above)
2. Use `python3 kokoro-tts.py` instead
3. Restart your terminal after setup

## Credits

- **Kokoro Model**: [hexgrad/Kokoro-82M](https://github.com/hexgrad/kokoro)
- **Voice Data**: See [VOICES.md](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md) on HuggingFace

## License

This CLI wrapper is provided as-is. The Kokoro model is Apache-2.0 licensed.

## Links

- [Kokoro GitHub](https://github.com/hexgrad/kokoro)
- [Kokoro on HuggingFace](https://huggingface.co/hexgrad/Kokoro-82M)
- [Voice Documentation](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md)
