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

#### Windows (Recommended for Python 3.13+)

**Important**: If you're using Python 3.13+, follow these steps for a working installation:

```powershell
# 1. Clone or download this repository
git clone https://github.com/JeromeRGero/kokoro-cli.git
cd kokoro-cli

# 2. Install PyTorch first (with CUDA support for GPU acceleration)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 3. Install core dependencies
pip install soundfile huggingface_hub loguru transformers scipy

# 4. Install spaCy (pre-built wheels available)
pip install spacy

# 5. Create a constraints file to prevent spaCy upgrade issues
echo spacy==3.8.11 > constraints.txt
echo thinc==8.3.10 >> constraints.txt
echo blis==1.3.3 >> constraints.txt

# 6. Install misaki from GitHub (latest version not on PyPI)
pip install git+https://github.com/hexgrad/misaki.git -c constraints.txt

# 7. Clone and install kokoro from source
cd ..
git clone https://github.com/hexgrad/kokoro.git
pip install .\kokoro -c kokoro-cli\constraints.txt

# 8. Clean up constraints file
del kokoro-cli\constraints.txt

# 9. Test the installation
cd kokoro-cli
python kokoro-tts.py --michael "Hello world"
```

#### Windows (Python 3.12 and below) / macOS / Linux

```bash
# Install dependencies
pip install kokoro soundfile

# Download the script
curl -O https://raw.githubusercontent.com/JeromeRGero/kokoro-cli/main/kokoro-tts.py

# Make it executable (macOS/Linux only)
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

**Option 1: PowerShell Function (Recommended)**

Add this to your PowerShell profile (`$PROFILE`):

```powershell
function kokoro { python C:\path\to\kokoro-cli\kokoro-tts.py $args }
```

Then use: `kokoro --michael "Hello world"`

**Option 2: Batch File**

Create a batch file `kokoro.bat` in a folder that's in your PATH:

```batch
@echo off
python "C:\path\to\kokoro-cli\kokoro-tts.py" %*
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

### Windows: Build errors during installation (blis, spaCy)

If you get compilation errors on Windows, especially with Python 3.13+:
1. Use the Windows-specific installation steps above
2. Install from GitHub sources instead of PyPI
3. Use constraints to prevent spaCy from upgrading to dev versions

### "ModuleNotFoundError: No module named 'kokoro'"

Install the dependencies:
```bash
# Python 3.12 and below
pip install kokoro soundfile

# Python 3.13+ (Windows)
# Follow the full Windows installation steps above
```

### "TypeError: unsupported operand type(s) for +: 'NoneType' and 'str'"

This means your misaki version is outdated. Install the latest from GitHub:
```bash
pip install git+https://github.com/hexgrad/misaki.git
```

### Audio doesn't play

The file is still saved. Play it manually:
- **macOS**: `afplay ~/kokoro-audio/kokoro_*.wav`
- **Linux**: `mpv ~/kokoro-audio/kokoro_*.wav`
- **Windows**: Double-click the file in File Explorer or `explorer kokoro-audio`

### "command not found: kokoro"

Either:
1. Set up the global command (see instructions above)
2. Use `python3 kokoro-tts.py` (or `python` on Windows) instead
3. Restart your terminal after setup

### First run is slow / downloads files

This is normal! The first run downloads:
- Kokoro TTS model (~327 MB) - one time only
- Voice files (~523 KB each) - cached after first use
- spaCy language model (~12 MB) - one time only

Subsequent runs will be much faster.

## Credits

- **Kokoro Model**: [hexgrad/Kokoro-82M](https://github.com/hexgrad/kokoro)
- **Voice Data**: See [VOICES.md](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md) on HuggingFace

## License

This CLI wrapper is provided as-is. The Kokoro model is Apache-2.0 licensed.

## Links

- [Kokoro GitHub](https://github.com/hexgrad/kokoro)
- [Kokoro on HuggingFace](https://huggingface.co/hexgrad/Kokoro-82M)
- [Voice Documentation](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md)
