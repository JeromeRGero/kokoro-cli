# Kokoro TTS Setup

Local text-to-speech system using the Kokoro-82M model. Works on macOS, Linux, and Windows.

## What It Does

Converts text to natural-sounding speech. Feed it text directly or from a file, choose a voice, and it generates audio that plays automatically and saves for later playback.

## Quick Start

### macOS/Linux
```bash
# Simple text
kokoro --michael "Hello world"

# Read a file
kokoro --echo README.md

# Use full voice names
kokoro -v am_fenrir "This voice has the best quality"

# Get help
kokoro --help
```

### Windows
```powershell
# Simple text
python kokoro-tts.py --michael "Hello world"

# Read a file
python kokoro-tts.py --echo README.md

# Get help
python kokoro-tts.py --help
```

## Installation

### macOS/Linux

1. Install Python 3.7+ (usually pre-installed on macOS)
2. Install dependencies:
   ```bash
   pip3 install kokoro soundfile
   ```
3. Download `kokoro-tts.py` from this repository
4. Make it executable:
   ```bash
   chmod +x kokoro-tts.py
   ```
5. (Optional) Set up global command:
   ```bash
   mkdir -p ~/bin
   echo '#!/bin/zsh' > ~/bin/kokoro
   echo 'exec python3 "$HOME/kokoro-tts.py" "$@"' >> ~/bin/kokoro
   chmod +x ~/bin/kokoro
   echo 'export PATH="$HOME/bin:$PATH"' >> ~/.zshrc  # or ~/.bashrc for bash
   source ~/.zshrc
   ```

### Windows (Python 3.13+)

**Important**: Python 3.13+ requires installation from source due to dependency compatibility. Follow these steps:

1. **Install Python 3.13+** from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation

2. **Open PowerShell** and navigate to where you want to install

3. **Clone this repository**:
   ```powershell
   git clone https://github.com/JeromeRGero/kokoro-cli.git
   cd kokoro-cli
   ```

4. **Install PyTorch** (with CUDA for GPU acceleration):
   ```powershell
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```
   This will download ~2.8 GB. Be patient!

5. **Install core dependencies**:
   ```powershell
   pip install soundfile huggingface_hub loguru transformers scipy
   ```

6. **Install spaCy** (NLP processing):
   ```powershell
   pip install spacy
   ```

7. **Create a constraints file** (prevents version conflicts):
   ```powershell
   echo spacy==3.8.11 > constraints.txt
   echo thinc==8.3.10 >> constraints.txt
   echo blis==1.3.3 >> constraints.txt
   ```

8. **Install misaki from GitHub** (text-to-phoneme conversion):
   ```powershell
   pip install git+https://github.com/hexgrad/misaki.git -c constraints.txt
   ```

9. **Clone and install kokoro**:
   ```powershell
   cd ..
   git clone https://github.com/hexgrad/kokoro.git
   pip install .\kokoro -c kokoro-cli\constraints.txt
   ```

10. **Clean up and test**:
    ```powershell
    del kokoro-cli\constraints.txt
    cd kokoro-cli
    python kokoro-tts.py --michael "Hello world"
    ```

**Why these steps?**
- PyPI versions of kokoro don't support Python 3.13 yet
- GitHub source versions support Python 3.13
- Constraints prevent spaCy from upgrading to dev versions that fail to build on Windows

