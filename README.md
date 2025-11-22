# Kokoro TTS CLI

A simple command-line interface for [Kokoro-82M](https://github.com/hexgrad/kokoro), an open-source text-to-speech model with natural-sounding voices.

## Features

- 🗣️ **Natural-sounding text-to-speech** - 82M parameter neural TTS model
- 🎭 **Multiple voices** - Male, female, and British accents
- 📄 **Flexible input** - Read from command-line text or files
- 💾 **Auto-saves audio** - All generated speech saved as WAV files
- 🔊 **Auto-playback** - Hear your audio immediately
- 🌍 **Cross-platform** - Works on macOS, Linux, and Windows

## Quick Start

### Installation

**macOS/Linux:**
```bash
pip3 install kokoro soundfile
curl -O https://raw.githubusercontent.com/JeromeRGero/kokoro-cli/main/kokoro-tts.py
chmod +x kokoro-tts.py
```

**Windows (Python 3.12 and below):**
```powershell
pip install kokoro soundfile sounddevice
git clone https://github.com/JeromeRGero/kokoro-cli.git
cd kokoro-cli
```

**Windows (Python 3.13+):**
Installation is more complex due to dependency compatibility. See [**INSTALLATION.md**](INSTALLATION.md) for detailed instructions.

### Basic Usage

```bash
# macOS/Linux
python3 kokoro-tts.py --michael "Hello world"

# Windows
python kokoro-tts.py --michael "Hello world"

# Read from a file
python kokoro-tts.py --echo --file story.txt

# Get help
python kokoro-tts.py --help
```

## Available Voices

### Male Voices (⭐ = Best Quality)
- `--fenrir` ⭐ (am_fenrir)
- `--michael` ⭐ (am_michael)
- `--puck` ⭐ (am_puck)
- `--adam`, `--echo`, `--eric`, `--liam`, `--onyx`, `--santa`

### Female Voices
- `--heart` (af_heart) - Default
- `--bella`, `--sarah`, `--sky`, `--nicole`, `--nova`
- `--alloy`, `--aoede`, `--jessica`, `--river`, `--kore`

### British
- `--emma` (bf_emma)

## Examples

```bash
# Use voice shortcuts
python kokoro-tts.py --michael "This is easy"
python kokoro-tts.py --fenrir "Best quality voice"
python kokoro-tts.py --bella "Female voice"
python kokoro-tts.py --emma "British accent"

# Read from files
python kokoro-tts.py --echo story.txt
python kokoro-tts.py --michael --file README.md

# Use full voice names with -v flag
python kokoro-tts.py -v am_michael "Using the -v flag"
```

## Output Files

Audio files are automatically saved with timestamps:

- **macOS/Linux**: `~/kokoro-audio/kokoro_YYYYMMDD_HHMMSS.wav`
- **Windows**: `C:\Users\YourName\kokoro-audio\kokoro_YYYYMMDD_HHMMSS.wav`

Files are in 24kHz WAV format and can be replayed anytime.

## Command Reference

```
Usage: python kokoro-tts.py [OPTIONS] <text>
       python kokoro-tts.py [OPTIONS] --file <file>

Options:
  --voice, -v VOICE    Choose a voice (default: af_heart)
  --file, -f FILE      Read text from a file
  --help, -h           Show this help message

Voice Shortcuts:
  Male:    --michael, --adam, --echo, --fenrir, --eric,
           --liam, --onyx, --puck, --santa
  Female:  --bella, --sarah, --heart, --sky, --nicole,
           --nova, --alloy, --aoede, --jessica, --river, --kore
  British: --emma
```

## Optional: Global Command Setup

Make `kokoro` available from anywhere on your system.

### macOS/Linux

Add to `~/.zshrc` or `~/.bashrc`:

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

Now use: `kokoro --michael "Hello world"`

### Windows

Add to your PowerShell profile (`$PROFILE`):

```powershell
function kokoro { python C:\path\to\kokoro-cli\kokoro-tts.py $args }
```

Then use: `kokoro --michael "Hello world"`

## How It Works

1. Takes your text input (direct or from file)
2. Processes through the Kokoro-82M neural TTS model
3. Generates audio in segments (for long texts)
4. Concatenates segments into one file
5. Saves to disk with timestamp
6. Automatically plays the audio

## Technical Details

- **Model**: Kokoro-82M (82 million parameters)
- **Framework**: PyTorch
- **Sample Rate**: 24kHz
- **Output Format**: WAV
- **Language**: American English
- **Max Length**: Unlimited (automatically splits long texts)

## Troubleshooting

### Installation Issues

**"ModuleNotFoundError: No module named 'kokoro'"**

Install the dependencies:
```bash
pip install kokoro soundfile
```

For Python 3.13+ on Windows, see [INSTALLATION.md](INSTALLATION.md).

**Build errors on Windows (blis, spaCy, etc.)**

See the detailed [Windows Python 3.13+ installation guide](INSTALLATION.md#windows-python-313).

**"TypeError: unsupported operand type(s) for +: 'NoneType' and 'str'"**

Your misaki version is outdated. Install the latest from GitHub:
```bash
pip install git+https://github.com/hexgrad/misaki.git
```

### Audio Issues

**Audio doesn't play**

The file is still saved. Play it manually:
- **macOS**: `afplay ~/kokoro-audio/kokoro_*.wav`
- **Linux**: `mpv ~/kokoro-audio/kokoro_*.wav`
- **Windows**: Double-click the file in File Explorer

**First run is slow / downloads files**

This is normal! The first run downloads:
- Kokoro TTS model (~327 MB) - one time only
- Voice files (~523 KB each) - cached after first use
- spaCy language model (~12 MB) - one time only

Subsequent runs will be much faster.

### Platform-Specific Notes

**macOS**
- Uses built-in `afplay` for audio playback
- Everything works out of the box

**Linux**
- Attempts to use `paplay`, `aplay`, `ffplay`, or `mpv` for playback
- Install one of these if audio doesn't auto-play

**Windows**
- Uses `sounddevice` for seamless terminal playback (no GUI windows!)
- Falls back to default player if sounddevice not installed
- Audio output folder: `C:\Users\YourName\kokoro-audio\`

## Documentation

- [**INSTALLATION.md**](INSTALLATION.md) - Detailed installation instructions for all platforms

## Credits

- **Kokoro Model**: [hexgrad/Kokoro-82M](https://github.com/hexgrad/kokoro)
- **Voice Documentation**: [VOICES.md on HuggingFace](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md)

## License

This CLI wrapper is provided as-is. The Kokoro model is Apache-2.0 licensed.

## Links

- [Kokoro GitHub](https://github.com/hexgrad/kokoro)
- [Kokoro on HuggingFace](https://huggingface.co/hexgrad/Kokoro-82M)
- [Voice Documentation](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md)