**Windows Note**: Audio will auto-play using your default audio player. Files are saved to `C:\Users\YourName\kokoro-audio\`

### Windows (Python 3.12 and below)

1. Install Python 3.10-3.12 from [python.org](https://www.python.org/downloads/)
2. Install dependencies:
   ```powershell
   pip install kokoro soundfile
   ```
3. Download `kokoro-tts.py` from this repository
4. Place it somewhere convenient (e.g., `C:\Users\YourName\kokoro-tts.py`)
5. Run with: `python kokoro-tts.py [options]`

## File Locations

### macOS/Linux
- **Main script**: `~/kokoro-tts.py`
- **Global command**: `~/bin/kokoro` (if configured)
- **Audio output**: `~/kokoro-audio/`

### Windows
- **Main script**: Wherever you placed it
- **Audio output**: `kokoro-audio/` in current directory

## Available Voices

### Male Voices
- `am_fenrir` ⭐ (Best quality - Grade B)
- `am_michael` ⭐ (Grade B)
- `am_puck` ⭐ (Grade B)
- `am_adam` (Grade D)
- `am_echo` (Grade C)
- `am_eric` (Grade C)
- `am_liam` (Grade C)
- `am_onyx` (Grade C)
- `am_santa` (Grade C)

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

## Usage Examples

```bash
# Voice shortcuts (easiest)
kokoro --michael "Read this text"
kokoro --fenrir "Best quality male voice"
kokoro --bella "Female voice"

# Read from files
kokoro --echo story.txt
kokoro --michael --file ~/Documents/article.md

# Full voice specification
kokoro -v am_michael "Using the -v flag"

# Default voice (af_heart - female)
kokoro "No voice specified uses default"
```

## Command Options

```
kokoro [OPTIONS] <text>
kokoro [OPTIONS] --file <file>

Options:
  --voice, -v VOICE    Choose a voice (default: af_heart)
  --file, -f FILE      Read text from a file
  --help, -h           Show help message

Voice Shortcuts:
  Male:   --michael, --adam, --echo, --fenrir, --eric, 
          --liam, --onyx, --puck, --santa
  Female: --bella, --sarah, --heart, --sky, --nicole, --nova
  British: --emma
```

## How It Works

1. Takes your text input (direct or from file)
2. Processes it through the Kokoro-82M neural TTS model
3. Generates audio in segments (for long texts)
4. Concatenates all segments into one file
5. Saves to `~/kokoro-audio/kokoro_TIMESTAMP.wav`
6. Automatically plays the audio

## Files Generated

Audio files are saved with timestamps:
```
~/kokoro-audio/kokoro_20251121_122235.wav
~/kokoro-audio/kokoro_20251121_123456.wav
```

Each file is a complete WAV file (24kHz sample rate) that you can replay anytime:
```bash
# macOS
afplay ~/kokoro-audio/kokoro_20251121_122235.wav

# Linux  
mpv ~/kokoro-audio/kokoro_20251121_122235.wav

# Windows
# Double-click the file in File Explorer
```

Or open the folder:
```bash
# macOS
open ~/kokoro-audio

# Linux
xdg-open ~/kokoro-audio

# Windows
explorer kokoro-audio
```

## Technical Details

- **Model**: Kokoro-82M (82 million parameters)
- **Framework**: PyTorch
- **Sample Rate**: 24kHz
- **Output Format**: WAV
- **G2P Library**: Misaki
- **Language**: American English (lang_code: 'a')

## Troubleshooting

### "kokoro: command not found"

Restart your terminal or run:
```bash
source ~/.zshrc  # or source ~/.bashrc
```

### Missing Dependencies

If you get import errors, reinstall:
```bash
pip3 install kokoro soundfile
```

### Audio Not Playing

The file is still saved. Play it manually:
- **macOS**: `afplay ~/kokoro-audio/kokoro_*.wav`
- **Linux**: `mpv ~/kokoro-audio/kokoro_*.wav` (install mpv if needed)
- **Windows**: Double-click the WAV file in File Explorer

## Uninstallation

To remove Kokoro TTS:
```bash
rm ~/kokoro-tts.py
rm ~/bin/kokoro
rm -rf ~/kokoro-audio
pip3 uninstall kokoro soundfile
```

## Resources

- **Official Repo**: https://github.com/hexgrad/kokoro
- **Model on HuggingFace**: https://huggingface.co/hexgrad/Kokoro-82M
- **Voice Documentation**: https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md

## Notes

- This is TEXT-TO-SPEECH (TTS), not speech-to-text
- For voice input/transcription, you'd need something like Whisper instead
- First run downloads voice models (~500KB each) from HuggingFace
- Subsequent runs are fast (voices are cached locally)
- Long texts are automatically split into segments and concatenated
